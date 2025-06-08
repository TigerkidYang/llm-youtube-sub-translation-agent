<div align="center">
  <h1>🎬 LLM YouTube 字幕翻譯代理程式 🌍</h1>
  <p>
    一款使用 LangGraph 的進階 AI 代理程式，用於高品質、具上下文感知能力的 YouTube 影片字幕翻譯。
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
    🌐 閱讀其他語言版本的 README：
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | 繁體中文 | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

本專案實作了一個進階的多步驟 AI 代理程式，可自動翻譯 YouTube 影片字幕。它使用 LangGraph 框架建立一個強大且智慧的流程，不僅僅是簡單的翻譯，更能確保上下文的一致性和高品質。

代理程式首先擷取字幕，分析全文以產生「翻譯記憶」（包含詞彙表和風格指南），然後逐塊翻譯內容，並在將結果最終化為新的 `.srt` 檔案之前驗證每個輸出。

## 📖 目錄

- [✨ 主要功能](#-主要功能)
- [🚀 運作方式：代理程式工作流程](#-運作方式代理程式工作流程)
- [🛠️ 快速開始](#️-快速開始)
- [🏃 如何執行](#-如何執行)
- [🤝 如何貢獻](#-如何貢獻)
- [📄 授權條款](#-授權條款)

## ✨ 主要功能

-   **互動式設定**：🗣️ 提示使用者輸入 YouTube 影片連結以及所需的原始/目標語言。
-   **上下文感知翻譯**：🧠 在翻譯之前，代理程式會產生一份全面的上下文指南（影片基礎、詞彙表、語音描述和風格提示），以確保高品質、一致的翻譯。
-   **分塊處理**：🧩 將字幕分割成易於管理的小塊，以便語言模型高效可靠地處理。
-   **強大且自我修正**：💪 包含一個驗證步驟，檢查 LLM 翻譯輸出的格式錯誤（例如不必要的 markdown）並自動使用修正指令重試。
-   **狀態化工作流程**：🔄 使用 `langgraph` 建構，以清晰、彈性且可觀察的方式管理複雜的多步驟流程。
-   **自動檔案管理**：📂 智慧地命名並將原始和最終翻譯的 `.srt` 檔案儲存在專用的 `transcripts` 目錄中。

## 🚀 運作方式：代理程式工作流程

代理程式作為一個狀態機運作，透過一系列定義好的步驟來完成翻譯任務。

1.  **取得影片連結**：🔗 代理程式首先要求使用者提供 YouTube 影片網址。
2.  **列出可用語言**：📜 它呼叫 YouTube Transcript API 來尋找影片所有可用的字幕語言並顯示它們。
3.  **取得語言選擇**：🎯 使用者選擇要翻譯的原始字幕語言並指定目標語言。
4.  **擷取字幕**：📥 呼叫一個由 LLM 驅動的工具代理程式。它正確地呼叫 `fetch_youtube_srt` 工具來下載原始字幕並將其儲存為 `.srt` 檔案（例如 `transcripts/video_id_en.srt`）。
5.  **準備翻譯**：⚙️ 解析下載的 `.srt` 檔案，並根據 `CHUNK_SIZE` 將其內容分割成較小的、編號的文字塊。
6.  **產生翻譯上下文**：💡 代理程式將*完整*的原始字幕文字傳送給 LLM 以產生「翻譯記憶」。這份關鍵文件包含關鍵術語詞彙表、說話者語音和語氣的描述以及翻譯技巧，以確保一致性。
7.  **翻譯文字塊（循環）**：🔁 代理程式迭代處理每個文字塊。  
    a.  **翻譯**：將目前的文字塊連同翻譯記憶一起傳送給 LLM 進行翻譯，以提供上下文。  
    b.  **驗證**：檢查 LLM 的輸出是否正確。具體來說，它確保輸出是純文字，而不是用 markdown 程式碼區塊包裹。如果驗證失敗，代理程式會在定義的最大次數內重試翻譯。  
    c.  **彙總**：將已驗證的翻譯文字加入清單中。如果某個文字塊重複驗證失敗，則使用原始文字作為預留位置以防止資料遺失。  
8.  **完成翻譯**：✅ 所有文字塊翻譯完成後，代理程式會重建完整的翻譯字幕清單，將其轉換回 SRT 格式，並儲存到新檔案（例如 `transcripts/video_id_en_zh-TW.srt`）。
9.  **結束**：🎉 流程完成。

## 🛠️ 快速開始

**1. 複製儲存庫**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 建立 Python 虛擬環境**

強烈建議使用虛擬環境。

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 安裝依賴套件**

從 `requirements.txt` 安裝所有必要的 Python 套件。

```bash
pip install -r requirements.txt
```

**4. 設定環境變數**

代理程式需要 API 金鑰和其他設定。

首先，將範例環境檔案 `.env.example` 重新命名為 `.env`。

```bash
# Windows
rename .env.example .env

# macOS/Linux
mv .env.example .env
```

接下來，開啟新的 `.env` 檔案並加入您的 OpenAI API 金鑰。該檔案也包含您可以自訂的選用預設值。

```env
# 必要
OPENAI_API_KEY="your_openai_api_key_here"

# 選用：您可以覆寫這些預設值
# .env.example 中有註解說明它們的用途。
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 如何執行

從您的終端機執行 `Agent.py` 指令碼。代理程式將引導您互動式地完成整個流程。

```bash
python Agent.py
```

系統會提示您輸入 YouTube 影片連結，然後選擇語言。代理程式會在執行工作流程的每個步驟時，在主控台顯示詳細的日誌。完成後，您會在 `transcripts` 目錄中找到原始和翻譯後的 `.srt` 檔案。

---

## 🤝 如何貢獻

歡迎貢獻！如果您有改進的想法或發現任何問題，請隨時：

1.  Fork 本儲存庫。
2.  建立一個新的分支 (`git checkout -b feature/your-feature-name`)。
3.  進行您的變更。
4.  提交您的變更 (`git commit -m 'Add some feature'`)。
5.  將分支推送到遠端 (`git push origin feature/your-feature-name`)。
6.  開啟一個 Pull Request。

請確保適當地更新測試。

## 📄 授權條款

本專案採用 MIT 授權條款。如果儲存庫中包含 `LICENSE` 檔案，您可以在其中找到更多詳細資訊，或參考 [MIT 授權條款](https://opensource.org/licenses/MIT)。
