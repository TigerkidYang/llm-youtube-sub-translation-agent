"""
YouTube Subtitle Translation Web Interface

This module provides a Streamlit-based web interface for the YouTube subtitle
translation system. It offers an intuitive UI for video processing, language
selection, translation management, and result visualization.

Key Features:
- Interactive video player with synchronized subtitles
- Multi-language UI support
- Real-time translation progress tracking
- Subtitle overlay controls
- Download functionality for translated subtitles
- Caching system for performance optimization

Dependencies:
- streamlit: Web interface framework
- Agent: Translation logic
- get_sub: Subtitle extraction
- languages: Multi-language support

Author: YouTube Subtitle Translation Project
License: MIT
"""

# Standard library imports
import os
import sys
import re
import json
import tempfile
import traceback
from typing import Dict, List

# Third-party imports
import streamlit as st

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local imports
from get_sub import list_available_languages
from Agent import translate_video_api, EXTRACTION_MODEL_NAME, TRANSLATION_MODEL_NAME, CONTEXT_MODEL_NAME
from languages import LANGUAGES

def get_text(key: str, **kwargs) -> str:
    """Get translated text based on current language"""
    if 'ui_language' not in st.session_state:
        st.session_state.ui_language = 'en'
    
    text = LANGUAGES.get(st.session_state.ui_language, LANGUAGES['en']).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

def language_selector():
    """Language selector in sidebar"""
    with st.sidebar:
        st.markdown("---")
        current_lang = st.session_state.get('ui_language', 'en')
        
        language_options = {lang_data['name']: lang_code for lang_code, lang_data in LANGUAGES.items()}
        
        selected_language_name = st.selectbox(
            "🌐 " + get_text("language_selector"),
            options=list(language_options.keys()),
            index=list(language_options.values()).index(current_lang)
        )
        
        selected_language_code = language_options[selected_language_name]
        
        if selected_language_code != current_lang:
            st.session_state.ui_language = selected_language_code
            st.rerun()

