<div align="center">
  <h1>🎬 YouTube字幕AI翻译器 🌍</h1>
  <p>
    一个先进的AI驱动网络应用程序，用于高质量、上下文感知的YouTube视频字幕翻译，集成实时视频播放器。
  </p>
  <p>
    <!-- 徽章 -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
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

本项目提供了一个使用先进 AI 技术翻译 YouTube 视频字幕的复杂网络应用程序。基于 Streamlit 构建并由 LangGraph 驱动，它提供直观的界面，具有实时视频播放、同步字幕显示和智能缓存功能，以实现最佳性能。

## 🌟 主要功能

### 🎥 **交互式视频体验**

- **嵌入式 YouTube 播放器**：直接在应用程序中观看具有同步字幕的视频
- **字幕叠加控制**：一键切换视频叠加字幕的开/关
- **实时同步**：字幕自动与视频播放同步
- **全屏支持**：适配所有屏幕尺寸的优化播放器体验

### 🧠 **AI 驱动的翻译**

- **上下文感知处理**：生成包括词汇表、说话者分析和风格指南的综合翻译记忆
- **分块翻译**：智能地将字幕分割成可管理的片段以确保准确性
- **质量验证**：自动格式检查和重试机制确保可靠输出
- **多种 AI 模型**：可配置的提取、上下文生成和翻译模型

### 🚀 **性能与可靠性**

- **智能缓存**：自动检测并重用现有翻译
- **双重提取方法**：主要的 youtube-transcript-api 配合 yt-dlp 后备方案
- **进度跟踪**：实时翻译进度与详细状态更新
- **错误恢复**：强大的错误处理和优雅的后备机制

### 🌍 **多语言支持**

- **国际化界面**：支持 11 种 UI 语言
- **自动语言检测**：发现所有可用的字幕语言
- **广泛翻译支持**：翻译为 AI 模型支持的任何语言

### 📁 **文件管理**

- **自动组织**：智能文件命名和专用文件夹存储
- **SRT 格式**：工业标准字幕格式，最大兼容性
- **一键下载**：轻松访问翻译字幕文件

## 🛠️ 安装与设置

### 前置要求

- Python 3.9 或更高版本
- OpenAI API 密钥（AI 翻译所需）
- 现代网络浏览器（Chrome、Firefox、Safari 或 Edge）

### 快速开始

**1. 克隆仓库**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 创建虚拟环境**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 安装依赖**

```bash
pip install -r requirements.txt
```

**4. 配置环境**

在项目根目录创建`.env`文件并添加您的 OpenAI API 密钥：

```env
# 必填
OPENAI_API_KEY=您的openai_api密钥

# 可选配置（显示默认值）
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. 启动应用程序**

```bash
python run_streamlit.py
```

应用程序将自动在您的默认浏览器中打开，地址为`http://localhost:8501`。

## 🎯 使用方法

### 基本工作流程

1. **启动应用程序**：运行`python run_streamlit.py`
2. **输入视频 URL**：粘贴任何 YouTube 视频链接
3. **选择语言**：从检测到的选项中选择源语言和目标语言
4. **配置模型**（可选）：为不同处理阶段选择 AI 模型
5. **开始翻译**：点击"开始 AI 翻译"并监控进度
6. **观看和下载**：享受具有同步字幕的翻译视频并下载文件

### 高级功能

#### 模型选择

- **提取模型**：处理字幕下载和预处理
- **上下文模型**：生成翻译记忆和指导原则
- **翻译模型**：执行实际翻译工作

#### 缓存系统

- 自动检测现有翻译
- 以前翻译视频的即时加载
- 智能缓存失效和管理

#### 多语言界面

- 在 11 种支持的界面语言之间切换
- 持久的语言首选项
- 本地化的错误消息和帮助文本

## 🏗️ 架构概述

### 核心组件

- **`streamlit_app.py`**：主要 Web 界面和用户交互逻辑
- **`Agent.py`**：基于 LangGraph 的翻译工作流引擎
- **`get_sub.py`**：具有双源备份的字幕提取
- **`prompts.py`**：为最佳翻译精心制作的 AI 提示
- **`languages.py`**：完整的国际化支持
- **`run_streamlit.py`**：具有依赖检查的应用程序启动器

