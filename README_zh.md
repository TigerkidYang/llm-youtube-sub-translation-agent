<div align="center">
  <h1>🎬 LLM YouTube 字幕翻译代理 🌍</h1>
  <p>
    一个使用 LangGraph 构建的先进 AI 代理，用于高质量、具备上下文感知能力的 YouTube 视频字幕翻译。
  </p>
  <p>
    <!-- 徽章 -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="许可证: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="问题"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="欢迎 PR"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 阅读其他语言版本的 README：
    <a href="README.md">English</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

本项目实现了一个先进的多步骤 AI 代理，可自动翻译 YouTube 视频字幕。它使用 LangGraph 框架创建一个强大且智能的流程，超越了简单的翻译，以确保上下文一致性和高质量。

该代理首先获取字幕，分析全文以生成“翻译记忆”（包括词汇表和风格指南），然后逐块翻译内容，在最终将结果输出到新的 `.srt` 文件之前验证每个输出。

## 📖 目录

- [✨ 主要功能](#-主要功能)
- [🚀 工作原理：代理工作流程](#-工作原理代理工作流程)
- [🛠️ 快速入门](#️-快速入门)
- [🏃 如何运行](#-如何运行)
- [🤝 如何贡献](#-如何贡献)
- [📄 许可证](#-许可证)

## ✨ 主要功能

-   **交互式设置**：🗣️ 提示用户输入 YouTube 视频链接以及期望的源语言和目标语言。
-   **上下文感知翻译**：🧠 在翻译之前，代理会生成一个全面的上下文指南（视频基础、词汇表、语音描述和风格提示），以确保高质量、一致的翻译。
-   **分块处理**：🧩 将字幕分割成易于管理的小块，以便语言模型高效可靠地处理。
-   **稳健且自我修正**：💪 包含一个验证步骤，检查 LLM 翻译输出的格式错误（如不需要的 Markdown 标记）并自动使用修正指令重试。
-   **状态化工作流**：🔄 使用 `langgraph` 构建，以清晰、有弹性且可观察的方式管理复杂的多步骤过程。
-   **自动文件管理**：📂 智能地命名并在专用的 `transcripts` 目录中保存原始和最终翻译的 `.srt` 文件。

## 🚀 工作原理：代理工作流程

代理作为一个状态机运行，通过一系列定义的步骤来完成翻译任务。

1.  **获取视频链接**：🔗 代理首先要求用户提供 YouTube 视频 URL。
2.  **列出可用语言**：📜 它调用 YouTube Transcript API 查找视频所有可用的字幕语言并显示它们。
3.  **获取语言选择**：🎯 用户选择要翻译的原始字幕语言并指定目标语言。
4.  **获取字幕**：📥 调用一个由 LLM 驱动的工具代理。它正确调用 `fetch_youtube_srt` 工具下载原始字幕并将其保存为 `.srt` 文件（例如 `transcripts/video_id_en.srt`）。
5.  **准备翻译**：⚙️ 解析下载的 `.srt` 文件，并根据 `CHUNK_SIZE` 将其内容分割成带编号的小文本块。
6.  **生成翻译上下文**：💡 代理将*完整*的原始字幕文本发送给 LLM 以生成“翻译记忆”。这份关键文档包含关键术语词汇表、说话者语音和语气的描述以及确保一致性的翻译提示。
7.  **翻译文本块（循环）**：🔁 代理遍历每个文本块。  
    a.  **翻译**：将当前文本块连同翻译记忆一起发送给 LLM 进行翻译，以提供上下文。  
    b.  **验证**：检查 LLM 输出的正确性。具体来说，它确保输出是纯文本，并且没有被 Markdown 代码块包裹。如果验证失败，代理会在定义的最大次数内重试翻译。  
    c.  **聚合**：将经过验证的翻译文本添加到列表中。如果某个文本块反复验证失败，则使用原始文本作为占位符以防止数据丢失。  
8.  **完成翻译**：✅ 一旦所有文本块都翻译完毕，代理会重建一个完整的翻译字幕列表，将其转换回 SRT 格式，并保存到一个新文件（例如 `transcripts/video_id_en_zh-CN.srt`）。
9.  **结束**：🎉 过程完成。

## 🛠️ 快速入门

**1. 克隆仓库**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 创建 Python 虚拟环境**

强烈建议使用虚拟环境。

```bash
# Windows 系统
python -m venv venv
venv\Scripts\activate

# macOS/Linux 系统
python3 -m venv venv
source venv/bin/activate
```

**3. 安装依赖**

从 `requirements.txt` 文件安装所有必需的 Python 包。

```bash
pip install -r requirements.txt
```

**4. 配置环境变量**

代理需要 API 密钥和其他配置。

首先，将示例环境文件 `.env.example` 重命名为 `.env`。

```bash
# Windows 系统
rename .env.example .env

# macOS/Linux 系统
mv .env.example .env
```

接下来，打开新的 `.env` 文件并添加您的 OpenAI API 密钥。该文件还将包含您可以自定义的可选默认值。

```env
# 必填
OPENAI_API_KEY="your_openai_api_key_here" # 请替换为您的 OpenAI API 密钥

# 可选：您可以覆盖这些默认值
# .env.example 文件中有关于这些参数的注释说明。
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 如何运行

从您的终端执行 `Agent.py` 脚本。代理将以交互方式引导您完成整个过程。

```bash
python Agent.py
```

系统将提示您输入 YouTube 视频链接，然后选择语言。代理在执行工作流程的每一步时，都会在控制台中显示详细的日志。完成后，您将在 `transcripts` 目录中找到原始和翻译后的 `.srt` 文件。

---

## 🤝 如何贡献

欢迎贡献！如果您有改进建议或发现任何问题，请随时：

1.  Fork 本仓库。
2.  创建一个新分支 (`git checkout -b feature/your-feature-name`)。
3.  进行更改。
4.  提交您的更改 (`git commit -m 'Add some feature'`)。
5.  将分支推送到远程仓库 (`git push origin feature/your-feature-name`)。
6.  创建一个 Pull Request。

请确保酌情更新测试。

## 📄 许可证

本项目采用 MIT 许可证。如果仓库中包含 `LICENSE` 文件，您可以在其中找到更多详细信息，或参考 [MIT 许可证条款](https://opensource.org/licenses/MIT)。