# Page configuration
st.set_page_config(
    page_title=get_text("page_title"),
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styles
st.markdown("""
<style>
    /* Maximize page width */
    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Player mode: full width layout */
    .player-mode .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stVideo {
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    /* Responsive video container */
    .video-container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Player mode: maximize video container */
    .player-mode .video-container {
        max-width: 100%;
    }
    
    /* Hide streamlit menu and footer for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide sidebar in player mode */
    .player-mode .css-1d391kg {
        display: none;
    }
    
    /* Expand main content in player mode */
    .player-mode .css-18e3th9 {
        margin-left: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def parse_srt_content(srt_content: str) -> List[Dict]:
    """Parse SRT content and return list of subtitle objects with timestamps in seconds"""
    subtitles = []
    if not srt_content:
        return subtitles
    
    # SRT pattern to match subtitle blocks
    pattern = re.compile(
        r'(\d+)\s*\n'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*\n'
        r'((?:.+\n?)+)', 
        re.MULTILINE
    )
    
    def srt_time_to_seconds(time_str):
        """Convert SRT time format (HH:MM:SS,mmm) to seconds"""
        time_parts = time_str.replace(',', '.').split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = float(time_parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    for match in pattern.finditer(srt_content):
        index = int(match.group(1))
        start_time = srt_time_to_seconds(match.group(2))
        end_time = srt_time_to_seconds(match.group(3))
        text = match.group(4).strip()
        
        # Clean up text - remove extra line breaks and spaces
        text = ' '.join(line.strip() for line in text.splitlines() if line.strip())
        
        subtitles.append({
            'index': index,
            'start': start_time,
            'end': end_time,
            'text': text
        })
    
    return subtitles

def create_video_player_with_subtitles(video_url: str, video_id: str, subtitles_data: List[Dict]):
    """Create a video player with synchronized subtitle display"""
    
    # Convert subtitles to JSON for JavaScript
    subtitles_json = json.dumps(subtitles_data)
    
    # Create HTML for the video player with subtitles
    html_code = f"""
    <div style="width: 100%; margin: 0; padding: 0;">
        <div style="position: relative; background: #000; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.3); width: 100%; height: 500px;">
            <iframe id="youtube-player" 
                width="100%" 
                height="100%" 
                src="https://www.youtube.com/embed/{video_id}?enablejsapi=1&rel=0&modestbranding=1&iv_load_policy=3" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
            </iframe>
            
            <!-- Subtitle overlay -->
            <div id="subtitle-overlay" style="
                position: absolute; 
                bottom: 6%; 
                left: 50%; 
                transform: translateX(-50%); 
                background: rgba(0, 0, 0, 0.85); 
                color: white; 
                padding: 8px 12px; 
                border-radius: 8px; 
                font-size: calc(12px + 0.5vw); 
                font-weight: 500; 
                text-align: center; 
                max-width: 90vw; 
                white-space: nowrap;
                overflow: visible;
                display: none;
                z-index: 100;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.9);
                line-height: 1.4;
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(4px);
                box-sizing: border-box;
            ">
                {get_text('no_subtitle_at_time')}
            </div>
        </div>
        
        <!-- Simple Control Panel -->
        <div style="margin-top: 15px; text-align: center;">
            <button id="subtitle-toggle" onclick="toggleSubtitleOverlay()" 
                    style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                🔇 {get_text('show_video_subtitles')}
            </button>
        </div>
    </div>

    <script>
        // Subtitles data
        const subtitles = {subtitles_json};
        let currentSubtitleIndex = -1;
        let player;
        let updateInterval;
        let subtitleOverlayEnabled = false;
        
        // Load YouTube IFrame API
        function loadYouTubeAPI() {{
            if (typeof YT !== 'undefined' && YT.Player) {{
                initializePlayer();
                return;
            }}
            
            const tag = document.createElement('script');
            tag.src = 'https://www.youtube.com/iframe_api';
            const firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            
            window.onYouTubeIframeAPIReady = initializePlayer;
        }}
        
        function initializePlayer() {{
            player = new YT.Player('youtube-player', {{
                events: {{
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}
        
        function onPlayerReady(event) {{
            console.log('YouTube player ready');
            startSubtitleSync();
        }}
        
        function onPlayerStateChange(event) {{
            // Pause/resume subtitle sync based on player state
            if (event.data === YT.PlayerState.PLAYING) {{
                startSubtitleSync();
            }} else if (event.data === YT.PlayerState.PAUSED) {{
                stopSubtitleSync();
            }}
        }}
        
        function startSubtitleSync() {{
            if (updateInterval) clearInterval(updateInterval);
            updateInterval = setInterval(() => {{
                if (player && player.getCurrentTime) {{
                    const currentTime = player.getCurrentTime();
                    updateCurrentSubtitle(currentTime);
                }}
            }}, 300); // Update every 300ms for smoother experience
        }}
        
        function stopSubtitleSync() {{
            if (updateInterval) {{
                clearInterval(updateInterval);
                updateInterval = null;
            }}
        }}
        
        function updateCurrentSubtitle(currentTime) {{
            const subtitle = findCurrentSubtitle(subtitles, currentTime);
            const subtitleOverlay = document.getElementById('subtitle-overlay');
            
            if (subtitle) {{
                const subtitleIndex = subtitles.indexOf(subtitle);
                if (subtitleIndex !== currentSubtitleIndex) {{
                    currentSubtitleIndex = subtitleIndex;
                    
                    // Update video overlay only if enabled
                    if (subtitleOverlayEnabled) {{
                        subtitleOverlay.style.opacity = '0';
                        setTimeout(() => {{
                            subtitleOverlay.textContent = subtitle.text;
                            subtitleOverlay.style.display = 'block';
                            subtitleOverlay.style.opacity = '1';
                        }}, 100);
                    }}
                }}
            }} else {{
                // No subtitle at current time
                if (currentSubtitleIndex !== -1) {{
                    currentSubtitleIndex = -1;
                    
                    // Hide video overlay
                    if (subtitleOverlayEnabled) {{
                        subtitleOverlay.style.opacity = '0';
                        setTimeout(() => {{
                            subtitleOverlay.style.display = 'none';
                        }}, 200);
                    }}
                }}
            }}
        }}

        function toggleSubtitleOverlay() {{
            subtitleOverlayEnabled = !subtitleOverlayEnabled;
            const toggleButton = document.getElementById('subtitle-toggle');
            const overlay = document.getElementById('subtitle-overlay');
            
            if (subtitleOverlayEnabled) {{
                toggleButton.innerHTML = '🔊 {get_text("hide_video_subtitles")}';
                toggleButton.style.background = '#dc3545';
                // Show current subtitle if any
                if (currentSubtitleIndex !== -1 && subtitles[currentSubtitleIndex]) {{
                    overlay.textContent = subtitles[currentSubtitleIndex].text;
                    overlay.style.display = 'block';
                    overlay.style.opacity = '1';
                }}
            }} else {{
                toggleButton.innerHTML = '🔇 {get_text("show_video_subtitles")}';
                toggleButton.style.background = '#007bff';
                overlay.style.opacity = '0';
                setTimeout(() => {{
                    overlay.style.display = 'none';
                }}, 200);
            }}
        }}
        
                function findCurrentSubtitle(subtitleArray, currentTime) {{
            return subtitleArray.find(subtitle => 
                currentTime >= subtitle.start && currentTime <= subtitle.end
            );
        }}
        
        function formatTime(seconds) {{
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {{
                return `${{hours}}:${{minutes.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }} else {{
                return `${{minutes}}:${{secs.toString().padStart(2, '0')}}`;
            }}
        }}
        
        // Add CSS for smooth transitions and responsive design
        const style = document.createElement('style');
        style.textContent = `
            #subtitle-overlay {{
                transition: opacity 0.2s ease-in-out;
                max-width: 90vw !important;
                white-space: nowrap !important;
                overflow: visible !important;
                box-sizing: border-box !important;
            }}
            #current-subtitle-status {{
                transition: color 0.3s ease;
            }}
            
            /* Responsive subtitle font size and width */
            @media (max-width: 768px) {{
                #subtitle-overlay {{
                    font-size: 16px !important;
                    padding: 6px 10px !important;
                    max-width: 95vw !important;
                    white-space: nowrap !important;
                }}
            }}
            
            @media (min-width: 1200px) {{
                #subtitle-overlay {{
                    font-size: 20px !important;
                    max-width: 85vw !important;
                    white-space: nowrap !important;
                }}
            }}
        `;
        document.head.appendChild(style);
        
        // Initialize when page loads
        loadYouTubeAPI();
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {{
            if (updateInterval) clearInterval(updateInterval);
        }});
    </script>
    """
    
    return html_code

def render_setup_interface():
    """Render the setup interface for video input and translation configuration."""
    # Main title
    st.markdown(f"<h1 class='main-header'>🎬 {get_text('page_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>{get_text('page_description')}</p>", unsafe_allow_html=True)
    
    # Sidebar information
    with st.sidebar:
        st.markdown(f"### 🛠️ {get_text('features')}")
        st.markdown(get_text("features_list"))
        
        st.markdown(f"### ℹ️ {get_text('usage_instructions')}")
        st.markdown(get_text("usage_list"))

    # Main interface - centered container for form elements
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Video link input
        st.markdown(f"### 📺 {get_text('video_link')}")
        video_url = st.text_input(
            get_text("video_link_placeholder"),
            placeholder="https://www.youtube.com/watch?v=...",
            help=get_text("video_link_help")
        )
        
        if video_url:
            # Validate URL and extract video ID
            video_id = extract_video_id(video_url)
            if video_id:
                # Display video
                st.markdown(f"### 🎥 {get_text('video_preview')}")
                st.video(video_url)
                
                # Get available languages
                with st.spinner(f"🔍 {get_text('getting_languages')}"):
                    try:
                        available_languages = list_available_languages.invoke({"video_url": video_url})
                        
                        if available_languages:
                            st.success(get_text("found_languages", count=len(available_languages)))
                            
                            # Language selection area
                            st.markdown(f"### 🌐 {get_text('language_settings')}")
                            
                            col_source, col_target = st.columns(2)
                            
                            with col_source:
                                # Source language selection
                                language_options = {}
                                for lang in available_languages:
                                    display_name = f"{lang['name']} ({lang['code']})"
                                    if lang.get('is_generated'):
                                        display_name += f" [{get_text('auto_generated')}]"
                                    language_options[display_name] = lang['code']
                                
                                selected_source_display = st.selectbox(
                                    get_text("source_language"),
                                    options=list(language_options.keys()),
                                    help=get_text("source_language_help")
                                )
                                selected_source_code = language_options[selected_source_display]
                            
                            with col_target:
                                # Target language selection
                                target_languages = {
                                    "Simplified Chinese": "zh-CN",
                                    "Traditional Chinese": "zh-TW", 
                                    "English": "en",
                                    "Japanese": "ja",
                                    "Korean": "ko",
                                    "French": "fr",
                                    "German": "de",
                                    "Spanish": "es",
                                    "Russian": "ru",
                                    "Italian": "it",
                                    "Portuguese": "pt"
                                }
                                
                                selected_target_display = st.selectbox(
                                    get_text("target_language"), 
                                    options=list(target_languages.keys()),
                                    index=2,  # Default to English
                                    help=get_text("target_language_help")
                                )
                                selected_target_code = target_languages[selected_target_display]
                            
                            # Model selection area
                            st.markdown(f"### {get_text('model_settings')}")
                            
                            # OpenAI model options
                            openai_models = {
                                "GPT-4o": "gpt-4o",
                                "GPT-4o mini": "gpt-4o-mini",
                                "GPT-4 Turbo": "gpt-4-turbo",
                                "GPT-4": "gpt-4",
                                "GPT-4.1": "gpt-4.1",
                                "GPT-3.5 Turbo": "gpt-3.5-turbo",
                                "o1 Preview": "o1-preview",
                                "o1 Mini": "o1-mini",
                                "o3 Mini": "o3-mini"
                            }
                            
                            # Function to get display name from model code
                            def get_model_display_name(model_code):
                                for display_name, code in openai_models.items():
                                    if code == model_code:
                                        return display_name
                                return "o3 Mini"  # fallback
                            
                            # Get default indices based on .env settings
                            default_extraction_display = get_model_display_name(EXTRACTION_MODEL_NAME)
                            default_translation_display = get_model_display_name(TRANSLATION_MODEL_NAME)
                            default_context_display = get_model_display_name(CONTEXT_MODEL_NAME)
                            default_extraction_index = list(openai_models.keys()).index(default_extraction_display)
                            default_translation_index = list(openai_models.keys()).index(default_translation_display)
                            default_context_index = list(openai_models.keys()).index(default_context_display)
                            
                            col_extract_model, col_context_model, col_translate_model = st.columns(3)
                            
                            with col_extract_model:
                                selected_extraction_display = st.selectbox(
                                    get_text("extraction_model"),
                                    options=list(openai_models.keys()),
                                    index=default_extraction_index,  # Use .env default
                                    help=get_text("extraction_model_help")
                                )
                                selected_extraction_model = openai_models[selected_extraction_display]
                            
                            with col_context_model:
                                selected_context_display = st.selectbox(
                                    get_text("context_model"),
                                    options=list(openai_models.keys()),
                                    index=default_context_index,  # Use .env default
                                    help=get_text("context_model_help")
                                )
                                selected_context_model = openai_models[selected_context_display]
                            
                            with col_translate_model:
                                selected_translation_display = st.selectbox(
                                    get_text("translation_model"),
                                    options=list(openai_models.keys()),
                                    index=default_translation_index,  # Use .env default
                                    help=get_text("translation_model_help")
                                )
                                selected_translation_model = openai_models[selected_translation_display]
                            
                            # Translation button and processing
                            st.markdown(f"### 🚀 {get_text('start_translation')}")
                            
                            if st.button(f"🎯 {get_text('start_button')}", type="primary", use_container_width=True):
                                # Store translation settings in session state
                                st.session_state.translation_settings = {
                                    'video_url': video_url,
                                    'video_id': video_id,
                                    'source_language_code': selected_source_code,
                                    'target_language': selected_target_code,
                                    'extraction_model': selected_extraction_model,
                                    'translation_model': selected_translation_model,
                                    'context_model': selected_context_model,
                                    'source_display': selected_source_display,
                                    'target_display': selected_target_display,
                                    'extraction_display': selected_extraction_display,
                                    'translation_display': selected_translation_display,
                                    'context_display': selected_context_display
                                }
                                
                                # Create progress container
                                progress_container = st.container()
                                
                                with progress_container:
                                    # Initialize progress bar
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    
                                    try:
                                        # Call our modified translation function with progress callback
                                        result = translate_video_api(
                                            video_url=video_url,
                                            source_language_code=selected_source_code,
                                            target_language=selected_target_code,
                                            extraction_model=selected_extraction_model,
                                            translation_model=selected_translation_model,
                                            context_model=selected_context_model,
                                            progress_callback=lambda step, progress, message: (
                                                progress_bar.progress(progress),
                                                status_text.text(f"🔄 {message}")
                                            )
                                        )
                                        
                                        # Handle different completion scenarios
                                        if result and "final_srt_path" in result:
                                            # Check if result came from cache
                                            if result.get("from_cache", False):
                                                progress_bar.progress(100)
                                                status_text.text(f"⚡ {get_text('cache_found')}")
                                                st.success(f"🎯 {get_text('cache_found')}")
                                            else:
                                                progress_bar.progress(100)
                                                status_text.text(f"✅ {get_text('translation_completed')}")
                                            
                                            # Store translation result in session state
                                            st.session_state.translation_result = result
                                            
                                            # Switch to player mode
                                            st.session_state.page_mode = 'player'
                                            
                                            # Force page refresh to show player interface
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {get_text('translation_error')}")
                                            
                                    except Exception as e:
                                        progress_bar.progress(0)
                                        status_text.text(f"❌ {get_text('translation_failed')}")
                                        st.error(get_text("error_occurred", error=str(e)))
                                        
                                        # Display detailed error information (for debugging)
                                        with st.expander(f"🔍 {get_text('error_details')}", expanded=False):
                                            st.code(traceback.format_exc())
                        else:
                            st.warning(f"⚠️ {get_text('no_subtitles')}")
                            
                    except Exception as e:
                        st.error(get_text("failed_get_languages", error=str(e)))
                        with st.expander(f"🔍 {get_text('error_details')}", expanded=False):
                            st.code(traceback.format_exc())
                            
            else:
                st.error(f"❌ {get_text('invalid_url')}")

def render_player_interface():
    """Render the video player interface with subtitle controls."""
    # Add CSS class for player mode
    st.markdown('<div class="player-mode">', unsafe_allow_html=True)
    
    # Header with back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔙 " + get_text('new_translation'), type="secondary"):
            # Clear session state and return to setup
            st.session_state.page_mode = 'setup'
            if 'translation_result' in st.session_state:
                del st.session_state.translation_result
            if 'translation_settings' in st.session_state:
                del st.session_state.translation_settings
            st.rerun()
    
    with col2:
        st.markdown(f"<h1 class='main-header'>🎬 {get_text('video_player')}</h1>", unsafe_allow_html=True)
    
    # Success message
    st.success(f"🎉 {get_text('task_completed')}")
    
    # Get data from session state
    settings = st.session_state.translation_settings
    result = st.session_state.translation_result
    
    # Read translated subtitle file
    final_srt_path = result["final_srt_path"]
    if os.path.exists(final_srt_path):
        with open(final_srt_path, 'r', encoding='utf-8') as f:
            translated_content = f.read()
        
        # Parse subtitles for video player
        parsed_subtitles = parse_srt_content(translated_content)
        
        # Display video player (full width)
        if parsed_subtitles:
            # Create player HTML
            player_html = create_video_player_with_subtitles(
                settings['video_url'], 
                settings['video_id'], 
                parsed_subtitles
            )
            
            # Display player with full container width
            st.components.v1.html(
                player_html, 
                height=800,
                scrolling=False
            )
        else:
            st.warning("⚠️ Unable to parse subtitles for video player")

        # Control area below player
        col1, col2 = st.columns(2)

        with col1:
            # Subtitle preview
            st.markdown(f"### 📝 {get_text('subtitle_preview')}")
            with st.expander("View Subtitle Content", expanded=False):
                st.text_area(
                    get_text("translated_content"),
                    value=translated_content,
                    height=300,
                    disabled=True
                )

        with col2:
            # Download and statistics
            st.markdown(f"### 📥 {get_text('download_button')}")
            
            filename = f"translated_{settings['target_language']}_{settings['video_id']}.srt"
            st.download_button(
                label=f"📥 {get_text('download_button')}",
                data=translated_content,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )
            
            # Statistics
            if "translated_sub_list" in result:
                total_subtitles = len(result["translated_sub_list"])
                st.info(get_text("translated_count", count=total_subtitles))
            
            st.markdown("**File Information:**")
            st.write(f"- Subtitle entries: {len(parsed_subtitles) if parsed_subtitles else 0}")
            st.write(f"- Source: {settings['source_display']}")
            st.write(f"- Target: {settings['target_display']}")
            
            # Show cache status if available
            if result.get("from_cache", False):
                st.write(f"- Status: ⚡ {get_text('loaded_from_cache')}")
            else:
                st.write(f"- Status: 🔄 {get_text('freshly_translated')}")
                st.write(f"- Extract Model: {settings['extraction_display']}")
                st.write(f"- Context Model: {settings['context_display']}")
                st.write(f"- Translate Model: {settings['translation_display']}")
    else:
        st.error(f"❌ {get_text('file_not_found')}")
    
    # Close player mode div
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """
    Main application entry point.
    
    Initializes the Streamlit application, manages session state,
    and routes between setup and player interfaces based on user progress.
    """
    # Initialize session state
    if 'page_mode' not in st.session_state:
        st.session_state.page_mode = 'setup'
    
    # Language selector at the top
    language_selector()
    
    # Render appropriate interface based on current mode
    if st.session_state.page_mode == 'setup':
        render_setup_interface()
    elif st.session_state.page_mode == 'player':
        render_player_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<p style='text-align: center; color: #888;'>{get_text('footer')} | "
        "<a href='https://github.com/tigerkidyang/llm-youtube-sub-translation-agent' target='_blank'>GitHub</a></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 