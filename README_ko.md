<div align="center">
  <h1>🎬 YTRossetaAI - 당신의 언어로 YouTube 보기 🌍</h1>
  <p>
    실시간 비디오 플레이어 통합을 통한 고품질, 컨텍스트 인식 YouTube 비디오 자막 번역을 위한 고급 AI 기반 웹 애플리케이션.
  </p>
  <p>
    <!-- 배지 -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="라이선스: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="이슈"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PR 환영"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 다른 언어로 README 읽기:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

이 프로젝트는 고급 AI 기술을 사용하여 YouTube 비디오 자막을 번역하는 정교한 웹 기반 애플리케이션을 제공합니다. Streamlit으로 구축되고 LangGraph로 구동되며, 실시간 비디오 재생, 동기화된 자막 표시 및 최적의 성능을 위한 지능형 캐싱을 갖춘 직관적인 인터페이스를 제공합니다.

## 🌟 주요 기능

### 🎥 **인터랙티브 비디오 경험**

- **임베디드 YouTube 플레이어**: 동기화된 자막이 있는 비디오를 앱 내에서 직접 시청
- **자막 오버레이 제어**: 원클릭으로 비디오 오버레이 자막 켜기/끄기 전환
- **실시간 동기화**: 자막이 비디오 재생과 자동으로 동기화
- **전체 화면 지원**: 모든 화면 크기에 최적화된 플레이어 경험

### 🧠 **AI 기반 번역**

- **컨텍스트 인식 처리**: 용어집, 화자 분석 및 스타일 가이드라인을 포함한 포괄적인 번역 메모리 생성
- **청크 기반 번역**: 정확성을 보장하기 위해 자막을 관리 가능한 세그먼트로 지능적으로 분할
- **품질 검증**: 신뢰할 수 있는 출력을 보장하는 자동 형식 검사 및 재시도 메커니즘
- **다중 AI 모델**: 추출, 컨텍스트 생성 및 번역을 위한 구성 가능한 모델

### 🚀 **성능 및 신뢰성**

- **스마트 캐싱**: 기존 번역을 자동으로 감지하고 재사용
- **이중 추출 방법**: 기본 youtube-transcript-api와 yt-dlp 백업
- **진행률 추적**: 자세한 상태 업데이트가 포함된 실시간 번역 진행률
- **오류 복구**: 강력한 오류 처리 및 우아한 백업 메커니즘

### 🌍 **다국어 지원**

- **국제화 인터페이스**: 11개 UI 지원 언어
- **자동 언어 감지**: 사용 가능한 모든 자막 언어 발견
- **광범위한 번역 지원**: AI 모델이 지원하는 모든 언어로 번역

### 📁 **파일 관리**

- **자동 정리**: 스마트 파일 명명 및 전용 폴더 저장
- **SRT 형식**: 최대 호환성을 위한 업계 표준 자막 형식
- **원클릭 다운로드**: 번역된 자막 파일에 쉽게 액세스

## 🛠️ 설치 및 설정

### 전제 조건

- Python 3.9 이상
- OpenAI API 키 (AI 번역에 필요)
- 최신 웹 브라우저 (Chrome, Firefox, Safari 또는 Edge)

### 빠른 시작

**1. 저장소 복제**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. 가상 환경 생성**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 종속성 설치**

```bash
pip install -r requirements.txt
```

**4. 환경 구성**

프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 추가:

```env
# 필수
OPENAI_API_KEY=your_openai_api_key

# 선택적 구성 (기본값 표시)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. 애플리케이션 시작**

```bash
python run_streamlit.py
```

애플리케이션이 `http://localhost:8501`에서 기본 브라우저에 자동으로 열립니다.

## 🎯 사용 방법

### 기본 워크플로우

1. **애플리케이션 시작**: `python run_streamlit.py` 실행
2. **비디오 URL 입력**: 모든 YouTube 비디오 링크 붙여넣기
3. **언어 선택**: 감지된 옵션에서 소스 및 대상 언어 선택
4. **모델 구성** (선택사항): 다양한 처리 단계에서 AI 모델 선택
5. **번역 시작**: "AI 번역 시작" 클릭하고 진행률 모니터링
6. **시청 및 다운로드**: 동기화된 자막이 있는 번역 비디오를 즐기고 파일 다운로드

## ⚙️ 구성

### 환경 변수

| 변수                            | 설명                  | 기본값        |
| ------------------------------- | --------------------- | ------------- |
| `OPENAI_API_KEY`                | OpenAI API 키 (필수)  | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | 자막 파일 디렉토리    | `transcripts` |
| `AGENT_CHUNK_SIZE`              | 자막 처리 청크 크기   | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | 최대 재시도 횟수      | `2`           |
| `EXTRACTION_MODEL`              | 자막 추출 AI 모델     | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | 번역 AI 모델          | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | 컨텍스트 생성 AI 모델 | `o3-mini`     |

## 🤝 기여

기여를 환영합니다! 시작하는 방법:

1. **저장소 포크**: GitHub에서 "Fork" 버튼 클릭
2. **기능 브랜치 생성**: `git checkout -b feature/your-feature-name`
3. **변경 사항 구현**: 개선 사항 구현
4. **철저한 테스트**: 모든 기능이 제대로 작동하는지 확인
5. **풀 리퀘스트 제출**: 설명이 포함된 자세한 PR 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.

---

<div align="center">
  <p>글로벌 커뮤니티를 위해 ❤️로 제작</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ 프로젝트에 별표</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 버그 신고</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 기능 요청</a>
  </p>
</div>
