from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re
import os
import time # Added for retry delay
from langchain_core.tools import tool
import logging

# Configure logging
# Using a distinct logger name for this module can be helpful for filtering logs.
logger = logging.getLogger(__name__)

# Retry parameters
MAX_RETRIES = 20
RETRY_DELAY_SECONDS = 3
if not logger.hasHandlers(): # Avoid adding multiple handlers if this module is reloaded
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) # Default level, can be adjusted

# --- Helper Functions ---

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
            logger.warning(f"Error listing transcripts for video ID {video_id} (URL: {video_url}) on attempt {attempt + 1}: {type(e).__name__} - {str(e)}. Not retrying for this type of error.")
            raise e # Re-raise immediately, no retry for these specific errors
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed to list transcripts for video ID {video_id} (URL: {video_url}): {str(e)}", exc_info=True)
            if attempt + 1 < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Maximum retry attempts ({MAX_RETRIES}) reached for listing transcripts for video ID {video_id}. Raising last exception.")
                raise Exception(f"Failed to list transcripts for video ID {video_id} after {MAX_RETRIES} attempts: {str(e)}")
    if transcript_list_obj is None:
        # This case should ideally be covered by exceptions in the loop, but as a fallback:
        logger.error(f"Failed to obtain transcript list for {video_id} after all retries, and no specific exception was re-raised. This indicates an unexpected state.")
        raise Exception(f"Unknown error: Failed to list transcripts for video ID {video_id} after {MAX_RETRIES} attempts and no specific error was propagated.")

    available_langs = []
    for transcript_lang in transcript_list_obj:
        available_langs.append({
            'name': transcript_lang.language,
            'code': transcript_lang.language_code,
            'is_generated': transcript_lang.is_generated
            # 'original_api_object': transcript_lang # Optionally include for more direct API interaction if needed by agent
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
            logger.warning(f"Error fetching transcript for video ID {video_id}, lang {language_code} (URL: {video_url}) on attempt {attempt + 1}: {type(e).__name__} - {str(e)}. Not retrying for this type of error.")
            raise e # Re-raise immediately, no retry for these specific errors
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed to fetch transcript for video ID {video_id}, lang {language_code} (URL: {video_url}): {str(e)}", exc_info=True)
            if attempt + 1 < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Maximum retry attempts ({MAX_RETRIES}) reached for fetching transcript for video ID {video_id}, lang {language_code}. Raising last exception.")
                raise Exception(f"Failed to fetch transcript for video ID {video_id} (lang: {language_code}) after {MAX_RETRIES} attempts: {str(e)}")
    if transcript_entries is None:
        # This case should ideally be covered by exceptions in the loop, but as a fallback:
        logger.error(f"Failed to obtain transcript entries for {video_id}, lang {language_code} after all retries, and no specific exception was re-raised. This indicates an unexpected state.")
        raise Exception(f"Unknown error: Failed to fetch transcript for video ID {video_id} (lang: {language_code}) after {MAX_RETRIES} attempts and no specific error was propagated.")

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
