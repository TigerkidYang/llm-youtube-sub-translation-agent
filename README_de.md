<div align="center">
  <h1>🎬 LLM YouTube-Untertitel-Übersetzungsagent 🌍</h1>
  <p>
    Ein fortschrittlicher KI-Agent für hochwertige, kontextsensitive Übersetzung von YouTube-Video-Untertiteln mit LangGraph.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Lizenz: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Probleme"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Willkommen"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Sterne"></a>
  </p>
  <p>
    🌐 Lesen Sie dieses README in anderen Sprachen:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | Deutsch | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Dieses Projekt implementiert einen fortschrittlichen, mehrstufigen KI-Agenten, der die Übersetzung von YouTube-Video-Untertiteln automatisiert. Es verwendet das LangGraph-Framework, um eine robuste und intelligente Pipeline zu erstellen, die über eine einfache Übersetzung hinausgeht, um kontextuelle Konsistenz und hohe Qualität zu gewährleisten.

Der Agent ruft zuerst die Untertitel ab, analysiert den gesamten Text, um ein "Übersetzungsspeicher" (einschließlich Glossar und Styleguide) zu generieren, und übersetzt dann den Inhalt Block für Block, wobei jede Ausgabe validiert wird, bevor das Ergebnis in einer neuen `.srt`-Datei finalisiert wird.

## 📖 Inhaltsverzeichnis

