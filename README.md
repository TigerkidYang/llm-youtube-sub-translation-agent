<div align="center">
  <h1>🎬 LLM YouTube Subtitle Translation Agent 🌍</h1>
  <p>
    An advanced AI agent for high-quality, context-aware translation of YouTube video subtitles using LangGraph.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Read this README in other languages:
    [简体中文](README_zh.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Français](README_fr.md) | [Deutsch](README_de.md) | [Español](README_es.md) | [Português](README_pt.md) | [Italiano](README_it.md) | [Русский](README_ru.md)
  </p>
</div>

This project implements an advanced, multi-step AI agent that automates the translation of YouTube video subtitles. It uses the LangGraph framework to create a robust and intelligent pipeline that goes beyond simple translation to ensure contextual consistency and high quality.

The agent first fetches the subtitles, analyzes the full text to generate a "translation memory" (including a glossary and style guide), and then translates the content chunk by chunk, validating each output before finalizing the result into a new `.srt` file.

## 📖 Table of Contents

- [✨ Key Features](#-key-features)
- [🚀 How It Works: The Agent Workflow](#-how-it-works-the-agent-workflow)
- [🛠️ Setup and Installation](#️-setup-and-installation)
- [🏃 How to Run](#-how-to-run)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Key Features

-   **Interactive Setup**: 🗣️ Prompts the user for the YouTube video link and desired original/target languages.
-   **Context-Aware Translation**: 🧠 Before translating, the agent generates a comprehensive context guide (video basis, glossary, voice descriptions, and style tips) to ensure high-quality, consistent translations.
-   **Chunk-Based Processing**: 🧩 Splits subtitles into manageable chunks for efficient and reliable processing by the language model.
-   **Robust and Self-Correcting**: 💪 Includes a validation step that checks the LLM's translated output for formatting errors (like unwanted markdown) and automatically retries with corrective instructions.
-   **Stateful Workflow**: 🔄 Built with `langgraph` to manage the complex, multi-step process in a clear, resilient, and observable way.
-   **Automatic File Management**: 📂 Intelligently names and saves both the original and final translated `.srt` files in a dedicated `transcripts` directory.

## 🚀 How It Works: The Agent Workflow

The agent operates as a state machine, moving through a series of defined steps to complete the translation task.

1.  **Get Video Link**: 🔗 The agent starts by asking the user for a YouTube video URL.
2.  **List Available Languages**: 📜 It calls the YouTube Transcript API to find all available subtitle languages for the video and displays them.
3.  **Get Language Choices**: 🎯 The user selects the original subtitle language to translate from and specifies the target language.
4.  **Fetch Subtitles**: 📥 An LLM-powered tool agent is invoked. It correctly calls the `fetch_youtube_srt` tool to download the original subtitles and saves them as an `.srt` file (e.g., `transcripts/video_id_en.srt`).
5.  **Prepare for Translation**: ⚙️ The downloaded `.srt` file is parsed and its content is split into smaller, numbered text chunks based on the `CHUNK_SIZE`.
6.  **Generate Translation Context**: 💡 The agent sends the *entire* original subtitle text to an LLM to generate a "translation memory." This critical document contains a glossary of key terms, descriptions of the speakers' voices and tones, and translation tips to ensure consistency.
7.  **Translate Chunks (Loop)**: 🔁 The agent iterates through each chunk of text.
    a.  **Translate**: The current chunk is sent to the LLM for translation, along with the translation memory for context.
    b.  **Validate**: The LLM's output is checked for correctness. Specifically, it ensures the output is plain text and not wrapped in markdown code blocks. If validation fails, the agent retries the translation up to a defined maximum.
    c.  **Aggregate**: The validated, translated text is added to a list. If a chunk repeatedly fails validation, the original text is used as a placeholder to prevent data loss.
8.  **Finalize Translation**: ✅ Once all chunks are translated, the agent reconstructs a complete, translated subtitle list, converts it back into the SRT format, and saves it to a new file (e.g., `transcripts/video_id_en_zh-CN.srt`).
9.  **End**: 🎉 The process is complete.

## 🛠️ Setup and Installation

**1. Clone the Repository**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Create a Python Virtual Environment**

It's highly recommended to use a virtual environment.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**

Install all the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**

The agent requires an API key and other configurations.

First, rename the example environment file `.env.example` to `.env`.

```bash
# For Windows
rename .env.example .env

# For macOS/Linux
mv .env.example .env
```

Next, open the new `.env` file and add your OpenAI API key. The file will also contain optional default values you can customize.

```env
# Required
OPENAI_API_KEY="your_openai_api_key_here"

# Optional: You can override these default values
# I have comments in .env.example to tell you what they are.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 How to Run

Execute the `Agent.py` script from your terminal. The agent will guide you through the process interactively.

```bash
python Agent.py
```

You will be prompted to enter the YouTube video link and then select the languages. The agent will display detailed logs in the console as it executes each step of the workflow. Once finished, you will find the original and translated `.srt` files in the `transcripts` directory.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or find any issues, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please make sure to update tests as appropriate.

## 📄 License

This project is licensed under the MIT License. You can find more details in the `LICENSE` file if one is included in the repository, or refer to the [MIT License terms](https://opensource.org/licenses/MIT).