### 翻译工作流程

1. **URL 处理**：提取视频 ID 并验证可访问性
2. **语言发现**：检测所有可用的字幕语言
3. **缓存检查**：查找现有翻译以避免重复工作
4. **字幕提取**：使用备用机制下载原始字幕
5. **上下文生成**：创建综合翻译记忆
6. **分块翻译**：在优化的片段中处理字幕
7. **质量验证**：验证翻译格式并根据需要重试
8. **输出生成**：创建最终 SRT 文件并显示结果

### 技术栈

- **前端**：Streamlit（交互式 Web 界面）
- **AI 框架**：LangGraph（工作流编排）
- **AI 模型**：OpenAI GPT 模型（可配置）
- **字幕 API**：youtube-transcript-api + yt-dlp（双重备份）
- **文件处理**：Python 标准库 + 自定义解析器

## ⚙️ 配置

### 环境变量

| 变量                            | 描述                    | 默认值        |
| ------------------------------- | ----------------------- | ------------- |
| `OPENAI_API_KEY`                | OpenAI API 密钥（必填） | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | 字幕文件目录            | `transcripts` |
| `AGENT_CHUNK_SIZE`              | 字幕处理块大小          | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | 最大重试次数            | `2`           |
| `EXTRACTION_MODEL`              | 字幕提取 AI 模型        | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | 翻译 AI 模型            | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | 上下文生成 AI 模型      | `o3-mini`     |

## 🔧 故障排除

### 常见问题

**应用程序无法启动**

- 验证 Python 版本（3.9+）
- 检查所有依赖是否已安装
- 确保已配置 OpenAI API 密钥

**翻译失败**

- 验证 OpenAI API 密钥有效且有额度
- 检查网络连接
- 如果受到速率限制，尝试不同的 AI 模型

**找不到字幕**

- 验证视频有可用字幕
- 尝试不同的语言选项
- 检查视频是否可公开访问

**界面语言问题**

- 清除浏览器缓存并刷新
- 检查浏览器语言设置
- 尝试从下拉菜单手动选择语言

### 性能优化

- 对大型视频使用更快的 AI 模型
- 为经常翻译的内容启用缓存
- 关闭其他应用程序以释放系统资源
- 使用有线网络连接以保证稳定性

## 🤝 贡献

我们欢迎贡献！以下是开始方法：

1. **Fork 仓库**：点击 GitHub 上的"Fork"按钮
2. **创建功能分支**：`git checkout -b feature/your-feature-name`
3. **进行更改**：实现您的改进
4. **彻底测试**：验证所有功能正常工作
5. **提交 Pull Request**：创建带有描述的详细 PR

### 开发指南

- 遵循 Python PEP 8 风格指南
- 为新函数添加全面的文档字符串
- 为新功能更新文档
- 使用各种视频类型和语言进行测试
- 尽可能保持向后兼容性

### 贡献领域

- 额外的字幕格式支持（VTT、ASS 等）
- 新的 AI 模型集成
- 性能优化
- 额外的语言支持
- UI/UX 改进
- 移动响应式增强

## 📊 项目统计

- **代码行数**：约 3,200 行
- **支持的 UI 语言**：11 种
- **支持的 AI 模型**：5+种
- **字幕格式**：SRT（计划更多）
- **备份系统**：2 个（youtube-transcript-api + yt-dlp）

## 📄 许可证

本项目采用 MIT 许可证。详细信息请参见[LICENSE](LICENSE)文件。

## 🙏 致谢

- **OpenAI**：提供强大的语言模型
- **Streamlit**：优秀的 Web 应用程序框架
- **LangGraph**：强大的工作流编排
- **YouTube Transcript API**：字幕访问
- **yt-dlp**：可靠的视频数据提取
- **开源社区**：持续的灵感和支持

---

<div align="center">
  <p>用❤️为全球社区制作</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ 给项目加星</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 报告Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 请求功能</a>
  </p>
</div>