- [✨ Hauptmerkmale](#-hauptmerkmale)
- [🚀 Funktionsweise: Der Agenten-Workflow](#-funktionsweise-der-agenten-workflow)
- [🛠️ Einrichtung und Installation](#️-einrichtung-und-installation)
- [🏃 Ausführung](#-ausführung)
- [🤝 Mitwirken](#-mitwirken)
- [📄 Lizenz](#-lizenz)

## ✨ Hauptmerkmale

-   **Interaktive Einrichtung**: 🗣️ Fordert den Benutzer zur Eingabe des YouTube-Videolinks und der gewünschten Original-/Zielsprachen auf.
-   **Kontextsensitive Übersetzung**: 🧠 Vor der Übersetzung generiert der Agent einen umfassenden Kontextleitfaden (Videobasis, Glossar, Sprachbeschreibungen und Stiltipps), um qualitativ hochwertige, konsistente Übersetzungen zu gewährleisten.
-   **Blockbasierte Verarbeitung**: 🧩 Teilt Untertitel in überschaubare Blöcke für eine effiziente und zuverlässige Verarbeitung durch das Sprachmodell.
-   **Robust und selbstkorrigierend**: 💪 Enthält einen Validierungsschritt, der die übersetzte Ausgabe des LLM auf Formatierungsfehler (wie unerwünschtes Markdown) überprüft und automatisch mit Korrekturanweisungen wiederholt.
-   **Zustandsbehafteter Workflow**: 🔄 Mit `langgraph` erstellt, um den komplexen, mehrstufigen Prozess klar, resilient und beobachtbar zu verwalten.
-   **Automatische Dateiverwaltung**: 📂 Benennt und speichert sowohl die ursprünglichen als auch die endgültig übersetzten `.srt`-Dateien intelligent in einem dedizierten `transcripts`-Verzeichnis.

## 🚀 Funktionsweise: Der Agenten-Workflow

Der Agent arbeitet als Zustandsautomat und durchläuft eine Reihe definierter Schritte, um die Übersetzungsaufgabe abzuschließen.

1.  **Videolink abrufen**: 🔗 Der Agent beginnt damit, den Benutzer nach einer YouTube-Video-URL zu fragen.
2.  **Verfügbare Sprachen auflisten**: 📜 Er ruft die YouTube Transcript API auf, um alle verfügbaren Untertitelsprachen für das Video zu finden und anzuzeigen.
3.  **Sprachauswahl treffen**: 🎯 Der Benutzer wählt die ursprüngliche Untertitelsprache für die Übersetzung aus und gibt die Zielsprache an.
4.  **Untertitel abrufen**: 📥 Ein LLM-gestützter Tool-Agent wird aufgerufen. Er ruft das `fetch_youtube_srt`-Tool korrekt auf, um die ursprünglichen Untertitel herunterzuladen und als `.srt`-Datei zu speichern (z. B. `transcripts/video_id_en.srt`).
5.  **Übersetzung vorbereiten**: ⚙️ Die heruntergeladene `.srt`-Datei wird geparst und ihr Inhalt wird basierend auf der `CHUNK_SIZE` in kleinere, nummerierte Textblöcke aufgeteilt.
6.  **Übersetzungskontext generieren**: 💡 Der Agent sendet den *gesamten* ursprünglichen Untertiteltext an ein LLM, um einen "Übersetzungsspeicher" zu generieren. Dieses wichtige Dokument enthält ein Glossar mit Schlüsselbegriffen, Beschreibungen der Stimmen und Töne der Sprecher sowie Übersetzungstipps, um Konsistenz zu gewährleisten.
7.  **Blöcke übersetzen (Schleife)**: 🔁 Der Agent iteriert durch jeden Textblock.  
    a.  **Übersetzen**: Der aktuelle Block wird zusammen mit dem Übersetzungsspeicher für den Kontext zur Übersetzung an das LLM gesendet.  
    b.  **Validieren**: Die Ausgabe des LLM wird auf Korrektheit überprüft. Insbesondere wird sichergestellt, dass die Ausgabe reiner Text ist und nicht in Markdown-Codeblöcken eingeschlossen ist. Wenn die Validierung fehlschlägt, wiederholt der Agent die Übersetzung bis zu einem definierten Maximum.  
    c.  **Aggregieren**: Der validierte, übersetzte Text wird einer Liste hinzugefügt. Wenn ein Block wiederholt die Validierung nicht besteht, wird der Originaltext als Platzhalter verwendet, um Datenverlust zu vermeiden.  
8.  **Übersetzung abschließen**: ✅ Sobald alle Blöcke übersetzt sind, rekonstruiert der Agent eine vollständige, übersetzte Untertitelliste, konvertiert sie zurück in das SRT-Format und speichert sie in einer neuen Datei (z. B. `transcripts/video_id_en_de.srt`).
9.  **Ende**: 🎉 Der Vorgang ist abgeschlossen.

## 🛠️ Schnellstart

**1. Repository klonen**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Python Virtuelle Umgebung erstellen**

Es wird dringend empfohlen, eine virtuelle Umgebung zu verwenden.

```bash
# Für Windows
python -m venv venv
venv\Scripts\activate

# Für macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Abhängigkeiten installieren**

Installieren Sie alle erforderlichen Python-Pakete aus `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Umgebungsvariablen konfigurieren**

Der Agent benötigt einen API-Schlüssel und andere Konfigurationen.

Benennen Sie zuerst die Beispiel-Umgebungsdatei `.env.example` in `.env` um.

```bash
# Für Windows
rename .env.example .env

# Für macOS/Linux
mv .env.example .env
```

Öffnen Sie als Nächstes die neue `.env`-Datei und fügen Sie Ihren OpenAI-API-Schlüssel hinzu. Die Datei enthält auch optionale Standardwerte, die Sie anpassen können.

```env
# Erforderlich
OPENAI_API_KEY="your_openai_api_key_here"

# Optional: Sie können diese Standardwerte überschreiben
# Ich habe Kommentare in .env.example, um Ihnen zu sagen, was sie sind.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 Ausführung

Führen Sie das Skript `Agent.py` von Ihrem Terminal aus. Der Agent führt Sie interaktiv durch den Prozess.

```bash
python Agent.py
```

Sie werden aufgefordert, den YouTube-Videolink einzugeben und dann die Sprachen auszuwählen. Der Agent zeigt detaillierte Protokolle in der Konsole an, während er jeden Schritt des Workflows ausführt. Nach Abschluss finden Sie die ursprünglichen und übersetzten `.srt`-Dateien im Verzeichnis `transcripts`.

---

## 🤝 Mitwirken

Beiträge sind willkommen! Wenn Sie Verbesserungsvorschläge haben oder Probleme finden, können Sie gerne:

1.  Das Repository forken.
2.  Einen neuen Branch erstellen (`git checkout -b feature/your-feature-name`).
3.  Ihre Änderungen vornehmen.
4.  Ihre Änderungen committen (`git commit -m 'Add some feature'`).
5.  Zum Branch pushen (`git push origin feature/your-feature-name`).
6.  Einen Pull Request öffnen.

Bitte stellen Sie sicher, dass Sie die Tests entsprechend aktualisieren.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details finden Sie in der Datei `LICENSE`, falls diese im Repository enthalten ist, oder beziehen Sie sich auf die [MIT-Lizenzbedingungen](https://opensource.org/licenses/MIT).
