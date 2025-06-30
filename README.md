<div align="center">
  <h1>🎬 YouTube Subtitle AI Translator 🌍</h1>
  <p>
    An advanced AI-powered web application for high-quality, context-aware translation of YouTube video subtitles with real-time video player integration.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Read this README in other languages:
    <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

This project provides a sophisticated web-based application for translating YouTube video subtitles using advanced AI technology. Built with Streamlit and powered by LangGraph, it offers an intuitive interface with real-time video playback, synchronized subtitle display, and intelligent caching for optimal performance.

## 🌟 Key Features

### 🎥 **Interactive Video Experience**

- **Embedded YouTube Player**: Watch videos directly in the app with synchronized subtitles
- **Subtitle Overlay Control**: Toggle video overlay subtitles on/off with one click
- **Real-time Synchronization**: Subtitles automatically sync with video playback
- **Full-screen Support**: Optimized player experience for all screen sizes

### 🧠 **AI-Powered Translation**

- **Context-Aware Processing**: Generates comprehensive translation memory including glossary, speaker analysis, and style guidelines
- **Chunk-Based Translation**: Intelligently processes subtitles in manageable segments for accuracy
- **Quality Validation**: Automatic format checking and retry mechanisms for reliable output
- **Multiple AI Models**: Configurable models for extraction, context generation, and translation

### 🚀 **Performance & Reliability**

- **Smart Caching**: Automatically detects and reuses existing translations
- **Dual Extraction Methods**: Primary youtube-transcript-api with yt-dlp fallback
- **Progress Tracking**: Real-time translation progress with detailed status updates
- **Error Recovery**: Robust error handling with graceful fallbacks

### 🌍 **Multi-language Support**

- **Internationalized Interface**: 11 supported UI languages
- **Automatic Language Detection**: Discovers all available subtitle languages
- **Wide Translation Support**: Translate to any language supported by the AI models

### 📁 **File Management**

- **Automatic Organization**: Smart file naming and storage in dedicated folders
- **SRT Format**: Industry-standard subtitle format for maximum compatibility
- **One-click Download**: Easy access to translated subtitle files

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (required for AI translation)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Quick Start

**1. Clone the Repository**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Environment**

Create a `.env` file in the project root with your OpenAI API key:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional configurations (with defaults shown)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Launch the Application**

```bash
python run_streamlit.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

## 🎯 How to Use

### Basic Workflow

1. **Start the Application**: Run `python run_streamlit.py`
2. **Enter Video URL**: Paste any YouTube video link
3. **Select Languages**: Choose source and target languages from detected options
4. **Configure Models** (Optional): Select AI models for different processing stages
5. **Start Translation**: Click "Start AI Translation" and monitor progress
6. **Watch & Download**: Enjoy the translated video with synchronized subtitles and download files

### Advanced Features

#### Model Selection

- **Extraction Model**: Handles subtitle downloading and preprocessing
- **Context Model**: Generates translation memory and guidelines
- **Translation Model**: Performs the actual translation work

#### Caching System

- Automatically detects existing translations
- Instant loading for previously translated videos
- Smart cache invalidation and management

#### Multi-language Interface

- Switch between 11 supported interface languages
- Persistent language preferences
- Localized error messages and help text

## 🏗️ Architecture Overview

### Core Components

- **`streamlit_app.py`**: Main web interface and user interaction logic
- **`Agent.py`**: LangGraph-based translation workflow engine
- **`get_sub.py`**: Subtitle extraction with dual-source fallback
- **`prompts.py`**: Carefully crafted AI prompts for optimal translation
- **`languages.py`**: Complete internationalization support
- **`run_streamlit.py`**: Application launcher with dependency checking

### Translation Workflow

1. **URL Processing**: Extract video ID and validate accessibility
2. **Language Discovery**: Detect all available subtitle languages
3. **Cache Check**: Look for existing translations to avoid duplicate work
4. **Subtitle Extraction**: Download original subtitles with fallback mechanisms
5. **Context Generation**: Create comprehensive translation memory
6. **Chunked Translation**: Process subtitles in optimized segments
7. **Quality Validation**: Verify translation format and retry if needed
8. **Output Generation**: Create final SRT file and display results

### Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **AI Framework**: LangGraph (Workflow orchestration)
- **AI Models**: OpenAI GPT models (Configurable)
- **Subtitle APIs**: youtube-transcript-api + yt-dlp (Dual fallback)
- **File Processing**: Python standard library + custom parsers

## ⚙️ Configuration

### Environment Variables

| Variable                        | Description                      | Default       |
| ------------------------------- | -------------------------------- | ------------- |
| `OPENAI_API_KEY`                | OpenAI API key (required)        | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Directory for subtitle files     | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Subtitle processing chunk size   | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Maximum retry attempts           | `2`           |
| `EXTRACTION_MODEL`              | AI model for subtitle extraction | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | AI model for translation         | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | AI model for context generation  | `o3-mini`     |

## 🔧 Troubleshooting

### Common Issues

**Application won't start**

- Verify Python version (3.9+)
- Check all dependencies are installed
- Ensure OpenAI API key is configured

**Translation fails**

- Verify OpenAI API key is valid and has credits
- Check internet connection
- Try different AI models if rate-limited

**Subtitles not found**

- Verify the video has available subtitles
- Try different language options
- Check if video is publicly accessible

**Interface language issues**

- Clear browser cache and refresh
- Check browser language settings
- Try selecting language manually from dropdown

### Performance Optimization

- Use faster AI models for large videos
- Enable caching for frequently translated content
- Close other applications to free up system resources
- Use wired internet connection for stability

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**: Click the "Fork" button on GitHub
2. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Verify all functionality works
5. **Submit Pull Request**: Create a detailed PR with description

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Add comprehensive docstrings to new functions
- Update documentation for new features
- Test with various video types and languages
- Maintain backward compatibility when possible

### Areas for Contribution

- Additional subtitle format support (VTT, ASS, etc.)
- New AI model integrations
- Performance optimizations
- Additional language support
- UI/UX improvements
- Mobile responsiveness enhancements

## 📊 Project Statistics

- **Lines of Code**: ~3,200
- **Supported UI Languages**: 11
- **AI Models Supported**: 5+
- **Subtitle Formats**: SRT (with more planned)
- **Fallback Systems**: 2 (youtube-transcript-api + yt-dlp)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For providing powerful language models
- **Streamlit**: For the excellent web application framework
- **LangGraph**: For robust workflow orchestration
- **YouTube Transcript API**: For subtitle access
- **yt-dlp**: For reliable video data extraction
- **Open Source Community**: For continuous inspiration and support

---

<div align="center">
  <p>Made with ❤️ for the global community</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Star this project</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Report Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Request Feature</a>
  </p>
</div>
