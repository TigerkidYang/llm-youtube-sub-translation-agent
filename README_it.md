<div align="center">
  <h1>🎬 Traduttore IA di Sottotitoli YouTube 🌍</h1>
  <p>
    Un'applicazione web avanzata alimentata dall'IA per la traduzione di alta qualità e consapevole del contesto dei sottotitoli video di YouTube con integrazione del lettore video in tempo reale.
  </p>
  <p>
    <!-- Badge -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licenza: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PR Benvenute"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Leggi questo README in altre lingue:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Questo progetto fornisce un'applicazione web sofisticata per tradurre i sottotitoli dei video di YouTube utilizzando tecnologia IA avanzata. Costruito con Streamlit e alimentato da LangGraph, offre un'interfaccia intuitiva con riproduzione video in tempo reale, visualizzazione sincronizzata dei sottotitoli e cache intelligente per prestazioni ottimali.

## 🌟 Caratteristiche Principali

### 🎥 **Esperienza Video Interattiva**

- **Lettore YouTube Integrato**: Guardare video direttamente nell'app con sottotitoli sincronizzati
- **Controllo Overlay Sottotitoli**: Attivare/disattivare l'overlay dei sottotitoli video con un clic
- **Sincronizzazione in Tempo Reale**: I sottotitoli si sincronizzano automaticamente con la riproduzione video
- **Supporto Schermo Intero**: Esperienza lettore ottimizzata per tutte le dimensioni dello schermo

### 🧠 **Traduzione Alimentata dall'IA**

- **Elaborazione Consapevole del Contesto**: Genera memoria di traduzione completa inclusi glossario, analisi dei parlanti e linee guida di stile
- **Traduzione Basata su Chunk**: Divide intelligentemente i sottotitoli in segmenti gestibili per precisione
- **Validazione Qualità**: Controllo automatico del formato e meccanismi di ripetizione per output affidabile
- **Modelli IA Multipli**: Modelli configurabili per estrazione, generazione di contesto e traduzione

### 🚀 **Prestazioni e Affidabilità**

- **Cache Intelligente**: Rileva e riutilizza automaticamente le traduzioni esistenti
- **Metodi di Estrazione Duali**: youtube-transcript-api principale con backup yt-dlp
- **Tracciamento Progresso**: Progresso traduzione in tempo reale con aggiornamenti dettagliati dello stato
- **Recupero Errori**: Gestione robusta degli errori con backup eleganti

### 🌍 **Supporto Multi-lingua**

- **Interfaccia Internazionalizzata**: 11 lingue interfaccia supportate
- **Rilevamento Automatico Lingua**: Scopre tutte le lingue sottotitoli disponibili
- **Ampio Supporto Traduzione**: Traduce in qualsiasi lingua supportata dai modelli IA

### 📁 **Gestione File**

- **Organizzazione Automatica**: Denominazione intelligente file e archiviazione cartelle dedicate
- **Formato SRT**: Formato sottotitoli standard industriale per massima compatibilità
- **Download Un Clic**: Accesso facile ai file sottotitoli tradotti

## 🛠️ Installazione e Configurazione

### Prerequisiti

- Python 3.9 o superiore
- Chiave API OpenAI (richiesta per traduzione IA)
- Browser web moderno (Chrome, Firefox, Safari o Edge)

### Avvio Rapido

**1. Clonare il Repository**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Creare Ambiente Virtuale**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Installare Dipendenze**

```bash
pip install -r requirements.txt
```

**4. Configurare Ambiente**

Creare un file `.env` nella radice del progetto e aggiungere la chiave API OpenAI:

```env
# Richiesto
OPENAI_API_KEY=la_tua_chiave_api_openai

# Configurazioni opzionali (valori predefiniti mostrati)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Eseguire l'Applicazione**

```bash
python run_streamlit.py
```

L'applicazione si aprirà automaticamente nel tuo browser predefinito su `http://localhost:8501`.

## 🎯 Utilizzo

### Flusso di Lavoro Base

1. **Avviare l'Applicazione**: Eseguire `python run_streamlit.py`
2. **Inserire URL Video**: Incollare qualsiasi link video YouTube
3. **Selezionare Lingue**: Scegliere lingue sorgente e destinazione dalle opzioni rilevate
4. **Configurare Modelli** (Opzionale): Selezionare modelli IA per diverse fasi di elaborazione
5. **Iniziare Traduzione**: Fare clic su "Inizia Traduzione IA" e monitorare il progresso
6. **Guardare e Scaricare**: Godersi il video tradotto con sottotitoli sincronizzati e scaricare file

## ⚙️ Configurazione

### Variabili Ambiente

| Variabile                       | Descrizione                               | Predefinito   |
| ------------------------------- | ----------------------------------------- | ------------- |
| `OPENAI_API_KEY`                | Chiave API OpenAI (richiesta)             | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Directory file sottotitoli                | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Dimensione chunk elaborazione sottotitoli | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Numero massimo tentativi                  | `2`           |
| `EXTRACTION_MODEL`              | Modello IA estrazione sottotitoli         | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | Modello IA traduzione                     | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | Modello IA generazione contesto           | `o3-mini`     |

## 🤝 Contribuzione

Accogliamo contribuzioni! Ecco come iniziare:

1. **Fare Fork del Repository**: Fare clic sul pulsante "Fork" su GitHub
2. **Creare Branch Feature**: `git checkout -b feature/your-feature-name`
3. **Implementare Modifiche**: Implementare i tuoi miglioramenti
4. **Testare Accuratamente**: Verificare che tutte le funzionalità funzionino correttamente
5. **Inviare Pull Request**: Creare un PR dettagliato con descrizione

## 📄 Licenza

Questo progetto è concesso in licenza sotto la Licenza MIT. Vedere il file [LICENSE](LICENSE) per i dettagli.

---

<div align="center">
  <p>Fatto con ❤️ per la comunità globale</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Dai una stella al progetto</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Segnala Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Richiedi Feature</a>
  </p>
</div>
