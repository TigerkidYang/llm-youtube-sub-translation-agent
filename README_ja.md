<div align="center">
  <h1>🎬 YTRossetaAI - あなたの言語でYouTubeを視聴 🌍</h1>
  <p>
    リアルタイム動画プレーヤー統合による高品質でコンテキスト対応のYouTube動画字幕翻訳のための先進的なAI駆動Webアプリケーション。
  </p>
  <p>
    <!-- バッジ -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="ライセンス: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs歓迎"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 他の言語のREADMEを読む：
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

このプロジェクトは、先進的な AI 技術を使用して YouTube 動画字幕を翻訳する洗練された Web ベースアプリケーションを提供します。Streamlit で構築され、LangGraph によって駆動され、リアルタイム動画再生、同期字幕表示、最適なパフォーマンスのためのインテリジェントキャッシングを備えた直感的なインターフェースを提供します。

## 🌟 主要機能

### 🎥 **インタラクティブな動画体験**

- **埋め込み YouTube プレーヤー**：同期字幕付きの動画をアプリ内で直接視聴
- **字幕オーバーレイ制御**：ワンクリックで動画オーバーレイ字幕のオン/オフを切り替え
- **リアルタイム同期**：字幕が動画再生と自動的に同期
- **フルスクリーン対応**：すべての画面サイズに最適化されたプレーヤー体験

### 🧠 **AI 駆動翻訳**

- **コンテキスト対応処理**：用語集、話者分析、スタイルガイドラインを含む包括的な翻訳メモリを生成
- **チャンク化翻訳**：精度確保のため字幕を管理可能なセグメントにインテリジェントに分割
- **品質検証**：信頼性のある出力を保証する自動フォーマットチェックと再試行メカニズム
- **複数 AI モデル**：抽出、コンテキスト生成、翻訳のための設定可能なモデル

### 🚀 **パフォーマンスと信頼性**

- **スマートキャッシング**：既存の翻訳を自動検出し再利用
- **デュアル抽出方法**：主要な youtube-transcript-api と yt-dlp フォールバック
- **進捗追跡**：詳細なステータス更新を伴うリアルタイム翻訳進捗
- **エラー回復**：堅牢なエラーハンドリングと優雅なフォールバック

### 🌍 **多言語サポート**

- **国際化インターフェース**：11 の UI サポート言語
- **自動言語検出**：利用可能なすべての字幕言語を発見
- **幅広い翻訳サポート**：AI モデルがサポートする任意の言語への翻訳

### 📁 **ファイル管理**

- **自動整理**：スマートファイル命名と専用フォルダ保存
- **SRT フォーマット**：最大互換性のための業界標準字幕フォーマット
- **ワンクリックダウンロード**：翻訳字幕ファイルへの簡単アクセス

## 🛠️ インストールとセットアップ

### 前提条件

- Python 3.9 以上
- OpenAI API キー（AI 翻訳に必要）
- モダン Web ブラウザ（Chrome、Firefox、Safari、Edge）

### クイックスタート

**1. リポジトリのクローン**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 仮想環境の作成**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 依存関係のインストール**

```bash
pip install -r requirements.txt
```

**4. 環境設定**

プロジェクトルートに`.env`ファイルを作成し、OpenAI API キーを追加：

```env
# 必須
OPENAI_API_KEY=あなたのopenai_apiキー

# オプション設定（デフォルト値を表示）
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. アプリケーションの起動**

```bash
python run_streamlit.py
```

アプリケーションは`http://localhost:8501`でデフォルトブラウザに自動的に開きます。

## 🎯 使用方法

### 基本ワークフロー

1. **アプリケーション起動**：`python run_streamlit.py`を実行
2. **動画 URL 入力**：任意の YouTube 動画リンクを貼り付け
3. **言語選択**：検出されたオプションからソース言語とターゲット言語を選択
4. **モデル設定**（オプション）：異なる処理段階で AI モデルを選択
5. **翻訳開始**：「AI 翻訳開始」をクリックして進捗を監視
6. **視聴とダウンロード**：同期字幕付きの翻訳動画を楽しみ、ファイルをダウンロード

### 高度な機能

#### モデル選択

- **抽出モデル**：字幕ダウンロードと前処理を処理
- **コンテキストモデル**：翻訳メモリとガイドラインを生成
- **翻訳モデル**：実際の翻訳作業を実行

#### キャッシングシステム

- 既存翻訳の自動検出
- 以前翻訳した動画の即座読み込み
- スマートキャッシュ無効化と管理

#### 多言語インターフェース

- 11 のサポートされるインターフェース言語間での切り替え
- 永続的な言語設定
- ローカライズされたエラーメッセージとヘルプテキスト

## 🏗️ アーキテクチャ概要

### コアコンポーネント

- **`streamlit_app.py`**：メイン Web インターフェースとユーザーインタラクションロジック
- **`Agent.py`**：LangGraph ベースの翻訳ワークフローエンジン
- **`get_sub.py`**：デュアルソースフォールバック付き字幕抽出
- **`prompts.py`**：最適な翻訳のために精巧に作られた AI プロンプト
- **`languages.py`**：完全な国際化サポート
- **`run_streamlit.py`**：依存関係チェック付きアプリケーションランチャー

### 翻訳ワークフロー

1. **URL 処理**：動画 ID を抽出しアクセス可能性を検証
2. **言語発見**：利用可能なすべての字幕言語を検出
3. **キャッシュチェック**：重複作業を避けるため既存翻訳を検索
4. **字幕抽出**：フォールバックメカニズムで元字幕をダウンロード
5. **コンテキスト生成**：包括的な翻訳メモリを作成
6. **チャンク化翻訳**：最適化されたセグメントで字幕を処理
7. **品質検証**：翻訳フォーマットを検証し必要に応じて再試行
8. **出力生成**：最終 SRT ファイルを作成し結果を表示

## ⚙️ 設定

### 環境変数

| 変数                            | 説明                       | デフォルト    |
| ------------------------------- | -------------------------- | ------------- |
| `OPENAI_API_KEY`                | OpenAI API キー（必須）    | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | 字幕ファイルディレクトリ   | `transcripts` |
| `AGENT_CHUNK_SIZE`              | 字幕処理チャンクサイズ     | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | 最大再試行回数             | `2`           |
| `EXTRACTION_MODEL`              | 字幕抽出 AI モデル         | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | 翻訳 AI モデル             | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | コンテキスト生成 AI モデル | `o3-mini`     |

## 🤝 貢献

貢献を歓迎します！始め方は以下の通りです：

1. **リポジトリをフォーク**：GitHub の「Fork」ボタンをクリック
2. **機能ブランチ作成**：`git checkout -b feature/your-feature-name`
3. **変更実装**：改善を実装
4. **徹底的テスト**：すべての機能が正常に動作することを確認
5. **プルリクエスト提出**：説明付きの詳細な PR を作成

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

---

<div align="center">
  <p>グローバルコミュニティのために❤️で作成</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ プロジェクトにスター</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 バグ報告</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 機能リクエスト</a>
  </p>
</div>
