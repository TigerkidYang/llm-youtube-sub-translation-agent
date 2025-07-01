<div align="center">
  <h1>🎬 YTRossetaAI - YouTube in Ihrer Sprache ansehen 🌍</h1>
  <p>
    Eine fortschrittliche KI-gestützte Webanwendung für hochwertige, kontextbewusste Übersetzung von YouTube-Video-Untertiteln mit Echtzeit-Videoplayer-Integration.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Lizenz: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Willkommen"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Diese README in anderen Sprachen lesen:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Dieses Projekt bietet eine ausgeklügelte webbasierte Anwendung zur Übersetzung von YouTube-Video-Untertiteln mit fortschrittlicher KI-Technologie. Gebaut mit Streamlit und angetrieben von LangGraph, bietet es eine intuitive Benutzeroberfläche mit Echtzeit-Videowiedergabe, synchronisierter Untertitelanzeige und intelligentem Caching für optimale Leistung.

## 🌟 Hauptfunktionen

### 🎥 **Interaktive Video-Erfahrung**

- **Eingebetteter YouTube-Player**: Videos direkt in der App mit synchronisierten Untertiteln ansehen
- **Untertitel-Overlay-Steuerung**: Video-Overlay-Untertitel mit einem Klick ein-/ausschalten
- **Echtzeit-Synchronisation**: Untertitel synchronisieren automatisch mit der Videowiedergabe
- **Vollbild-Unterstützung**: Optimierte Player-Erfahrung für alle Bildschirmgrößen

### 🧠 **KI-gestützte Übersetzung**

- **Kontextbewusste Verarbeitung**: Generiert umfassendes Übersetzungsgedächtnis mit Glossar, Sprecher-Analyse und Stil-Richtlinien
- **Chunk-basierte Übersetzung**: Teilt Untertitel intelligent in handhabbare Segmente für Genauigkeit
- **Qualitätsvalidierung**: Automatische Formatprüfung und Wiederholungsmechanismen für zuverlässige Ausgabe
- **Mehrere KI-Modelle**: Konfigurierbare Modelle für Extraktion, Kontextgenerierung und Übersetzung

### 🚀 **Leistung und Zuverlässigkeit**

- **Intelligenter Cache**: Erkennt und verwendet bestehende Übersetzungen automatisch wieder
- **Duale Extraktionsmethoden**: Primäre youtube-transcript-api mit yt-dlp Fallback
- **Fortschrittsverfolgung**: Echtzeit-Übersetzungsfortschritt mit detaillierten Status-Updates
- **Fehlerwiederherstellung**: Robuste Fehlerbehandlung mit eleganten Fallbacks

### 🌍 **Mehrsprachige Unterstützung**

- **Internationalisierte Benutzeroberfläche**: 11 unterstützte UI-Sprachen
- **Automatische Spracherkennung**: Entdeckt alle verfügbaren Untertitelsprachen
- **Breite Übersetzungsunterstützung**: Übersetzt in jede von KI-Modellen unterstützte Sprache

### 📁 **Dateiverwaltung**

- **Automatische Organisation**: Intelligente Dateibenennung und dedizierte Ordnerspeicherung
- **SRT-Format**: Industrie-Standard Untertitelformat für maximale Kompatibilität
- **Ein-Klick-Download**: Einfacher Zugang zu übersetzten Untertiteldateien

## 🛠️ Installation und Einrichtung

### Voraussetzungen

- Python 3.9 oder höher
- OpenAI API-Schlüssel (für KI-Übersetzung erforderlich)
- Moderner Webbrowser (Chrome, Firefox, Safari oder Edge)

### Schnellstart

**1. Repository klonen**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Virtuelle Umgebung erstellen**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Abhängigkeiten installieren**

```bash
pip install -r requirements.txt
```

**4. Umgebung konfigurieren**

Eine `.env`-Datei im Projektverzeichnis erstellen und Ihren OpenAI API-Schlüssel hinzufügen:

```env
# Erforderlich
OPENAI_API_KEY=ihr_openai_api_schlüssel

# Optionale Konfigurationen (Standardwerte angezeigt)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Anwendung starten**

```bash
python run_streamlit.py
```

Die Anwendung öffnet sich automatisch in Ihrem Standard-Browser unter `http://localhost:8501`.

## 🎯 Verwendung

### Grundlegender Workflow

1. **Anwendung starten**: `python run_streamlit.py` ausführen
2. **Video-URL eingeben**: Beliebigen YouTube-Video-Link einfügen
3. **Sprachen auswählen**: Quell- und Zielsprache aus erkannten Optionen wählen
4. **Modelle konfigurieren** (Optional): KI-Modelle für verschiedene Verarbeitungsschritte auswählen
5. **Übersetzung starten**: "KI-Übersetzung starten" klicken und Fortschritt überwachen
6. **Ansehen und Herunterladen**: Übersetztes Video mit synchronisierten Untertiteln genießen und Dateien herunterladen

## ⚙️ Konfiguration

### Umgebungsvariablen

| Variable                        | Beschreibung                         | Standard      |
| ------------------------------- | ------------------------------------ | ------------- |
| `OPENAI_API_KEY`                | OpenAI API-Schlüssel (erforderlich)  | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Untertitel-Dateiverzeichnis          | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Untertitel-Verarbeitungs-Chunk-Größe | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Maximale Wiederholungsversuche       | `2`           |
| `EXTRACTION_MODEL`              | Untertitel-Extraktions-KI-Modell     | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | Übersetzungs-KI-Modell               | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | Kontextgenerierungs-KI-Modell        | `o3-mini`     |

## 🤝 Mitwirken

Wir begrüßen Beiträge! So können Sie anfangen:

1. **Repository forken**: Den "Fork"-Button auf GitHub klicken
2. **Feature-Branch erstellen**: `git checkout -b feature/your-feature-name`
3. **Änderungen implementieren**: Ihre Verbesserungen umsetzen
4. **Gründlich testen**: Überprüfen, dass alle Funktionen ordnungsgemäß funktionieren
5. **Pull Request einreichen**: Detaillierte PR mit Beschreibung erstellen

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe [LICENSE](LICENSE) Datei für Details.

---

<div align="center">
  <p>Mit ❤️ für die globale Gemeinschaft erstellt</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Projekt mit Stern versehen</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Bug melden</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Feature anfordern</a>
  </p>
</div>
