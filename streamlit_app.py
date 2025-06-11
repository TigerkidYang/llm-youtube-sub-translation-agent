import streamlit as st
import os
import sys
from typing import Dict, List
import tempfile
import traceback

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_sub import list_available_languages
from Agent import translate_video_api

# Page configuration
st.set_page_config(
    page_title="YouTube Subtitle AI Translator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styles
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    import re
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

def main():
    # Main title
    st.markdown("<h1 class='main-header'>🎬 YouTube Subtitle AI Translator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>High-quality AI-powered YouTube video subtitle translation tool</p>", unsafe_allow_html=True)
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 🛠️ Features")
        st.markdown("""
        - 🧠 AI context-aware translation
        - 🎯 Terminology consistency guarantee
        - 📝 Multiple subtitle format support
        - 🚀 Intelligent chunk processing
        - ✅ Automatic format validation
        - 🔄 yt-dlp fallback solution
        """)
        
        st.markdown("### ℹ️ Usage Instructions")
        st.markdown("""
        1. Enter YouTube video link
        2. Select source subtitle language
        3. Select target translation language
        4. Click start translation
        5. Download translation results
        """)

    # Main interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Video link input
        st.markdown("### 📺 YouTube Video Link")
        video_url = st.text_input(
            "Please enter YouTube video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Supports various YouTube link formats"
        )
        
        if video_url:
            # Validate URL and extract video ID
            video_id = extract_video_id(video_url)
            if video_id:
                # Display video
                st.markdown("### 🎥 Video Preview")
                st.video(video_url)
                
                # Get available languages
                with st.spinner("🔍 Getting available subtitle languages... (will automatically try fallback if issues occur)"):
                    try:
                        available_languages = list_available_languages.invoke({"video_url": video_url})
                        
                        if available_languages:
                            st.success(f"✅ Found {len(available_languages)} available subtitle languages")
                            
                            # Language selection area
                            st.markdown("### 🌐 Language Settings")
                            
                            col_source, col_target = st.columns(2)
                            
                            with col_source:
                                # Source language selection
                                language_options = {}
                                for lang in available_languages:
                                    display_name = f"{lang['name']} ({lang['code']})"
                                    if lang.get('is_generated'):
                                        display_name += " [Auto-generated]"
                                    language_options[display_name] = lang['code']
                                
                                selected_source_display = st.selectbox(
                                    "Source Subtitle Language",
                                    options=list(language_options.keys()),
                                    help="Select the source subtitle language to translate"
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
                                    "Target Translation Language", 
                                    options=list(target_languages.keys()),
                                    index=2,  # Default to English
                                    help="Select the target language to translate to"
                                )
                                selected_target_code = target_languages[selected_target_display]
                            
                            # Translation button and processing
                            st.markdown("### 🚀 Start Translation")
                            
                            if st.button("🎯 Start AI Translation", type="primary", use_container_width=True):
                                # Create progress container
                                progress_container = st.container()
                                
                                with progress_container:
                                    # Initialize progress bar
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    
                                    try:
                                        # Display start status
                                        status_text.text("🔄 Initializing translation task...")
                                        progress_bar.progress(10)
                                        
                                        # Call translation API
                                        status_text.text("📥 Downloading original subtitles... (using youtube-transcript-api, will auto-switch to yt-dlp if failed)")
                                        progress_bar.progress(20)
                                        
                                        # Call our modified translation function
                                        result = translate_video_api(
                                            video_url=video_url,
                                            source_language_code=selected_source_code,
                                            target_language=selected_target_code,
                                            progress_callback=lambda step, progress, message: (
                                                progress_bar.progress(progress),
                                                status_text.text(f"🔄 {message}")
                                            )
                                        )
                                        
                                        # Completion status
                                        progress_bar.progress(100)
                                        status_text.text("✅ Translation completed!")
                                        
                                        if result and "final_srt_path" in result:
                                            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                                            st.success("🎉 Translation task completed!")
                                            st.markdown("</div>", unsafe_allow_html=True)
                                            
                                            # Read translated subtitle file
                                            final_srt_path = result["final_srt_path"]
                                            if os.path.exists(final_srt_path):
                                                with open(final_srt_path, 'r', encoding='utf-8') as f:
                                                    translated_content = f.read()
                                                
                                                # Display subtitle preview
                                                with st.expander("📝 Subtitle Preview", expanded=False):
                                                    st.text_area(
                                                        "Translated subtitle content",
                                                        value=translated_content[:1000] + ("..." if len(translated_content) > 1000 else ""),
                                                        height=200,
                                                        disabled=True
                                                    )
                                                
                                                # Download button
                                                filename = f"translated_{selected_target_code}_{video_id}.srt"
                                                st.download_button(
                                                    label="📥 Download Translated Subtitle File",
                                                    data=translated_content,
                                                    file_name=filename,
                                                    mime="text/plain",
                                                    use_container_width=True
                                                )
                                                
                                                # Display statistics
                                                if "translated_sub_list" in result:
                                                    total_subtitles = len(result["translated_sub_list"])
                                                    st.info(f"📊 Translated {total_subtitles} subtitle entries")
                                            else:
                                                st.error("❌ Translation file not found")
                                        else:
                                            st.error("❌ Error occurred during translation process")
                                            
                                    except Exception as e:
                                        progress_bar.progress(0)
                                        status_text.text("❌ Translation failed")
                                        st.error(f"Error occurred during translation: {str(e)}")
                                        
                                        # Display detailed error information (for debugging)
                                        with st.expander("🔍 Error Details", expanded=False):
                                            st.code(traceback.format_exc())
                        else:
                            st.warning("⚠️ This video has no available subtitles")
                            
                    except Exception as e:
                        st.error(f"❌ Failed to get subtitle languages: {str(e)}")
                        with st.expander("🔍 Error Details", expanded=False):
                            st.code(traceback.format_exc())
                            
            else:
                st.error("❌ Invalid YouTube link, please check URL format")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>Built with LangGraph + OpenAI | "
        "<a href='https://github.com/tigerkidyang/llm-youtube-sub-translation-agent' target='_blank'>GitHub</a></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 