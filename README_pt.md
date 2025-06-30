<div align="center">
  <h1>🎬 Tradutor IA de Legendas do YouTube 🌍</h1>
  <p>
    Uma aplicação web avançada alimentada por IA para tradução de alta qualidade e consciente do contexto de legendas de vídeos do YouTube com integração de player de vídeo em tempo real.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licença: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Bem-vindos"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Ler este README em outros idiomas:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Este projeto fornece uma aplicação web sofisticada para traduzir legendas de vídeos do YouTube usando tecnologia de IA avançada. Construído com Streamlit e alimentado pelo LangGraph, oferece uma interface intuitiva com reprodução de vídeo em tempo real, exibição de legendas sincronizadas e cache inteligente para desempenho ótimo.

## 🌟 Características Principais

### 🎥 **Experiência de Vídeo Interativa**

- **Player YouTube Incorporado**: Assistir vídeos diretamente no app com legendas sincronizadas
- **Controle de Sobreposição de Legendas**: Alternar legendas de sobreposição de vídeo on/off com um clique
- **Sincronização em Tempo Real**: Legendas sincronizam automaticamente com a reprodução do vídeo
- **Suporte Tela Cheia**: Experiência de player otimizada para todos os tamanhos de tela

### 🧠 **Tradução Alimentada por IA**

- **Processamento Consciente do Contexto**: Gera memória de tradução abrangente incluindo glossário, análise de falantes e diretrizes de estilo
- **Tradução Baseada em Chunks**: Divide inteligentemente as legendas em segmentos gerenciáveis para precisão
- **Validação de Qualidade**: Verificação automática de formato e mecanismos de nova tentativa para saída confiável
- **Múltiplos Modelos de IA**: Modelos configuráveis para extração, geração de contexto e tradução

### 🚀 **Desempenho e Confiabilidade**

- **Cache Inteligente**: Detecta e reutiliza automaticamente traduções existentes
- **Métodos de Extração Duplos**: youtube-transcript-api principal com backup yt-dlp
- **Rastreamento de Progresso**: Progresso de tradução em tempo real com atualizações detalhadas de status
- **Recuperação de Erro**: Tratamento robusto de erros com backups elegantes

### 🌍 **Suporte Multi-idioma**

- **Interface Internacionalizada**: 11 idiomas de interface suportados
- **Detecção Automática de Idioma**: Descobre todos os idiomas de legendas disponíveis
- **Amplo Suporte de Tradução**: Traduz para qualquer idioma suportado pelos modelos de IA

### 📁 **Gestão de Arquivos**

- **Organização Automática**: Nomenclatura inteligente de arquivos e armazenamento em pastas dedicadas
- **Formato SRT**: Formato de legendas padrão da indústria para máxima compatibilidade
- **Download com Um Clique**: Acesso fácil a arquivos de legendas traduzidas

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- Chave API OpenAI (necessária para tradução IA)
- Navegador web moderno (Chrome, Firefox, Safari ou Edge)

### Início Rápido

**1. Clonar o Repositório**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Criar Ambiente Virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar Dependências**

```bash
pip install -r requirements.txt
```

**4. Configurar Ambiente**

Criar um arquivo `.env` na raiz do projeto e adicionar sua chave API OpenAI:

```env
# Obrigatório
OPENAI_API_KEY=sua_chave_api_openai

# Configurações opcionais (valores padrão mostrados)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Executar a Aplicação**

```bash
python run_streamlit.py
```

A aplicação abrirá automaticamente no seu navegador padrão em `http://localhost:8501`.

## 🎯 Uso

### Fluxo de Trabalho Básico

1. **Iniciar a Aplicação**: Executar `python run_streamlit.py`
2. **Inserir URL do Vídeo**: Colar qualquer link de vídeo do YouTube
3. **Selecionar Idiomas**: Escolher idiomas fonte e destino das opções detectadas
4. **Configurar Modelos** (Opcional): Selecionar modelos de IA para diferentes etapas de processamento
5. **Iniciar Tradução**: Clicar em "Iniciar Tradução IA" e monitorar o progresso
6. **Assistir e Baixar**: Desfrutar do vídeo traduzido com legendas sincronizadas e baixar arquivos

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável                        | Descrição                                     | Padrão        |
| ------------------------------- | --------------------------------------------- | ------------- |
| `OPENAI_API_KEY`                | Chave API OpenAI (obrigatório)                | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Diretório de arquivos de legendas             | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Tamanho do chunk de processamento de legendas | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Número máximo de tentativas                   | `2`           |
| `EXTRACTION_MODEL`              | Modelo IA para extração de legendas           | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | Modelo IA para tradução                       | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | Modelo IA para geração de contexto            | `o3-mini`     |

## 🤝 Contribuição

Damos as boas-vindas a contribuições! Aqui está como começar:

1. **Fazer Fork do Repositório**: Clicar no botão "Fork" no GitHub
2. **Criar Branch de Feature**: `git checkout -b feature/your-feature-name`
3. **Implementar Mudanças**: Implementar suas melhorias
4. **Testar Completamente**: Verificar que todas as funcionalidades funcionam corretamente
5. **Enviar Pull Request**: Criar um PR detalhado com descrição

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  <p>Feito com ❤️ para a comunidade global</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Dar estrela ao projeto</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Reportar Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Solicitar Feature</a>
  </p>
</div>
