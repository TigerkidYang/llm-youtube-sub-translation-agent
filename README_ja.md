<div align="center">
  <h1>🎬 LLM YouTube 字幕翻訳エージェント 🌍</h1>
  <p>
    LangGraph を使用した、高品質でコンテキストを意識した YouTube 動画字幕の高度な AI 翻訳エージェントです。
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
    🌐 他の言語でこの README を読む:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | 日本語 | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

このプロジェクトは、YouTube 動画字幕の翻訳を自動化する高度なマルチステップ AI エージェントを実装しています。LangGraph フレームワークを使用して、単純な翻訳を超えて文脈上の一貫性と高品質を保証する堅牢でインテリジェントなパイプラインを作成します。

エージェントはまず字幕を取得し、全文を分析して「翻訳メモリ」（用語集とスタイルガイドを含む）を生成し、次にコンテンツをチャンクごとに翻訳し、各出力を検証してから結果を新しい `.srt` ファイルに最終化します。

## 📖 目次

- [✨ 主な機能](#-主な機能)
- [🚀 仕組み：エージェントのワークフロー](#-仕組みエージェントのワークフロー)
- [🛠️ セットアップとインストール](#️-セットアップとインストール)
- [🏃 実行方法](#-実行方法)
- [🤝 貢献](#-貢献)
- [📄 ライセンス](#-ライセンス)

## ✨ 主な機能

-   **インタラクティブなセットアップ**：🗣️ YouTube 動画のリンクと希望の原文/翻訳言語をユーザーに促します。
-   **コンテキストを意識した翻訳**：🧠 翻訳前に、エージェントは包括的なコンテキストガイド（動画の基本情報、用語集、声の説明、スタイルに関するヒント）を生成し、高品質で一貫性のある翻訳を保証します。
-   **チャンクベースの処理**：🧩 字幕を管理しやすいチャンクに分割し、言語モデルによる効率的で信頼性の高い処理を実現します。
-   **堅牢で自己修正機能**：💪 LLM の翻訳出力のフォーマットエラー（不要なマークダウンなど）をチェックし、修正指示を付けて自動的に再試行する検証ステップが含まれています。
-   **ステートフルなワークフロー**：🔄 `langgraph` で構築され、複雑なマルチステッププロセスを明確で、回復力があり、観察可能な方法で管理します。
-   **自動ファイル管理**：📂 元の `.srt` ファイルと最終的な翻訳済み `.srt` ファイルの両方を、専用の `transcripts` ディレクトリにインテリジェントに命名して保存します。

## 🚀 仕組み：エージェントのワークフロー

エージェントはステートマシンとして動作し、定義された一連のステップを経て翻訳タスクを完了します。

1.  **動画リンクの取得**：🔗 エージェントは、ユーザーに YouTube 動画の URL を尋ねることから始まります。
2.  **利用可能な言語のリスト表示**：📜 YouTube Transcript API を呼び出して、動画で利用可能なすべての字幕言語を検索し、表示します。
3.  **言語の選択**：🎯 ユーザーは翻訳元の字幕言語を選択し、翻訳先の言語を指定します。
4.  **字幕の取得**：📥 LLM を活用したツールエージェントが呼び出されます。`fetch_youtube_srt` ツールを正しく呼び出して元の字幕をダウンロードし、`.srt` ファイル（例：`transcripts/video_id_en.srt`）として保存します。
5.  **翻訳の準備**：⚙️ ダウンロードした `.srt` ファイルを解析し、その内容を `CHUNK_SIZE` に基づいて、番号付きの小さなテキストチャンクに分割します。
6.  **翻訳コンテキストの生成**：💡 エージェントは、*全体*の元の字幕テキストを LLM に送信して「翻訳メモリ」を生成します。この重要なドキュメントには、主要な用語の用語集、話者の声とトーンの説明、一貫性を確保するための翻訳のヒントが含まれています。
7.  **チャンクの翻訳（ループ）**：🔁 エージェントは各テキストチャンクを反復処理します。  
    a.  **翻訳**：現在のチャンクは、コンテキスト用の翻訳メモリとともに翻訳のために LLM に送信されます。  
    b.  **検証**：LLM の出力の正しさがチェックされます。具体的には、出力がプレーンテキストであり、マークダウンコードブロックで囲まれていないことを確認します。検証に失敗した場合、エージェントは定義された最大回数まで翻訳を再試行します。  
    c.  **集約**：検証済みの翻訳済みテキストがリストに追加されます。チャンクが繰り返し検証に失敗した場合、データ損失を防ぐために元のテキストがプレースホルダーとして使用されます。  
8.  **翻訳の最終化**：✅ すべてのチャンクが翻訳されると、エージェントは完全な翻訳済み字幕リストを再構築し、SRT 形式に戻して新しいファイル（例：`transcripts/video_id_en_ja.srt`）に保存します。
9.  **終了**：🎉 プロセス完了です。

## 🛠️ クイックスタート

**1. リポジトリのクローン**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Python 仮想環境の作成**

仮想環境の使用を強くお勧めします。

```bash
# Windows の場合
python -m venv venv
venv\Scripts\activate

# macOS/Linux の場合
python3 -m venv venv
source venv/bin/activate
```

**3. 依存関係のインストール**

`requirements.txt` から必要なすべての Python パッケージをインストールします。

```bash
pip install -r requirements.txt
```

**4. 環境変数の設定**

エージェントには API キーとその他の設定が必要です。

まず、サンプル環境ファイル `.env.example` を `.env` に名前変更します。

```bash
# Windows の場合
rename .env.example .env

# macOS/Linux の場合
mv .env.example .env
```

次に、新しい `.env` ファイルを開き、OpenAI API キーを追加します。このファイルには、カスタマイズ可能なオプションのデフォルト値も含まれています。

```env
# 必須
OPENAI_API_KEY="your_openai_api_key_here"

# オプション：これらのデフォルト値は上書きできます
# それらが何であるかについては、.env.example にコメントがあります。
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 実行方法

ターミナルから `Agent.py` スクリプトを実行します。エージェントがインタラクティブにプロセスを案内します。

```bash
python Agent.py
```

YouTube 動画のリンクを入力し、次に言語を選択するよう求められます。エージェントは、ワークフローの各ステップを実行する際に、コンソールに詳細なログを表示します。終了すると、`transcripts` ディレクトリに元の `.srt` ファイルと翻訳済みの `.srt` ファイルが見つかります。

---

## 🤝 貢献

貢献を歓迎します！改善のためのアイデアがある場合や問題を見つけた場合は、お気軽に次の手順を実行してください：

1.  リポジトリをフォークします。
2.  新しいブランチを作成します（`git checkout -b feature/your-feature-name`）。
3.  変更を加えます。
4.  変更をコミットします（`git commit -m 'Add some feature'`）。
5.  ブランチにプッシュします（`git push origin feature/your-feature-name`）。
6.  プルリクエストを開きます。

必要に応じてテストを更新してください。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。リポジトリに `LICENSE` ファイルが含まれている場合は詳細を確認できます。または、[MIT ライセンス条項](https://opensource.org/licenses/MIT)を参照してください。
