<div align="center">
  <h1>🎬 YTRossetaAI - Ve YouTube en tu idioma 🌍</h1>
  <p>
    Una aplicación web avanzada impulsada por IA para traducción de alta calidad y consciente del contexto de subtítulos de videos de YouTube con integración de reproductor de video en tiempo real.
  </p>
  <p>
    <!-- Insignias -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licencia: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Bienvenidos"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Leer este README en otros idiomas:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Este proyecto proporciona una aplicación web sofisticada para traducir subtítulos de videos de YouTube utilizando tecnología de IA avanzada. Construido con Streamlit y potenciado por LangGraph, ofrece una interfaz intuitiva con reproducción de video en tiempo real, visualización de subtítulos sincronizados y caché inteligente para rendimiento óptimo.

## 🌟 Características Principales

### 🎥 **Experiencia de Video Interactiva**

- **Reproductor de YouTube Integrado**: Ver videos directamente en la app con subtítulos sincronizados
- **Control de Superposición de Subtítulos**: Alternar subtítulos de superposición de video on/off con un clic
- **Sincronización en Tiempo Real**: Los subtítulos se sincronizan automáticamente con la reproducción del video
- **Soporte de Pantalla Completa**: Experiencia de reproductor optimizada para todos los tamaños de pantalla

### 🧠 **Traducción Impulsada por IA**

- **Procesamiento Consciente del Contexto**: Genera memoria de traducción comprensiva incluyendo glosario, análisis de hablantes y directrices de estilo
- **Traducción Basada en Chunks**: Divide inteligentemente los subtítulos en segmentos manejables para precisión
- **Validación de Calidad**: Verificación automática de formato y mecanismos de reintento para salida confiable
- **Múltiples Modelos de IA**: Modelos configurables para extracción, generación de contexto y traducción

### 🚀 **Rendimiento y Confiabilidad**

- **Caché Inteligente**: Detecta y reutiliza automáticamente traducciones existentes
- **Métodos de Extracción Duales**: youtube-transcript-api principal con respaldo yt-dlp
- **Seguimiento de Progreso**: Progreso de traducción en tiempo real con actualizaciones detalladas de estado
- **Recuperación de Errores**: Manejo robusto de errores con respaldos elegantes

### 🌍 **Soporte Multiidioma**

- **Interfaz Internacionalizada**: 11 idiomas de interfaz soportados
- **Detección Automática de Idioma**: Descubre todos los idiomas de subtítulos disponibles
- **Amplio Soporte de Traducción**: Traduce a cualquier idioma soportado por los modelos de IA

### 📁 **Gestión de Archivos**

- **Organización Automática**: Nomenclatura inteligente de archivos y almacenamiento en carpetas dedicadas
- **Formato SRT**: Formato de subtítulos estándar de la industria para máxima compatibilidad
- **Descarga con Un Clic**: Acceso fácil a archivos de subtítulos traducidos

## 🛠️ Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- Clave API de OpenAI (requerida para traducción de IA)
- Navegador web moderno (Chrome, Firefox, Safari o Edge)

### Inicio Rápido

**1. Clonar el Repositorio**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Crear Entorno Virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar Entorno**

Crear un archivo `.env` en la raíz del proyecto y agregar tu clave API de OpenAI:

```env
# Requerido
OPENAI_API_KEY=tu_clave_api_openai

# Configuraciones opcionales (valores por defecto mostrados)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Ejecutar la Aplicación**

```bash
python run_streamlit.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`.

## 🎯 Uso

### Flujo de Trabajo Básico

1. **Iniciar la Aplicación**: Ejecutar `python run_streamlit.py`
2. **Ingresar URL del Video**: Pegar cualquier enlace de video de YouTube
3. **Seleccionar Idiomas**: Elegir idiomas fuente y destino de las opciones detectadas
4. **Configurar Modelos** (Opcional): Seleccionar modelos de IA para diferentes etapas de procesamiento
5. **Iniciar Traducción**: Hacer clic en "Iniciar Traducción IA" y monitorear el progreso
6. **Ver y Descargar**: Disfrutar del video traducido con subtítulos sincronizados y descargar archivos

## ⚙️ Configuración

### Variables de Entorno

| Variable                        | Descripción                                    | Por Defecto   |
| ------------------------------- | ---------------------------------------------- | ------------- |
| `OPENAI_API_KEY`                | Clave API de OpenAI (requerida)                | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Directorio de archivos de subtítulos           | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Tamaño de chunk de procesamiento de subtítulos | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Máximo número de reintentos                    | `2`           |
| `EXTRACTION_MODEL`              | Modelo de IA para extracción de subtítulos     | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | Modelo de IA para traducción                   | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | Modelo de IA para generación de contexto       | `o3-mini`     |

## 🤝 Contribución

¡Damos la bienvenida a las contribuciones! Aquí está cómo empezar:

1. **Hacer Fork del Repositorio**: Hacer clic en el botón "Fork" en GitHub
2. **Crear Rama de Característica**: `git checkout -b feature/your-feature-name`
3. **Implementar Cambios**: Implementar tus mejoras
4. **Probar Exhaustivamente**: Verificar que todas las funcionalidades funcionen correctamente
5. **Enviar Pull Request**: Crear un PR detallado con descripción

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para detalles.

---

<div align="center">
  <p>Hecho con ❤️ para la comunidad global</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Dar estrella al proyecto</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Reportar Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Solicitar Característica</a>
  </p>
</div>
