<div align="center">
  <h1>🎬 YTRossetaAI - Смотрите YouTube на вашем языке 🌍</h1>
  <p>
    Продвинутое веб-приложение на базе ИИ для высококачественного, контекстно-осознанного перевода субтитров YouTube видео с интеграцией видеоплеера в реальном времени.
  </p>
  <p>
    <!-- Значки -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Лицензия: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PR Добро пожаловать"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Читать этот README на других языках:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a>
  </p>
</div>

Этот проект предоставляет изощренное веб-приложение для перевода субтитров YouTube видео с использованием передовых ИИ-технологий. Построенное на Streamlit и работающее на LangGraph, оно предлагает интуитивный интерфейс с воспроизведением видео в реальном времени, синхронизированным отображением субтитров и интеллектуальным кэшированием для оптимальной производительности.

## 🌟 Основные функции

### 🎥 **Интерактивный видео-опыт**

- **Встроенный YouTube плеер**: Просмотр видео прямо в приложении с синхронизированными субтитрами
- **Управление наложением субтитров**: Переключение наложения субтитров видео вкл/выкл одним кликом
- **Синхронизация в реальном времени**: Субтитры автоматически синхронизируются с воспроизведением видео
- **Поддержка полного экрана**: Оптимизированный опыт плеера для всех размеров экрана

### 🧠 **ИИ-перевод**

- **Контекстно-осознанная обработка**: Генерирует всестороннюю память перевода, включая глоссарий, анализ говорящих и стилистические указания
- **Перевод по частям**: Интеллектуально разделяет субтитры на управляемые сегменты для точности
- **Проверка качества**: Автоматическая проверка формата и механизмы повтора для надежного вывода
- **Множественные ИИ-модели**: Настраиваемые модели для извлечения, генерации контекста и перевода

### 🚀 **Производительность и надежность**

- **Умное кэширование**: Автоматически обнаруживает и повторно использует существующие переводы
- **Двойные методы извлечения**: Основной youtube-transcript-api с резервным yt-dlp
- **Отслеживание прогресса**: Прогресс перевода в реальном времени с подробными обновлениями статуса
- **Восстановление после ошибок**: Надежная обработка ошибок с элегантными резервными копиями

### 🌍 **Многоязычная поддержка**

- **Интернационализированный интерфейс**: 11 поддерживаемых языков интерфейса
- **Автоматическое определение языка**: Обнаруживает все доступные языки субтитров
- **Широкая поддержка перевода**: Переводит на любой язык, поддерживаемый ИИ-моделями

### 📁 **Управление файлами**

- **Автоматическая организация**: Умное именование файлов и хранение в выделенных папках
- **Формат SRT**: Промышленный стандарт формата субтитров для максимальной совместимости
- **Загрузка одним кликом**: Легкий доступ к переведенным файлам субтитров

## 🛠️ Установка и настройка

### Предварительные требования

- Python 3.9 или выше
- Ключ API OpenAI (требуется для ИИ-перевода)
- Современный веб-браузер (Chrome, Firefox, Safari или Edge)

### Быстрый старт

**1. Клонировать репозиторий**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Создать виртуальную среду**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Установить зависимости**

```bash
pip install -r requirements.txt
```

**4. Настроить среду**

Создать файл `.env` в корне проекта и добавить ваш ключ API OpenAI:

```env
# Обязательно
OPENAI_API_KEY=ваш_ключ_api_openai

# Дополнительные настройки (показаны значения по умолчанию)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Запустить приложение**

```bash
python run_streamlit.py
```

Приложение автоматически откроется в вашем браузере по умолчанию на `http://localhost:8501`.

## 🎯 Использование

### Базовый рабочий процесс

1. **Запустить приложение**: Выполнить `python run_streamlit.py`
2. **Ввести URL видео**: Вставить любую ссылку на видео YouTube
3. **Выбрать языки**: Выбрать исходный и целевой языки из обнаруженных опций
4. **Настроить модели** (Необязательно): Выбрать ИИ-модели для разных этапов обработки
5. **Начать перевод**: Нажать "Начать ИИ-перевод" и отслеживать прогресс
6. **Смотреть и скачивать**: Наслаждаться переведенным видео с синхронизированными субтитрами и скачивать файлы

## ⚙️ Конфигурация

### Переменные среды

| Переменная                      | Описание                         | По умолчанию  |
| ------------------------------- | -------------------------------- | ------------- |
| `OPENAI_API_KEY`                | Ключ API OpenAI (обязательно)    | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Директория файлов субтитров      | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Размер чанка обработки субтитров | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Максимальное количество повторов | `2`           |
| `EXTRACTION_MODEL`              | ИИ-модель извлечения субтитров   | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | ИИ-модель перевода               | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | ИИ-модель генерации контекста    | `o3-mini`     |

## 🤝 Вклад

Мы приветствуем вклады! Вот как начать:

1. **Форкнуть репозиторий**: Нажать кнопку "Fork" на GitHub
2. **Создать ветку функции**: `git checkout -b feature/your-feature-name`
3. **Реализовать изменения**: Реализовать ваши улучшения
4. **Тщательно протестировать**: Проверить, что все функции работают правильно
5. **Отправить Pull Request**: Создать подробный PR с описанием

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT. См. файл [LICENSE](LICENSE) для деталей.

---

<div align="center">
  <p>Сделано с ❤️ для глобального сообщества</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Поставить звезду проекту</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Сообщить об ошибке</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Запросить функцию</a>
  </p>
</div>
