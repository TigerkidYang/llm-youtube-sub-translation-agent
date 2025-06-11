from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re
import os
import time # For implementing retry delays
from langchain_core.tools import tool
import logging
import yt_dlp
import json
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Configure logging
# Using a distinct logger name for this module can be helpful for filtering logs.
logger = logging.getLogger(__name__)

# Retry parameters
MAX_RETRIES = int(os.environ.get("YOUTUBE_API_MAX_RETRIES", "1"))
RETRY_DELAY_SECONDS = int(os.environ.get("YOUTUBE_API_RETRY_DELAY_SECONDS", "3"))
if not logger.hasHandlers(): # Avoid adding multiple handlers if this module is reloaded
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) # Default level, can be adjusted

# --- Helper Functions ---

def _convert_vtt_to_srt_time(vtt_time: str) -> str:
    """Convert WebVTT time format to SRT time format"""
    # VTT: 00:00:01.500 -> SRT: 00:00:01,500
    return vtt_time.replace('.', ',')

def _convert_yt_dlp_subtitles_to_srt(subtitles_data: list) -> str:
    """Convert yt-dlp subtitle data to SRT format"""
    srt_lines = []
    
    for i, entry in enumerate(subtitles_data, 1):
        # yt-dlp returns subtitle entries with 'start', 'end', and 'text' fields
        start_time = entry.get('start', 0)
        end_time = entry.get('end', start_time + 1)
        text = entry.get('text', '').strip()
        
        if not text:
            continue
            
        # Convert seconds to SRT format
        start_srt = format_time_srt(start_time)
        end_srt = format_time_srt(end_time)
        
        srt_lines.append(str(i))
        srt_lines.append(f"{start_srt} --> {end_srt}")
        srt_lines.append(text)
        srt_lines.append("")  # Blank line
    
    return "\n".join(srt_lines)

def _fetch_subtitles_with_yt_dlp(video_url: str, language_code: str = None) -> tuple:
    """
    Fetch subtitles using yt-dlp as backup method
    
    Returns:
        tuple: (subtitles_content, available_languages)
        subtitles_content: SRT format string if language_code specified, None otherwise
        available_languages: list of available language info
    """
    logger.info(f"Using yt-dlp to fetch subtitles for: {video_url}")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['all'] if not language_code else [language_code],
        'skip_download': True,
        'subtitlesformat': 'vtt',  # yt-dlp works best with vtt
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info about the video
            info = ydl.extract_info(video_url, download=False)
            
            # Get available subtitle languages
            available_subs = info.get('subtitles', {})
            auto_subs = info.get('automatic_captions', {})
            
            # Combine manual and auto subtitles
            all_subs = {**available_subs, **auto_subs}
            
            # Format available languages info
            available_languages = []
            for lang_code, sub_info in all_subs.items():
                lang_name = lang_code  # yt-dlp doesn't always provide full language names
                is_generated = lang_code in auto_subs
                available_languages.append({
                    'name': lang_name,
                    'code': lang_code, 
                    'is_generated': is_generated
                })
            
            # If no specific language requested, just return available languages
            if not language_code:
                logger.info(f"yt-dlp found {len(available_languages)} available subtitle languages")
                return None, available_languages
            
            # Try to get subtitles for specific language
            if language_code not in all_subs:
                raise NoTranscriptFound(f"Language '{language_code}' not found in available subtitles")
            
            # Download subtitles to temporary file
            with tempfile.TemporaryDirectory() as temp_dir:
                ydl_opts_download = {
                    'quiet': True,
                    'no_warnings': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': [language_code],
                    'skip_download': True,
                    'subtitlesformat': 'vtt',
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                }
                
                with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
                    ydl_download.download([video_url])
                
                # Find the downloaded subtitle file
                vtt_files = [f for f in os.listdir(temp_dir) if f.endswith(f'.{language_code}.vtt')]
                if not vtt_files:
                    raise NoTranscriptFound(f"Failed to download subtitles for language '{language_code}'")
                
                vtt_file_path = os.path.join(temp_dir, vtt_files[0])
                
                # Parse VTT file and convert to SRT
                with open(vtt_file_path, 'r', encoding='utf-8') as f:
                    vtt_content = f.read()
                
                # Simple VTT to SRT conversion
                srt_content = _convert_vtt_to_srt_format(vtt_content)
                logger.info(f"Successfully converted yt-dlp VTT to SRT format")
                
                return srt_content, available_languages
                
    except Exception as e:
        logger.error(f"yt-dlp failed to fetch subtitles: {str(e)}")
        raise e

