<div align="center">
  <h1>🎬 YouTube字幕AI翻譯器 🌍</h1>
  <p>
    一個先進的AI驅動網路應用程式，用於高品質、上下文感知的YouTube影片字幕翻譯，整合即時影片播放器。
  </p>
  <p>
    <!-- 徽章 -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="授權: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="問題"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="歡迎 PR"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 閱讀其他語言版本的 README：
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

本專案提供了一個使用先進 AI 技術翻譯 YouTube 影片字幕的複雜網路應用程式。基於 Streamlit 構建並由 LangGraph 驅動，它提供直觀的介面，具有即時影片播放、同步字幕顯示和智慧快取功能，以實現最佳效能。

## 🌟 主要功能

### 🎥 **互動式影片體驗**

- **嵌入式 YouTube 播放器**：直接在應用程式中觀看具有同步字幕的影片
- **字幕覆蓋控制**：一鍵切換影片覆蓋字幕的開/關
- **即時同步**：字幕自動與影片播放同步
- **全螢幕支援**：適配所有螢幕尺寸的最佳化播放器體驗

### 🧠 **AI 驅動的翻譯**

- **上下文感知處理**：生成包括詞彙表、說話者分析和風格指南的綜合翻譯記憶
- **分塊翻譯**：智慧地將字幕分割成可管理的片段以確保準確性
- **品質驗證**：自動格式檢查和重試機制確保可靠輸出
- **多種 AI 模型**：可設定的提取、上下文生成和翻譯模型

### 🚀 **效能與可靠性**

- **智慧快取**：自動偵測並重複使用現有翻譯
- **雙重提取方法**：主要的 youtube-transcript-api 配合 yt-dlp 後備方案
- **進度追蹤**：即時翻譯進度與詳細狀態更新
- **錯誤復原**：強大的錯誤處理和優雅的後備機制

### 🌍 **多語言支援**

- **國際化介面**：支援 11 種 UI 語言
- **自動語言偵測**：發現所有可用的字幕語言
- **廣泛翻譯支援**：翻譯為 AI 模型支援的任何語言

### 📁 **檔案管理**

- **自動組織**：智慧檔案命名和專用資料夾儲存
- **SRT 格式**：工業標準字幕格式，最大相容性
- **一鍵下載**：輕鬆存取翻譯字幕檔案

## 🛠️ 安裝與設定

### 前置需求

- Python 3.9 或更高版本
- OpenAI API 金鑰（AI 翻譯所需）
- 現代網路瀏覽器（Chrome、Firefox、Safari 或 Edge）

### 快速開始

**1. 複製儲存庫**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 建立虛擬環境**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 安裝依賴**

```bash
pip install -r requirements.txt
```

**4. 設定環境**

在專案根目錄建立`.env`檔案並新增您的 OpenAI API 金鑰：

```env
# 必填
OPENAI_API_KEY=您的openai_api金鑰

# 可選設定（顯示預設值）
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. 啟動應用程式**

```bash
python run_streamlit.py
```

應用程式將自動在您的預設瀏覽器中開啟，位址為`http://localhost:8501`。

## 🎯 使用方法

### 基本工作流程

1. **啟動應用程式**：執行`python run_streamlit.py`
2. **輸入影片 URL**：貼上任何 YouTube 影片連結
3. **選擇語言**：從偵測到的選項中選擇來源語言和目標語言
4. **設定模型**（可選）：為不同處理階段選擇 AI 模型
5. **開始翻譯**：點擊「開始 AI 翻譯」並監控進度
6. **觀看和下載**：享受具有同步字幕的翻譯影片並下載檔案

### 進階功能

#### 模型選擇

- **提取模型**：處理字幕下載和預處理
- **上下文模型**：生成翻譯記憶和指導原則
- **翻譯模型**：執行實際翻譯工作

#### 快取系統

- 自動偵測現有翻譯
- 之前翻譯影片的即時載入
- 智慧快取失效和管理

#### 多語言介面

- 在 11 種支援的介面語言之間切換
- 持久的語言偏好設定
- 本地化的錯誤訊息和說明文字

## 🏗️ 架構概述

### 核心元件

- **`streamlit_app.py`**：主要 Web 介面和使用者互動邏輯
- **`Agent.py`**：基於 LangGraph 的翻譯工作流引擎
- **`get_sub.py`**：具有雙來源備份的字幕提取
- **`prompts.py`**：為最佳翻譯精心製作的 AI 提示
- **`languages.py`**：完整的國際化支援
- **`run_streamlit.py`**：具有依賴檢查的應用程式啟動器

### 翻譯工作流程

1. **URL 處理**：提取影片 ID 並驗證可存取性
2. **語言發現**：偵測所有可用的字幕語言
3. **快取檢查**：尋找現有翻譯以避免重複工作
4. **字幕提取**：使用備份機制下載原始字幕
5. **上下文生成**：建立綜合翻譯記憶
6. **分塊翻譯**：在最佳化的片段中處理字幕
7. **品質驗證**：驗證翻譯格式並根據需要重試
8. **輸出生成**：建立最終 SRT 檔案並顯示結果

## ⚙️ 設定

### 環境變數

| 變數                            | 描述                    | 預設值        |
| ------------------------------- | ----------------------- | ------------- |
| `OPENAI_API_KEY`                | OpenAI API 金鑰（必填） | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | 字幕檔案目錄            | `transcripts` |
| `AGENT_CHUNK_SIZE`              | 字幕處理塊大小          | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | 最大重試次數            | `2`           |
| `EXTRACTION_MODEL`              | 字幕提取 AI 模型        | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | 翻譯 AI 模型            | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | 上下文生成 AI 模型      | `o3-mini`     |

## 🤝 貢獻

我們歡迎貢獻！以下是開始方法：

1. **Fork 儲存庫**：點擊 GitHub 上的"Fork"按鈕
2. **建立功能分支**：`git checkout -b feature/your-feature-name`
3. **進行更改**：實現您的改進
4. **徹底測試**：驗證所有功能正常運作
5. **提交 Pull Request**：建立帶有描述的詳細 PR

## 📄 授權

本專案採用 MIT 授權。詳細資訊請參見[LICENSE](LICENSE)檔案。

---

<div align="center">
  <p>用❤️為全球社群製作</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ 給專案加星</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 回報Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 請求功能</a>
  </p>
</div>
