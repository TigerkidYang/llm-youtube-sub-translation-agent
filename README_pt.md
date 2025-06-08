<div align="center">
  <h1>🎬 Agente de Tradução de Legendas do YouTube LLM 🌍</h1>
  <p>
    Um agente de IA avançado para tradução de legendas de vídeos do YouTube de alta qualidade e com reconhecimento de contexto, usando LangGraph.
  </p>
  <p>
    <!-- Emblemas -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licença: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Problemas"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Bem-vindos"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="Estrelas do GitHub"></a>
  </p>
  <p>
    🌐 Leia este README em outros idiomas:
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_fr.md">Français</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | Português | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Este projeto implementa um agente de IA avançado de várias etapas que automatiza a tradução de legendas de vídeos do YouTube. Ele usa o framework LangGraph para criar um pipeline robusto e inteligente que vai além da simples tradução para garantir consistência contextual e alta qualidade.

O agente primeiro busca as legendas, analisa o texto completo para gerar uma "memória de tradução" (incluindo um glossário e guia de estilo) e, em seguida, traduz o conteúdo bloco por bloco, validando cada saída antes de finalizar o resultado em um novo arquivo `.srt`.

## 📖 Índice

- [✨ Principais Recursos](#-principais-recursos)
- [🚀 Como Funciona: O Fluxo de Trabalho do Agente](#-como-funciona-o-fluxo-de-trabalho-do-agente)
- [🛠️ Configuração e Instalação](#️-configuração-e-instalação)
- [🏃 Como Executar](#-como-executar)
- [🤝 Contribuindo](#-contribuindo)
- [📄 Licença](#-licença)

## ✨ Principais Recursos

-   **Configuração Interativa**: 🗣️ Solicita ao usuário o link do vídeo do YouTube e os idiomas original/alvo desejados.
-   **Tradução Consciente do Contexto**: 🧠 Antes de traduzir, o agente gera um guia de contexto abrangente (base do vídeo, glossário, descrições de voz e dicas de estilo) para garantir traduções consistentes e de alta qualidade.
-   **Processamento Baseado em Blocos**: 🧩 Divide as legendas em blocos gerenciáveis para processamento eficiente e confiável pelo modelo de linguagem.
-   **Robusto e Autocorretivo**: 💪 Inclui uma etapa de validação que verifica a saída traduzida do LLM em busca de erros de formatação (como markdown indesejado) e tenta novamente automaticamente com instruções corretivas.
-   **Fluxo de Trabalho com Estado**: 🔄 Construído com `langgraph` para gerenciar o complexo processo de várias etapas de forma clara, resiliente e observável.
-   **Gerenciamento Automático de Arquivos**: 📂 Nomeia e salva de forma inteligente os arquivos `.srt` originais e finais traduzidos em um diretório `transcripts` dedicado.

## 🚀 Como Funciona: O Fluxo de Trabalho do Agente

O agente opera como uma máquina de estados, movendo-se através de uma série de etapas definidas para concluir a tarefa de tradução.

1.  **Obter Link do Vídeo**: 🔗 O agente começa pedindo ao usuário um URL de vídeo do YouTube.
2.  **Listar Idiomas Disponíveis**: 📜 Ele chama a API de Transcrição do YouTube para encontrar todos os idiomas de legenda disponíveis para o vídeo e os exibe.
3.  **Obter Escolhas de Idioma**: 🎯 O usuário seleciona o idioma original da legenda para traduzir e especifica o idioma alvo.
4.  **Buscar Legendas**: 📥 Um agente de ferramentas alimentado por LLM é invocado. Ele chama corretamente a ferramenta `fetch_youtube_srt` para baixar as legendas originais e as salva como um arquivo `.srt` (por exemplo, `transcripts/video_id_en.srt`).
5.  **Preparar para Tradução**: ⚙️ O arquivo `.srt` baixado é analisado e seu conteúdo é dividido em blocos de texto menores e numerados com base no `CHUNK_SIZE`.
6.  **Gerar Contexto de Tradução**: 💡 O agente envia o texto *inteiro* da legenda original para um LLM para gerar uma "memória de tradução". Este documento crítico contém um glossário de termos-chave, descrições das vozes e tons dos falantes e dicas de tradução para garantir a consistência.
7.  **Traduzir Blocos (Loop)**: 🔁 O agente itera por cada bloco de texto.  
    a.  **Traduzir**: O bloco atual é enviado ao LLM para tradução, juntamente com a memória de tradução para contexto.  
    b.  **Validar**: A saída do LLM é verificada quanto à correção. Especificamente, garante que a saída seja texto simples e não envolta em blocos de código markdown. Se a validação falhar, o agente tenta novamente a tradução até um máximo definido.  
    c.  **Agregar**: O texto traduzido e validado é adicionado a uma lista. Se um bloco falhar repetidamente na validação, o texto original é usado como um espaço reservado para evitar a perda de dados.  
8.  **Finalizar Tradução**: ✅ Assim que todos os blocos são traduzidos, o agente reconstrói uma lista completa de legendas traduzidas, converte-a de volta para o formato SRT e a salva em um novo arquivo (por exemplo, `transcripts/video_id_en_pt.srt`).
9.  **Fim**: 🎉 O processo está concluído.

## 🛠️ Início Rápido

**1. Clonar o Repositório**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Criar um Ambiente Virtual Python**

É altamente recomendável usar um ambiente virtual.

```bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar Dependências**

Instale todos os pacotes Python necessários de `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configurar Variáveis de Ambiente**

O agente requer uma chave de API e outras configurações.

Primeiro, renomeie o arquivo de ambiente de exemplo `.env.example` para `.env`.

```bash
# Para Windows
rename .env.example .env

# Para macOS/Linux
mv .env.example .env
```

Em seguida, abra o novo arquivo `.env` e adicione sua chave de API OpenAI. O arquivo também conterá valores padrão opcionais que você pode personalizar.

```env
# Obrigatório
OPENAI_API_KEY="your_openai_api_key_here"

# Opcional: Você pode substituir esses valores padrão
# Tenho comentários em .env.example para dizer o que são.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 Como Executar

Execute o script `Agent.py` do seu terminal. O agente o guiará pelo processo interativamente.

```bash
python Agent.py
```

Você será solicitado a inserir o link do vídeo do YouTube e, em seguida, selecionar os idiomas. O agente exibirá logs detalhados no console à medida que executa cada etapa do fluxo de trabalho. Após a conclusão, você encontrará os arquivos `.srt` originais e traduzidos no diretório `transcripts`.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você tiver ideias para melhorias ou encontrar algum problema, sinta-se à vontade para:

1.  Fazer um fork do repositório.
2.  Criar uma nova branch (`git checkout -b feature/your-feature-name`).
3.  Fazer suas alterações.
4.  Confirmar suas alterações (`git commit -m 'Add some feature'`).
5.  Enviar para a branch (`git push origin feature/your-feature-name`).
6.  Abrir um Pull Request.

Certifique-se de atualizar os testes conforme apropriado.

## 📄 Licença

Este projeto é licenciado sob a Licença MIT. Você pode encontrar mais detalhes no arquivo `LICENSE` se um estiver incluído no repositório, ou consulte os [termos da Licença MIT](https://opensource.org/licenses/MIT).