def _convert_vtt_to_srt_format(vtt_content: str) -> str:
    """Convert VTT format to SRT format"""
    lines = vtt_content.split('\n')
    srt_lines = []
    entry_num = 1
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip metadata lines and empty lines
        if line.startswith('WEBVTT') or line.startswith('NOTE') or not line:
            i += 1
            continue
        
        # Look for timestamp lines (format: 00:00:01.500 --> 00:00:03.500)
        if '-->' in line:
            # Convert VTT time to SRT time
            time_line = line.replace('.', ',')
            
            # Get subtitle text (next non-empty lines until empty line or next timestamp)
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                text_lines.append(lines[i].strip())
                i += 1
            
            if text_lines:
                srt_lines.append(str(entry_num))
                srt_lines.append(time_line)
                srt_lines.extend(text_lines)
                srt_lines.append("")  # Empty line
                entry_num += 1
        else:
            i += 1
    
    return '\n'.join(srt_lines)

def format_time_srt(time_seconds: float) -> str:
    """Converts seconds to SRT time format HH:MM:SS,mmm"""
    if time_seconds < 0:
        time_seconds = 0
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    milliseconds = int(round((time_seconds - int(time_seconds)) * 1000))
    
    if milliseconds == 1000:
        seconds += 1
        milliseconds = 0
        if seconds == 60:
            minutes += 1
            seconds = 0
            if minutes == 60:
                hours += 1
                minutes = 0
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def _extract_video_id(video_url: str) -> str:
    """Extracts YouTube video ID from various URL formats."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    logger.error(f"Could not extract video ID from URL: {video_url}")
    raise ValueError(f"Could not extract video ID from URL: {video_url}")

# --- Tool Functions for LangGraph Agent ---
@tool
def list_available_languages(video_url: str) -> list:
    """
    Lists available subtitle languages for a given YouTube video URL.

    Args:
        video_url (str): The YouTube video URL.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              {'name': str (e.g., 'English'), 
               'code': str (e.g., 'en'), 
               'is_generated': bool}
    
    Raises:
        ValueError: If the video URL is invalid.
        TranscriptsDisabled: If transcripts are disabled for this video.
        NoTranscriptFound: If no transcripts are available at all.
        Exception: For other unexpected errors from the API.
    """
    logger.info(f"Attempting to list available languages for URL: {video_url}")
    video_id = _extract_video_id(video_url) 
    logger.debug(f"Extracted video ID: {video_id} for URL: {video_url}")
    
    transcript_list_obj = None
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Attempt {attempt + 1}/{MAX_RETRIES} to list available languages for video ID {video_id}...")
            transcript_list_obj = YouTubeTranscriptApi.list_transcripts(video_id)
            logger.debug(f"Successfully listed transcripts for video ID {video_id} on attempt {attempt + 1}.")
            break # Success, exit retry loop
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.warning(f"Error listing transcripts for video ID {video_id} (URL: {video_url}) on attempt {attempt + 1}: {type(e).__name__} - {str(e)}. Trying yt-dlp as fallback...")
            # Try yt-dlp as fallback for these specific errors
            try:
                _, available_languages_fallback = _fetch_subtitles_with_yt_dlp(video_url)
                if available_languages_fallback:
                    logger.info(f"yt-dlp fallback succeeded for {type(e).__name__} error, found {len(available_languages_fallback)} languages")
                    return available_languages_fallback
                else:
                    raise e  # If yt-dlp also fails, raise original error
            except Exception as fallback_error:
                logger.error(f"yt-dlp fallback failed for {type(e).__name__}: {str(fallback_error)}")
                raise e  # Raise original error if fallback fails
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed to list transcripts for video ID {video_id} (URL: {video_url}): {str(e)}", exc_info=True)
            if attempt + 1 < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Maximum retry attempts ({MAX_RETRIES}) reached for listing transcripts for video ID {video_id}. Trying yt-dlp as fallback...")
                # Try yt-dlp as fallback
                try:
                    _, available_languages_fallback = _fetch_subtitles_with_yt_dlp(video_url)
                    if available_languages_fallback:
                        logger.info(f"yt-dlp fallback succeeded, found {len(available_languages_fallback)} languages")
                        return available_languages_fallback
                    else:
                        raise Exception("yt-dlp fallback returned no languages")
                except Exception as fallback_error:
                    logger.error(f"yt-dlp fallback also failed: {str(fallback_error)}")
                    raise Exception(f"Both youtube_transcript_api and yt-dlp failed. Primary error: {str(e)}. Fallback error: {str(fallback_error)}")
    if transcript_list_obj is None:
        # This case should ideally be covered by exceptions in the loop, but as a fallback:
        logger.error(f"Failed to obtain transcript list for {video_id} after all retries, and no specific exception was re-raised. This indicates an unexpected state.")
        # Try yt-dlp as final fallback
        try:
            _, available_languages_fallback = _fetch_subtitles_with_yt_dlp(video_url)
            if available_languages_fallback:
                logger.info(f"yt-dlp final fallback succeeded")
                return available_languages_fallback
        except:
            pass
        raise Exception(f"Unknown error: Failed to list transcripts for video ID {video_id} after {MAX_RETRIES} attempts and fallback methods failed.")

    available_langs = []
    for transcript_lang in transcript_list_obj:
        available_langs.append({
            'name': transcript_lang.language,
            'code': transcript_lang.language_code,
            'is_generated': transcript_lang.is_generated
        })
    
    if not available_langs:
        logger.warning(f"No subtitle languages found for video ID {video_id} (URL: {video_url}), though transcripts are not explicitly disabled.")
        raise NoTranscriptFound(f"No subtitle languages found for video ID {video_id}, though transcripts are not explicitly disabled.")
    
    logger.info(f"Found {len(available_langs)} available languages for video ID {video_id} (URL: {video_url}).")
    logger.debug(f"Available languages for {video_id}: {available_langs}")
    return available_langs

@tool
def fetch_youtube_srt(video_url: str, language_code: str, output_srt_path: str) -> str:
    """
    Fetches subtitles for a given YouTube video URL and language, 
    returning SRT content as a string or saving it to a file.

    Args:
        video_url (str): The YouTube video URL.
        language_code (str): The desired language code (e.g., 'en', 'zh-Hans').
                               This code should be one of those returned by list_available_languages.
        output_srt_path (str): The full path where the SRT file MUST be saved (e.g., 'path/to/video_en.srt').
                                     The LLM is responsible for constructing a suitable path, for example, using the video ID and language code
                                     (e.g., 'videoid_lang.srt'), and saving the file in the current working directory.

    Returns:
        str: The full path to the saved SRT file. This path is the one provided in the 'output_srt_path' argument, where the file has been saved.

    Raises:
        ValueError: If video URL is invalid or video ID cannot be extracted.
        NoTranscriptFound: If the specified language_code transcript is not found by the API.
        TranscriptsDisabled: If transcripts are disabled for the video (might be caught by get_transcript too).
        IOError: If output_srt_path is provided and file writing fails.
        Exception: For other unexpected errors from the API or file system.
    """
    logger.info(f"Attempting to fetch SRT for URL: {video_url}, language: {language_code}, output: {output_srt_path}")
    video_id = _extract_video_id(video_url)
    logger.debug(f"Extracted video ID: {video_id} for URL: {video_url}")

    transcript_entries = None
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Attempt {attempt + 1}/{MAX_RETRIES} to fetch transcript for video ID {video_id}, language {language_code}...")
            # Fetches a list of dictionaries: [{'text': '...', 'start': ..., 'duration': ...}, ...]
            transcript_entries = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
            logger.debug(f"Successfully fetched transcript data on attempt {attempt + 1} for video ID {video_id}, language {language_code}. Entries: {len(transcript_entries)}")
            break # Success, exit retry loop
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            logger.warning(f"Error fetching transcript for video ID {video_id}, lang {language_code} (URL: {video_url}) on attempt {attempt + 1}: {type(e).__name__} - {str(e)}. Trying yt-dlp as fallback...")
            # Try yt-dlp as fallback for these specific errors
            try:
                srt_content_fallback, _ = _fetch_subtitles_with_yt_dlp(video_url, language_code)
                if srt_content_fallback:
                    logger.info(f"yt-dlp fallback succeeded for {type(e).__name__} error, language {language_code}")
                    # Save the content to file
                    output_dir = os.path.dirname(output_srt_path)
                    if output_dir and not os.path.exists(output_dir):
                        logger.info(f"Creating output directory: {output_dir}")
                        os.makedirs(output_dir, exist_ok=True)
                    
                    try:
                        with open(output_srt_path, 'w', encoding='utf-8') as f:
                            f.write(srt_content_fallback)
                        logger.info(f"Successfully wrote yt-dlp SRT content to: {output_srt_path}")
                        return output_srt_path
                    except Exception as file_error:
                        logger.error(f"Failed to write yt-dlp content to file: {str(file_error)}")
                        raise e  # Raise original error if file writing fails
                else:
                    raise e  # If yt-dlp also fails, raise original error
            except Exception as fallback_error:
                logger.error(f"yt-dlp fallback failed for {type(e).__name__}: {str(fallback_error)}")
                raise e  # Raise original error if fallback fails
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed to fetch transcript for video ID {video_id}, lang {language_code} (URL: {video_url}): {str(e)}", exc_info=True)
            if attempt + 1 < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Maximum retry attempts ({MAX_RETRIES}) reached for fetching transcript for video ID {video_id}, lang {language_code}. Trying yt-dlp as fallback...")
                # Try yt-dlp as fallback
                try:
                    srt_content_fallback, _ = _fetch_subtitles_with_yt_dlp(video_url, language_code)
                    if srt_content_fallback:
                        logger.info(f"yt-dlp fallback succeeded for language {language_code}")
                        # Save the content to file
                        output_dir = os.path.dirname(output_srt_path)
                        if output_dir and not os.path.exists(output_dir):
                            logger.info(f"Creating output directory: {output_dir}")
                            os.makedirs(output_dir, exist_ok=True)
                        
                        try:
                            with open(output_srt_path, 'w', encoding='utf-8') as f:
                                f.write(srt_content_fallback)
                            logger.info(f"Successfully wrote yt-dlp SRT content to: {output_srt_path}")
                            return output_srt_path
                        except Exception as file_error:
                            logger.error(f"Failed to write yt-dlp content to file: {str(file_error)}")
                            raise IOError(f"Failed to write SRT file to {output_srt_path}: {str(file_error)}")
                    else:
                        raise Exception("yt-dlp fallback returned no content")
                except Exception as fallback_error:
                    logger.error(f"yt-dlp fallback also failed: {str(fallback_error)}")
                    raise Exception(f"Both youtube_transcript_api and yt-dlp failed. Primary error: {str(e)}. Fallback error: {str(fallback_error)}")
    if transcript_entries is None:
        # This case should ideally be covered by exceptions in the loop, but as a fallback:
        logger.error(f"Failed to obtain transcript entries for {video_id}, lang {language_code} after all retries, and no specific exception was re-raised. This indicates an unexpected state.")
        # Try yt-dlp as final fallback
        try:
            srt_content_fallback, _ = _fetch_subtitles_with_yt_dlp(video_url, language_code)
            if srt_content_fallback:
                logger.info(f"yt-dlp final fallback succeeded for language {language_code}")
                # Save the content to file
                output_dir = os.path.dirname(output_srt_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                with open(output_srt_path, 'w', encoding='utf-8') as f:
                    f.write(srt_content_fallback)
                logger.info(f"Successfully wrote yt-dlp final fallback content to: {output_srt_path}")
                return output_srt_path
        except:
            pass
        raise Exception(f"Unknown error: Failed to fetch transcript for video ID {video_id} (lang: {language_code}) after {MAX_RETRIES} attempts and fallback methods failed.")

    if not transcript_entries: # Should be redundant if API raises NoTranscriptFound correctly
        logger.warning(f"Transcript data for video ID {video_id} (lang: {language_code}) was unexpectedly empty after fetch.")
        raise NoTranscriptFound(f"Transcript data for video ID {video_id} (lang: {language_code}) was unexpectedly empty after fetch.")

    srt_content_lines = []
    for i, entry in enumerate(transcript_entries):
        start_time_seconds = entry['start'] 
        duration_seconds = entry['duration']
        text = entry['text'].strip()
        end_time_seconds = start_time_seconds + duration_seconds

        srt_content_lines.append(str(i + 1))
        srt_content_lines.append(
            f"{format_time_srt(start_time_seconds)} --> {format_time_srt(end_time_seconds)}"
        )
        srt_content_lines.append(text)
        srt_content_lines.append("") # Blank line separator

    srt_content_string = "\n".join(srt_content_lines)

    output_dir = os.path.dirname(output_srt_path)
    if output_dir and not os.path.exists(output_dir): # Ensure directory exists
        logger.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content_string)
        logger.info(f"Successfully wrote SRT content to: {output_srt_path}")
    except IOError as e:
        logger.error(f"IOError writing SRT file to {output_srt_path}: {str(e)}", exc_info=True)
        raise IOError(f"Failed to write SRT file to {output_srt_path}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error writing SRT file to {output_srt_path}: {str(e)}", exc_info=True)
        raise Exception(f"Unexpected error writing SRT file to {output_srt_path}: {str(e)}")

    return output_srt_path
