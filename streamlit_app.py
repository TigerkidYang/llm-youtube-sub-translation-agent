import streamlit as st
import os
import sys
from typing import Dict, List
import tempfile
import traceback

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_sub import list_available_languages
from Agent import translate_video_api, EXTRACTION_MODEL_NAME, TRANSLATION_MODEL_NAME
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
    # Language selector at the top
    language_selector()
    
    # Main title
    st.markdown(f"<h1 class='main-header'>🎬 {get_text('page_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>{get_text('page_description')}</p>", unsafe_allow_html=True)
    
    # Sidebar information
    with st.sidebar:
        st.markdown(f"### 🛠️ {get_text('features')}")
        st.markdown(get_text("features_list"))
        
        st.markdown(f"### ℹ️ {get_text('usage_instructions')}")
        st.markdown(get_text("usage_list"))

    # Main interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
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
                            default_extraction_index = list(openai_models.keys()).index(default_extraction_display)
                            default_translation_index = list(openai_models.keys()).index(default_translation_display)
                            
                            col_extract_model, col_translate_model = st.columns(2)
                            
                            with col_extract_model:
                                selected_extraction_display = st.selectbox(
                                    get_text("extraction_model"),
                                    options=list(openai_models.keys()),
                                    index=default_extraction_index,  # Use .env default
                                    help=get_text("extraction_model_help")
                                )
                                selected_extraction_model = openai_models[selected_extraction_display]
                            
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
                                # Create progress container
                                progress_container = st.container()
                                
                                with progress_container:
                                    # Initialize progress bar
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    
                                    try:
                                        # Display start status
                                        status_text.text(f"🔄 {get_text('initializing')}")
                                        progress_bar.progress(10)
                                        
                                        # Call translation API
                                        status_text.text(f"📥 {get_text('downloading')}")
                                        progress_bar.progress(20)
                                        
                                        # Call our modified translation function
                                        result = translate_video_api(
                                            video_url=video_url,
                                            source_language_code=selected_source_code,
                                            target_language=selected_target_code,
                                            extraction_model=selected_extraction_model,
                                            translation_model=selected_translation_model,
                                            progress_callback=lambda step, progress, message: (
                                                progress_bar.progress(progress),
                                                status_text.text(f"🔄 {message}")
                                            )
                                        )
                                        
                                        # Completion status
                                        progress_bar.progress(100)
                                        status_text.text(f"✅ {get_text('translation_completed')}")
                                        
                                        if result and "final_srt_path" in result:
                                            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                                            st.success(f"🎉 {get_text('task_completed')}")
                                            st.markdown("</div>", unsafe_allow_html=True)
                                            
                                            # Read translated subtitle file
                                            final_srt_path = result["final_srt_path"]
                                            if os.path.exists(final_srt_path):
                                                with open(final_srt_path, 'r', encoding='utf-8') as f:
                                                    translated_content = f.read()
                                                
                                                # Display subtitle preview
                                                with st.expander(f"📝 {get_text('subtitle_preview')}", expanded=False):
                                                    st.text_area(
                                                        get_text("translated_content"),
                                                        value=translated_content[:1000] + ("..." if len(translated_content) > 1000 else ""),
                                                        height=200,
                                                        disabled=True
                                                    )
                                                
                                                # Download button
                                                filename = f"translated_{selected_target_code}_{video_id}.srt"
                                                st.download_button(
                                                    label=f"📥 {get_text('download_button')}",
                                                    data=translated_content,
                                                    file_name=filename,
                                                    mime="text/plain",
                                                    use_container_width=True
                                                )
                                                
                                                # Display statistics
                                                if "translated_sub_list" in result:
                                                    total_subtitles = len(result["translated_sub_list"])
                                                    st.info(get_text("translated_count", count=total_subtitles))
                                            else:
                                                st.error(f"❌ {get_text('file_not_found')}")
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

    # Footer
    st.markdown("---")
    st.markdown(
        f"<p style='text-align: center; color: #888;'>{get_text('footer')} | "
        "<a href='https://github.com/tigerkidyang/llm-youtube-sub-translation-agent' target='_blank'>GitHub</a></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 