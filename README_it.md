<div align="center">
  <h1>🎬 Agente di Traduzione Sottotitoli YouTube LLM 🌍</h1>
  <p>
    Un agente AI avanzato per la traduzione di alta qualità e sensibile al contesto dei sottotitoli dei video di YouTube, utilizzando LangGraph.
  </p>
  <p>
    <!-- Badge -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licenza: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Problemi"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PR Benvenuti"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="Stelle GitHub"></a>
  </p>
  <p>
    🌐 Leggi questo README in altre lingue:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | Italiano | <a href="README_ru.md">Русский</a>
  </p>
</div>

Questo progetto implementa un agente AI avanzato multi-step che automatizza la traduzione dei sottotitoli dei video di YouTube. Utilizza il framework LangGraph per creare una pipeline robusta e intelligente che va oltre la semplice traduzione per garantire coerenza contestuale e alta qualità.

L'agente recupera prima i sottotitoli, analizza l'intero testo per generare una "memoria di traduzione" (comprensiva di glossario e guida di stile), quindi traduce il contenuto pezzo per pezzo, convalidando ogni output prima di finalizzare il risultato in un nuovo file `.srt`.

## 📖 Indice dei Contenuti

- [✨ Caratteristiche Principali](#-caratteristiche-principali)
- [🚀 Come Funziona: Il Flusso di Lavoro dell'Agente](#-come-funziona-il-flusso-di-lavoro-dellagente)
- [🛠️ Configurazione e Installazione](#️-configurazione-e-installazione)
- [🏃 Come Eseguire](#-come-eseguire)
- [🤝 Contribuire](#-contribuire)
- [📄 Licenza](#-licenza)

## ✨ Caratteristiche Principali

-   **Configurazione Interattiva**: 🗣️ Chiede all'utente il link del video di YouTube e le lingue di origine/destinazione desiderate.
-   **Traduzione Sensibile al Contesto**: 🧠 Prima di tradurre, l'agente genera una guida contestuale completa (base del video, glossario, descrizioni vocali e consigli di stile) per garantire traduzioni coerenti e di alta qualità.
-   **Elaborazione Basata su Chunk**: 🧩 Divide i sottotitoli in chunk gestibili per un'elaborazione efficiente e affidabile da parte del modello linguistico.
-   **Robusto e Autocorrettivo**: 💪 Include una fase di convalida che controlla l'output tradotto dell'LLM per errori di formattazione (come markdown indesiderato) e riprova automaticamente con istruzioni correttive.
-   **Flusso di Lavoro State-based**: 🔄 Costruito con `langgraph` per gestire il complesso processo multi-step in modo chiaro, resiliente e osservabile.
-   **Gestione Automatica dei File**: 📂 Nomina e salva in modo intelligente sia i file `.srt` originali che quelli finali tradotti in una directory `transcripts` dedicata.

## 🚀 Come Funziona: Il Flusso di Lavoro dell'Agente

L'agente opera come una macchina a stati, muovendosi attraverso una serie di passaggi definiti per completare l'attività di traduzione.

1.  **Ottieni Link Video**: 🔗 L'agente inizia chiedendo all'utente un URL di un video di YouTube.
2.  **Elenca Lingue Disponibili**: 📜 Chiama l'API YouTube Transcript per trovare tutte le lingue dei sottotitoli disponibili per il video e le visualizza.
3.  **Ottieni Scelte Lingua**: 🎯 L'utente seleziona la lingua originale dei sottotitoli da tradurre e specifica la lingua di destinazione.
4.  **Recupera Sottotitoli**: 📥 Viene invocato un agente tool alimentato da LLM. Chiama correttamente lo strumento `fetch_youtube_srt` per scaricare i sottotitoli originali e li salva come file `.srt` (ad es. `transcripts/video_id_en.srt`).
5.  **Prepara per la Traduzione**: ⚙️ Il file `.srt` scaricato viene analizzato e il suo contenuto viene diviso in chunk di testo più piccoli e numerati in base al `CHUNK_SIZE`.
6.  **Genera Contesto di Traduzione**: 💡 L'agente invia l'intero testo dei sottotitoli originali a un LLM per generare una "memoria di traduzione". Questo documento critico contiene un glossario di termini chiave, descrizioni delle voci e dei toni degli oratori e suggerimenti di traduzione per garantire la coerenza.
7.  **Traduci Chunk (Loop)**: 🔁 L'agente itera attraverso ogni chunk di testo.  
    a.  **Traduci**: Il chunk corrente viene inviato all'LLM per la traduzione, insieme alla memoria di traduzione per il contesto.  
    b.  **Convalida**: L'output dell'LLM viene controllato per verificarne la correttezza. In particolare, si assicura che l'output sia testo semplice e non racchiuso in blocchi di codice markdown. Se la convalida fallisce, l'agente riprova la traduzione fino a un massimo definito.  
    c.  **Aggrega**: Il testo tradotto e convalidato viene aggiunto a un elenco. Se un chunk fallisce ripetutamente la convalida, il testo originale viene utilizzato come segnaposto per evitare la perdita di dati.  
8.  **Finalizza Traduzione**: ✅ Una volta tradotti tutti i chunk, l'agente ricostruisce un elenco completo di sottotitoli tradotti, lo riconverte in formato SRT e lo salva in un nuovo file (ad es. `transcripts/video_id_en_it.srt`).
9.  **Fine**: 🎉 Il processo è completo.

## 🛠️ Avvio Rapido

**1. Clona il Repository**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Crea un Ambiente Virtuale Python**

Si consiglia vivamente di utilizzare un ambiente virtuale.

```bash
# Per Windows
python -m venv venv
venv\Scripts\activate

# Per macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Installa Dipendenze**

Installa tutti i pacchetti Python richiesti da `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configura Variabili d'Ambiente**

L'agente richiede una chiave API e altre configurazioni.

Innanzitutto, rinomina il file di ambiente di esempio `.env.example` in `.env`.

```bash
# Per Windows
rename .env.example .env

# Per macOS/Linux
mv .env.example .env
```

Successivamente, apri il nuovo file `.env` e aggiungi la tua chiave API OpenAI. Il file conterrà anche valori predefiniti opzionali che puoi personalizzare.

```env
# Richiesto
OPENAI_API_KEY="your_openai_api_key_here"

# Opzionale: puoi sovrascrivere questi valori predefiniti
# Ho commenti in .env.example per dirti cosa sono.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 Come Eseguire

Esegui lo script `Agent.py` dal tuo terminale. L'agente ti guiderà attraverso il processo in modo interattivo.

```bash
python Agent.py
```

Ti verrà chiesto di inserire il link del video di YouTube e quindi di selezionare le lingue. L'agente visualizzerà log dettagliati nella console durante l'esecuzione di ogni passaggio del flusso di lavoro. Una volta completato, troverai i file `.srt` originali e tradotti nella directory `transcripts`.

---

## 🤝 Contribuire

I contributi sono benvenuti! Se hai idee per miglioramenti o trovi problemi, sentiti libero di:

1.  Eseguire il fork del repository.
2.  Creare un nuovo ramo (`git checkout -b feature/your-feature-name`).
3.  Apportare le modifiche.
4.  Eseguire il commit delle modifiche (`git commit -m 'Add some feature'`).
5.  Eseguire il push al ramo (`git push origin feature/your-feature-name`).
6.  Aprire una Pull Request.

Assicurati di aggiornare i test, se del caso.

## 📄 Licenza

Questo progetto è concesso in licenza con la Licenza MIT. Puoi trovare maggiori dettagli nel file `LICENSE` se incluso nel repository, oppure fare riferimento ai [termini della Licenza MIT](https://opensource.org/licenses/MIT).
