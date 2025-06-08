<div align="center">
  <h1>🎬 Agente de Traducción de Subtítulos de YouTube LLM 🌍</h1>
  <p>
    Un agente de IA avanzado para la traducción de alta calidad y consciente del contexto de los subtítulos de videos de YouTube, utilizando LangGraph.
  </p>
  <p>
    <!-- Insignias -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licencia: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Problemas"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Bienvenidos"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="Estrellas de GitHub"></a>
  </p>
  <p>
    🌐 Lea este README en otros idiomas:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | Español | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Este proyecto implementa un agente de IA avanzado de múltiples pasos que automatiza la traducción de subtítulos de videos de YouTube. Utiliza el marco LangGraph para crear una canalización robusta e inteligente que va más allá de la simple traducción para garantizar la coherencia contextual y la alta calidad.

El agente primero recupera los subtítulos, analiza el texto completo para generar una "memoria de traducción" (que incluye un glosario y una guía de estilo), y luego traduce el contenido fragmento por fragmento, validando cada salida antes de finalizar el resultado en un nuevo archivo `.srt`.

## 📖 Tabla de Contenidos

- [✨ Características Clave](#-características-clave)
- [🚀 Cómo Funciona: El Flujo de Trabajo del Agente](#-cómo-funciona-el-flujo-de-trabajo-del-agente)
- [🛠️ Configuración e Instalación](#️-configuración-e-instalación)
- [🏃 Cómo Ejecutar](#-cómo-ejecutar)
- [🤝 Contribuir](#-contribuir)
- [📄 Licencia](#-licencia)

## ✨ Características Clave

-   **Configuración Interactiva**: 🗣️ Solicita al usuario el enlace del video de YouTube y los idiomas de origen/destino deseados.
-   **Traducción Consciente del Contexto**: 🧠 Antes de traducir, el agente genera una guía de contexto completa (base del video, glosario, descripciones de voz y consejos de estilo) para garantizar traducciones consistentes y de alta calidad.
-   **Procesamiento Basado en Fragmentos**: 🧩 Divide los subtítulos en fragmentos manejables para un procesamiento eficiente y confiable por parte del modelo de lenguaje.
-   **Robusto y Autocorregible**: 💪 Incluye un paso de validación que verifica la salida traducida del LLM en busca de errores de formato (como markdown no deseado) y reintenta automáticamente con instrucciones correctivas.
-   **Flujo de Trabajo con Estado**: 🔄 Construido con `langgraph` para gestionar el complejo proceso de múltiples pasos de una manera clara, resiliente y observable.
-   **Gestión Automática de Archivos**: 📂 Nombra y guarda de forma inteligente tanto los archivos `.srt` originales como los finales traducidos en un directorio `transcripts` dedicado.

## 🚀 Cómo Funciona: El Flujo de Trabajo del Agente

El agente opera como una máquina de estados, moviéndose a través de una serie de pasos definidos para completar la tarea de traducción.

1.  **Obtener Enlace del Video**: 🔗 El agente comienza pidiendo al usuario una URL de video de YouTube.
2.  **Listar Idiomas Disponibles**: 📜 Llama a la API de YouTube Transcript para encontrar todos los idiomas de subtítulos disponibles para el video y los muestra.
3.  **Obtener Elecciones de Idioma**: 🎯 El usuario selecciona el idioma original de los subtítulos para traducir y especifica el idioma de destino.
4.  **Recuperar Subtítulos**: 📥 Se invoca un agente de herramientas impulsado por LLM. Llama correctamente a la herramienta `fetch_youtube_srt` para descargar los subtítulos originales y los guarda como un archivo `.srt` (por ejemplo, `transcripts/video_id_en.srt`).
5.  **Preparar para la Traducción**: ⚙️ El archivo `.srt` descargado se analiza y su contenido se divide en fragmentos de texto más pequeños y numerados según el `CHUNK_SIZE`.
6.  **Generar Contexto de Traducción**: 💡 El agente envía el texto *completo* de los subtítulos originales a un LLM para generar una "memoria de traducción". Este documento crítico contiene un glosario de términos clave, descripciones de las voces y tonos de los hablantes, y consejos de traducción para garantizar la coherencia.
7.  **Traducir Fragmentos (Bucle)**: 🔁 El agente itera a través de cada fragmento de texto.  
    a.  **Traducir**: El fragmento actual se envía al LLM para la traducción, junto con la memoria de traducción para el contexto. 
    b.  **Validar**: Se comprueba la corrección de la salida del LLM. Específicamente, se asegura de que la salida sea texto sin formato y no esté envuelta en bloques de código markdown. Si la validación falla, el agente reintenta la traducción hasta un máximo definido.  
    c.  **Agregar**: El texto traducido y validado se agrega a una lista. Si un fragmento falla repetidamente la validación, se utiliza el texto original como marcador de posición para evitar la pérdida de datos.  
8.  **Finalizar Traducción**: ✅ Una vez que todos los fragmentos están traducidos, el agente reconstruye una lista completa de subtítulos traducidos, la convierte de nuevo al formato SRT y la guarda en un nuevo archivo (por ejemplo, `transcripts/video_id_en_es.srt`).
9.  **Fin**: 🎉 El proceso está completo.

## 🛠️ Inicio Rápido

**1. Clonar el Repositorio**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Crear un Entorno Virtual de Python**

Se recomienda encarecidamente utilizar un entorno virtual.

```bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar Dependencias**

Instale todos los paquetes de Python necesarios desde `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configurar Variables de Entorno**

El agente requiere una clave API y otras configuraciones.

Primero, cambie el nombre del archivo de entorno de ejemplo `.env.example` a `.env`.

```bash
# Para Windows
rename .env.example .env

# Para macOS/Linux
mv .env.example .env
```

A continuación, abra el nuevo archivo `.env` y agregue su clave API de OpenAI. El archivo también contendrá valores predeterminados opcionales que puede personalizar.

```env
# Requerido
OPENAI_API_KEY="your_openai_api_key_here"

# Opcional: Puede anular estos valores predeterminados
# Tengo comentarios en .env.example para decirle cuáles son.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 Cómo Ejecutar

Ejecute el script `Agent.py` desde su terminal. El agente lo guiará a través del proceso de forma interactiva.

```bash
python Agent.py
```

Se le pedirá que ingrese el enlace del video de YouTube y luego seleccione los idiomas. El agente mostrará registros detallados en la consola a medida que ejecuta cada paso del flujo de trabajo. Una vez finalizado, encontrará los archivos `.srt` originales y traducidos en el directorio `transcripts`.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tiene ideas para mejoras o encuentra algún problema, no dude en:

1.  Hacer un fork del repositorio.
2.  Crear una nueva rama (`git checkout -b feature/your-feature-name`).
3.  Realizar sus cambios.
4.  Confirmar sus cambios (`git commit -m 'Add some feature'`).
5.  Empujar a la rama (`git push origin feature/your-feature-name`).
6.  Abrir una Pull Request.

Asegúrese de actualizar las pruebas según corresponda.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Puede encontrar más detalles en el archivo `LICENSE` si se incluye en el repositorio, o consultar los [términos de la Licencia MIT](https://opensource.org/licenses/MIT).
