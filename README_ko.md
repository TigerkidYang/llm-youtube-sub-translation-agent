<div align="center">
  <h1>🎬 LLM YouTube 자막 번역 에이전트 🌍</h1>
  <p>
    LangGraph를 사용하여 고품질의 문맥 인식 YouTube 비디오 자막을 위한 고급 AI 번역 에이전트입니다.
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
    🌐 다른 언어로 이 README 읽기:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | 한국어 | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

이 프로젝트는 YouTube 비디오 자막 번역을 자동화하는 고급 다단계 AI 에이전트를 구현합니다. LangGraph 프레임워크를 사용하여 단순한 번역을 넘어 문맥적 일관성과 고품질을 보장하는 강력하고 지능적인 파이프라인을 만듭니다.

에이전트는 먼저 자막을 가져오고, 전체 텍스트를 분석하여 "번역 메모리"(용어집 및 스타일 가이드 포함)를 생성한 다음, 콘텐츠를 청크 단위로 번역하고, 각 출력을 검증한 후 결과를 새 `.srt` 파일로 최종화합니다.

## 📖 목차

- [✨ 주요 기능](#-주요-기능)
- [🚀 작동 방식: 에이전트 워크플로](#-작동-방식-에이전트-워크플로)
- [🛠️ 설정 및 설치](#️-설정-및-설치)
- [🏃 실행 방법](#-실행-방법)
- [🤝 기여](#-기여)
- [📄 라이선스](#-라이선스)

## ✨ 주요 기능

-   **대화형 설정**: 🗣️ 사용자에게 YouTube 비디오 링크와 원하는 원본/대상 언어를 묻습니다.
-   **문맥 인식 번역**: 🧠 번역하기 전에 에이전트는 포괄적인 문맥 가이드(비디오 기본 정보, 용어집, 음성 설명 및 스타일 팁)를 생성하여 고품질의 일관된 번역을 보장합니다.
-   **청크 기반 처리**: 🧩 자막을 관리하기 쉬운 청크로 분할하여 언어 모델이 효율적이고 안정적으로 처리하도록 합니다.
-   **강력하고 자가 수정 기능**: 💪 LLM의 번역된 출력에서 서식 오류(원치 않는 마크다운 등)를 확인하고 수정 지침과 함께 자동으로 재시도하는 유효성 검사 단계를 포함합니다.
-   **상태 저장 워크플로**: 🔄 `langgraph`로 구축되어 복잡한 다단계 프로세스를 명확하고 탄력적이며 관찰 가능한 방식으로 관리합니다.
-   **자동 파일 관리**: 📂 원본 및 최종 번역된 `.srt` 파일을 전용 `transcripts` 디렉토리에 지능적으로 이름을 지정하고 저장합니다.

## 🚀 작동 방식: 에이전트 워크플로

에이전트는 상태 시스템으로 작동하며, 정의된 일련의 단계를 통해 번역 작업을 완료합니다.

1.  **비디오 링크 가져오기**: 🔗 에이전트는 사용자에게 YouTube 비디오 URL을 묻는 것으로 시작합니다.
2.  **사용 가능한 언어 목록 표시**: 📜 YouTube Transcript API를 호출하여 비디오에 사용할 수 있는 모든 자막 언어를 찾아 표시합니다.
3.  **언어 선택 가져오기**: 🎯 사용자는 번역할 원본 자막 언어를 선택하고 대상 언어를 지정합니다.
4.  **자막 가져오기**: 📥 LLM 기반 도구 에이전트가 호출됩니다. `fetch_youtube_srt` 도구를 올바르게 호출하여 원본 자막을 다운로드하고 `.srt` 파일(예: `transcripts/video_id_en.srt`)로 저장합니다.
5.  **번역 준비**: ⚙️ 다운로드한 `.srt` 파일을 구문 분석하고 `CHUNK_SIZE`를 기준으로 내용을 더 작고 번호가 매겨진 텍스트 청크로 분할합니다.
6.  **번역 문맥 생성**: 💡 에이전트는 *전체* 원본 자막 텍스트를 LLM으로 보내 "번역 메모리"를 생성합니다. 이 중요한 문서에는 주요 용어 용어집, 화자의 목소리와 어조에 대한 설명, 일관성을 보장하기 위한 번역 팁이 포함되어 있습니다.
7.  **청크 번역(루프)**: 🔁 에이전트는 각 텍스트 청크를 반복합니다.  
    a.  **번역**: 현재 청크는 문맥을 위한 번역 메모리와 함께 번역을 위해 LLM으로 전송됩니다.  
    b.  **유효성 검사**: LLM의 출력이 올바른지 확인합니다. 특히 출력이 일반 텍스트이고 마크다운 코드 블록으로 묶여 있지 않은지 확인합니다. 유효성 검사에 실패하면 에이전트는 정의된 최대 횟수까지 번역을 재시도합니다.  
    c.  **집계**: 유효성이 검사된 번역된 텍스트가 목록에 추가됩니다. 청크가 반복적으로 유효성 검사에 실패하면 데이터 손실을 방지하기 위해 원본 텍스트가 자리 표시자로 사용됩니다.  
8.  **번역 완료**: ✅ 모든 청크가 번역되면 에이전트는 완전한 번역된 자막 목록을 재구성하고 SRT 형식으로 다시 변환한 다음 새 파일(예: `transcripts/video_id_en_ko.srt`)에 저장합니다.
9.  **종료**: 🎉 프로세스가 완료됩니다.

## 🛠️ 빠른 시작

**1. 리포지토리 복제**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Python 가상 환경 만들기**

가상 환경을 사용하는 것이 좋습니다.

```bash
# Windows의 경우
python -m venv venv
venv\Scripts\activate

# macOS/Linux의 경우
python3 -m venv venv
source venv/bin/activate
```

**3. 종속성 설치**

`requirements.txt`에서 필요한 모든 Python 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

**4. 환경 변수 구성**

에이전트에는 API 키 및 기타 구성이 필요합니다.

먼저 예제 환경 파일 `.env.example`의 이름을 `.env`로 바꿉니다.

```bash
# Windows의 경우
rename .env.example .env

# macOS/Linux의 경우
mv .env.example .env
```

다음으로 새 `.env` 파일을 열고 OpenAI API 키를 추가합니다. 이 파일에는 사용자 지정할 수 있는 선택적 기본값도 포함됩니다.

```env
# 필수
OPENAI_API_KEY="your_openai_api_key_here"

# 선택 사항: 이러한 기본값을 재정의할 수 있습니다.
# .env.example에 해당 내용에 대한 주석이 있습니다.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 실행 방법

터미널에서 `Agent.py` 스크립트를 실행합니다. 에이전트가 대화식으로 프로세스를 안내합니다.

```bash
python Agent.py
```

YouTube 비디오 링크를 입력한 다음 언어를 선택하라는 메시지가 표시됩니다. 에이전트는 워크플로의 각 단계를 실행할 때 콘솔에 자세한 로그를 표시합니다. 완료되면 `transcripts` 디렉토리에서 원본 및 번역된 `.srt` 파일을 찾을 수 있습니다.

---

## 🤝 기여

기여를 환영합니다! 개선 아이디어가 있거나 문제를 발견하면 언제든지 다음을 수행하십시오.

1.  리포지토리를 포크합니다.
2.  새 브랜치를 만듭니다 (`git checkout -b feature/your-feature-name`).
3.  변경 사항을 적용합니다.
4.  변경 사항을 커밋합니다 (`git commit -m 'Add some feature'`).
5.  브랜치에 푸시합니다 (`git push origin feature/your-feature-name`).
6.  풀 리퀘스트를 엽니다.

적절하게 테스트를 업데이트하십시오.

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 리포지토리에 `LICENSE` 파일이 포함된 경우 자세한 내용을 찾거나 [MIT 라이선스 조건](https://opensource.org/licenses/MIT)을 참조하십시오.
