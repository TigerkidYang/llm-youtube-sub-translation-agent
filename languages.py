# Multi-language support for YouTube Subtitle AI Translator

LANGUAGES = {
    "en": {
        "name": "English",
        "page_title": "YouTube Subtitle AI Translator",
        "page_description": "High-quality AI-powered YouTube video subtitle translation tool",
        "language_selector": "Select Interface Language",
        "features": "Features",
        "usage_instructions": "Usage Instructions",
        "features_list": """
        - 🧠 AI context-aware translation
        - 🎯 Terminology consistency guarantee
        - 📝 Multiple subtitle format support
        - 🚀 Intelligent chunk processing
        - ✅ Automatic format validation
        - 🔄 yt-dlp fallback solution
        """,
        "usage_list": """
        1. Enter YouTube video link
        2. Select source subtitle language
        3. Select target translation language
        4. Click start translation
        5. Download translation results
        """,
        "video_link": "YouTube Video Link",
        "video_link_placeholder": "Please enter YouTube video URL",
        "video_link_help": "Supports various YouTube link formats",
        "video_preview": "Video Preview",
        "getting_languages": "Getting available subtitle languages... (will automatically try fallback if issues occur)",
        "found_languages": "Found {count} available subtitle languages",
        "language_settings": "Language Settings",
        "source_language": "Source Subtitle Language",
        "source_language_help": "Select the source subtitle language to translate",
        "target_language": "Target Translation Language",
        "target_language_help": "Select the target language to translate to",
        "auto_generated": "Auto-generated",
        "start_translation": "Start Translation",
        "start_button": "Start AI Translation",
        "initializing": "Initializing translation task...",
        "downloading": "Downloading original subtitles... (using youtube-transcript-api, will auto-switch to yt-dlp if failed)",
        "translation_completed": "Translation completed!",
        "task_completed": "Translation task completed!",
        "subtitle_preview": "Subtitle Preview",
        "translated_content": "Translated subtitle content",
        "download_button": "Download Translated Subtitle File",
        "translated_count": "Translated {count} subtitle entries",
        "file_not_found": "Translation file not found",
        "translation_error": "Error occurred during translation process",
        "translation_failed": "Translation failed",
        "error_occurred": "Error occurred during translation: {error}",
        "error_details": "Error Details",
        "no_subtitles": "This video has no available subtitles",
        "failed_get_languages": "Failed to get subtitle languages: {error}",
        "invalid_url": "Invalid YouTube link, please check URL format",
        "footer": "Built with LangGraph + OpenAI"
    },
    "zh": {
        "name": "简体中文",
        "page_title": "YouTube字幕智能翻译器",
        "page_description": "基于AI的高质量YouTube视频字幕翻译工具",
        "language_selector": "选择界面语言",
        "features": "功能特点",
        "usage_instructions": "使用说明",
        "features_list": """
        - 🧠 AI上下文感知翻译
        - 🎯 术语一致性保证
        - 📝 多种字幕格式支持
        - 🚀 分块智能处理
        - ✅ 自动格式验证
        - 🔄 yt-dlp备用方案
        """,
        "usage_list": """
        1. 输入YouTube视频链接
        2. 选择原始字幕语言
        3. 选择目标翻译语言
        4. 点击开始翻译
        5. 下载翻译结果
        """,
        "video_link": "YouTube视频链接",
        "video_link_placeholder": "请输入YouTube视频URL",
        "video_link_help": "支持各种YouTube链接格式",
        "video_preview": "视频预览",
        "getting_languages": "正在获取可用字幕语言... (如遇问题将自动尝试备用方案)",
        "found_languages": "找到 {count} 种可用字幕语言",
        "language_settings": "语言设置",
        "source_language": "原始字幕语言",
        "source_language_help": "选择要翻译的原始字幕语言",
        "target_language": "目标翻译语言",
        "target_language_help": "选择要翻译成的目标语言",
        "auto_generated": "自动生成",
        "start_translation": "开始翻译",
        "start_button": "开始AI翻译",
        "initializing": "初始化翻译任务...",
        "downloading": "正在下载原始字幕... (使用youtube-transcript-api，如失败将自动切换到yt-dlp)",
        "translation_completed": "翻译完成！",
        "task_completed": "翻译任务完成！",
        "subtitle_preview": "字幕预览",
        "translated_content": "翻译后的字幕内容",
        "download_button": "下载翻译字幕文件",
        "translated_count": "共翻译了 {count} 条字幕",
        "file_not_found": "翻译文件未找到",
        "translation_error": "翻译过程出现错误",
        "translation_failed": "翻译失败",
        "error_occurred": "翻译过程中出现错误: {error}",
        "error_details": "错误详情",
        "no_subtitles": "该视频没有可用的字幕",
        "failed_get_languages": "获取字幕语言失败: {error}",
        "invalid_url": "无效的YouTube链接，请检查URL格式",
        "footer": "基于 LangGraph + OpenAI 构建"
    },
    "zh-TW": {
        "name": "繁體中文",
        "page_title": "YouTube字幕智能翻譯器",
        "page_description": "基於AI的高質量YouTube視頻字幕翻譯工具",
        "language_selector": "選擇介面語言",
        "features": "功能特點",
        "usage_instructions": "使用說明",
        "features_list": """
        - 🧠 AI上下文感知翻譯
        - 🎯 術語一致性保證
        - 📝 多種字幕格式支持
        - 🚀 分塊智能處理
        - ✅ 自動格式驗證
        - 🔄 yt-dlp備用方案
        """,
        "usage_list": """
        1. 輸入YouTube視頻鏈接
        2. 選擇原始字幕語言
        3. 選擇目標翻譯語言
        4. 點擊開始翻譯
        5. 下載翻譯結果
        """,
        "video_link": "YouTube視頻鏈接",
        "video_link_placeholder": "請輸入YouTube視頻URL",
        "video_link_help": "支持各種YouTube鏈接格式",
        "video_preview": "視頻預覽",
        "getting_languages": "正在獲取可用字幕語言... (如遇問題將自動嘗試備用方案)",
        "found_languages": "找到 {count} 種可用字幕語言",
        "language_settings": "語言設置",
        "source_language": "原始字幕語言",
        "source_language_help": "選擇要翻譯的原始字幕語言",
        "target_language": "目標翻譯語言",
        "target_language_help": "選擇要翻譯成的目標語言",
        "auto_generated": "自動生成",
        "start_translation": "開始翻譯",
        "start_button": "開始AI翻譯",
        "initializing": "初始化翻譯任務...",
        "downloading": "正在下載原始字幕... (使用youtube-transcript-api，如失敗將自動切換到yt-dlp)",
        "translation_completed": "翻譯完成！",
        "task_completed": "翻譯任務完成！",
        "subtitle_preview": "字幕預覽",
        "translated_content": "翻譯後的字幕內容",
        "download_button": "下載翻譯字幕文件",
        "translated_count": "共翻譯了 {count} 條字幕",
        "file_not_found": "翻譯文件未找到",
        "translation_error": "翻譯過程出現錯誤",
        "translation_failed": "翻譯失敗",
        "error_occurred": "翻譯過程中出現錯誤: {error}",
        "error_details": "錯誤詳情",
        "no_subtitles": "該視頻沒有可用的字幕",
        "failed_get_languages": "獲取字幕語言失敗: {error}",
        "invalid_url": "無效的YouTube鏈接，請檢查URL格式",
        "footer": "基於 LangGraph + OpenAI 構建"
    },
    "ja": {
        "name": "日本語",
        "page_title": "YouTube字幕AI翻訳ツール",
        "page_description": "AIを活用した高品質なYouTube動画字幕翻訳ツール",
        "language_selector": "インターフェース言語を選択",
        "features": "機能",
        "usage_instructions": "使用方法",
        "features_list": """
        - 🧠 AIコンテキスト認識翻訳
        - 🎯 用語の一貫性保証
        - 📝 複数の字幕形式サポート
        - 🚀 インテリジェントチャンク処理
        - ✅ 自動形式検証
        - 🔄 yt-dlpフォールバック解決策
        """,
        "usage_list": """
        1. YouTubeビデオリンクを入力
        2. ソース字幕言語を選択
        3. ターゲット翻訳言語を選択
        4. 翻訳開始をクリック
        5. 翻訳結果をダウンロード
        """,
        "video_link": "YouTubeビデオリンク",
        "video_link_placeholder": "YouTubeビデオURLを入力してください",
        "video_link_help": "様々なYouTubeリンク形式をサポート",
        "video_preview": "ビデオプレビュー",
        "getting_languages": "利用可能な字幕言語を取得中... (問題が発生した場合は自動的にフォールバックを試行)",
        "found_languages": "{count}の利用可能な字幕言語が見つかりました",
        "language_settings": "言語設定",
        "source_language": "ソース字幕言語",
        "source_language_help": "翻訳するソース字幕言語を選択",
        "target_language": "ターゲット翻訳言語",
        "target_language_help": "翻訳先の言語を選択",
        "auto_generated": "自動生成",
        "start_translation": "翻訳開始",
        "start_button": "AI翻訳を開始",
        "initializing": "翻訳タスクを初期化中...",
        "downloading": "元の字幕をダウンロード中... (youtube-transcript-apiを使用、失敗時は自動的にyt-dlpに切り替え)",
        "translation_completed": "翻訳完了！",
        "task_completed": "翻訳タスク完了！",
        "subtitle_preview": "字幕プレビュー",
        "translated_content": "翻訳された字幕内容",
        "download_button": "翻訳字幕ファイルをダウンロード",
        "translated_count": "{count}の字幕エントリを翻訳しました",
        "file_not_found": "翻訳ファイルが見つかりません",
        "translation_error": "翻訳プロセス中にエラーが発生しました",
        "translation_failed": "翻訳失敗",
        "error_occurred": "翻訳中にエラーが発生しました: {error}",
        "error_details": "エラー詳細",
        "no_subtitles": "このビデオには利用可能な字幕がありません",
        "failed_get_languages": "字幕言語の取得に失敗しました: {error}",
        "invalid_url": "無効なYouTubeリンクです。URL形式を確認してください",
        "footer": "LangGraph + OpenAIで構築"
    },
    "ko": {
        "name": "한국어",
        "page_title": "YouTube 자막 AI 번역기",
        "page_description": "AI 기반 고품질 YouTube 비디오 자막 번역 도구",
        "language_selector": "인터페이스 언어 선택",
        "features": "기능",
        "usage_instructions": "사용 방법",
        "features_list": """
        - 🧠 AI 맥락 인식 번역
        - 🎯 용어 일관성 보장
        - 📝 다양한 자막 형식 지원
        - 🚀 지능형 청크 처리
        - ✅ 자동 형식 검증
        - 🔄 yt-dlp 폴백 솔루션
        """,
        "usage_list": """
        1. YouTube 비디오 링크 입력
        2. 소스 자막 언어 선택
        3. 대상 번역 언어 선택
        4. 번역 시작 클릭
        5. 번역 결과 다운로드
        """,
        "video_link": "YouTube 비디오 링크",
        "video_link_placeholder": "YouTube 비디오 URL을 입력하세요",
        "video_link_help": "다양한 YouTube 링크 형식 지원",
        "video_preview": "비디오 미리보기",
        "getting_languages": "사용 가능한 자막 언어 가져오는 중... (문제 발생 시 자동으로 폴백 시도)",
        "found_languages": "{count}개의 사용 가능한 자막 언어를 찾았습니다",
        "language_settings": "언어 설정",
        "source_language": "소스 자막 언어",
        "source_language_help": "번역할 소스 자막 언어 선택",
        "target_language": "대상 번역 언어",
        "target_language_help": "번역할 대상 언어 선택",
        "auto_generated": "자동 생성",
        "start_translation": "번역 시작",
        "start_button": "AI 번역 시작",
        "initializing": "번역 작업 초기화 중...",
        "downloading": "원본 자막 다운로드 중... (youtube-transcript-api 사용, 실패 시 자동으로 yt-dlp로 전환)",
        "translation_completed": "번역 완료!",
        "task_completed": "번역 작업 완료!",
        "subtitle_preview": "자막 미리보기",
        "translated_content": "번역된 자막 내용",
        "download_button": "번역된 자막 파일 다운로드",
        "translated_count": "{count}개의 자막 항목을 번역했습니다",
        "file_not_found": "번역 파일을 찾을 수 없습니다",
        "translation_error": "번역 과정에서 오류가 발생했습니다",
        "translation_failed": "번역 실패",
        "error_occurred": "번역 중 오류 발생: {error}",
        "error_details": "오류 세부사항",
        "no_subtitles": "이 비디오에는 사용 가능한 자막이 없습니다",
        "failed_get_languages": "자막 언어 가져오기 실패: {error}",
        "invalid_url": "유효하지 않은 YouTube 링크입니다. URL 형식을 확인하세요",
        "footer": "LangGraph + OpenAI로 구축"
    },
    "fr": {
        "name": "Français",
        "page_title": "Traducteur de Sous-titres YouTube IA",
        "page_description": "Outil de traduction de sous-titres vidéo YouTube de haute qualité alimenté par l'IA",
        "language_selector": "Sélectionner la langue de l'interface",
        "features": "Fonctionnalités",
        "usage_instructions": "Instructions d'utilisation",
        "features_list": """
        - 🧠 Traduction consciente du contexte IA
        - 🎯 Garantie de cohérence terminologique
        - 📝 Support de multiples formats de sous-titres
        - 🚀 Traitement intelligent par chunks
        - ✅ Validation automatique du format
        - 🔄 Solution de secours yt-dlp
        """,
        "usage_list": """
        1. Entrez le lien vidéo YouTube
        2. Sélectionnez la langue des sous-titres source
        3. Sélectionnez la langue de traduction cible
        4. Cliquez sur démarrer la traduction
        5. Téléchargez les résultats de traduction
        """,
        "video_link": "Lien Vidéo YouTube",
        "video_link_placeholder": "Veuillez entrer l'URL de la vidéo YouTube",
        "video_link_help": "Supporte divers formats de liens YouTube",
        "video_preview": "Aperçu Vidéo",
        "getting_languages": "Récupération des langues de sous-titres disponibles... (tentative automatique de secours en cas de problème)",
        "found_languages": "Trouvé {count} langues de sous-titres disponibles",
        "language_settings": "Paramètres de Langue",
        "source_language": "Langue des Sous-titres Source",
        "source_language_help": "Sélectionnez la langue des sous-titres source à traduire",
        "target_language": "Langue de Traduction Cible",
        "target_language_help": "Sélectionnez la langue cible pour la traduction",
        "auto_generated": "Généré automatiquement",
        "start_translation": "Démarrer la Traduction",
        "start_button": "Démarrer la Traduction IA",
        "initializing": "Initialisation de la tâche de traduction...",
        "downloading": "Téléchargement des sous-titres originaux... (utilisant youtube-transcript-api, basculera automatiquement vers yt-dlp en cas d'échec)",
        "translation_completed": "Traduction terminée !",
        "task_completed": "Tâche de traduction terminée !",
        "subtitle_preview": "Aperçu des Sous-titres",
        "translated_content": "Contenu des sous-titres traduits",
        "download_button": "Télécharger le Fichier de Sous-titres Traduits",
        "translated_count": "Traduit {count} entrées de sous-titres",
        "file_not_found": "Fichier de traduction non trouvé",
        "translation_error": "Une erreur s'est produite lors du processus de traduction",
        "translation_failed": "Échec de la traduction",
        "error_occurred": "Une erreur s'est produite lors de la traduction : {error}",
        "error_details": "Détails de l'Erreur",
        "no_subtitles": "Cette vidéo n'a pas de sous-titres disponibles",
        "failed_get_languages": "Échec de récupération des langues de sous-titres : {error}",
        "invalid_url": "Lien YouTube invalide, veuillez vérifier le format de l'URL",
        "footer": "Construit avec LangGraph + OpenAI"
    },
    "de": {
        "name": "Deutsch",
        "page_title": "YouTube Untertitel KI-Übersetzer",
        "page_description": "Hochqualitatives KI-betriebenes YouTube-Video-Untertitel-Übersetzungstool",
        "language_selector": "Oberflächensprache auswählen",
        "features": "Funktionen",
        "usage_instructions": "Anweisungen",
        "features_list": """
        - 🧠 KI-kontextbewusste Übersetzung
        - 🎯 Terminologie-Konsistenz-Garantie
        - 📝 Unterstützung mehrerer Untertitelformate
        - 🚀 Intelligente Chunk-Verarbeitung
        - ✅ Automatische Formatvalidierung
        - 🔄 yt-dlp Fallback-Lösung
        """,
        "usage_list": """
        1. YouTube-Video-Link eingeben
        2. Quell-Untertitelsprache auswählen
        3. Ziel-Übersetzungssprache auswählen
        4. Übersetzung starten klicken
        5. Übersetzungsergebnisse herunterladen
        """,
        "video_link": "YouTube-Video-Link",
        "video_link_placeholder": "Bitte geben Sie die YouTube-Video-URL ein",
        "video_link_help": "Unterstützt verschiedene YouTube-Link-Formate",
        "video_preview": "Video-Vorschau",
        "getting_languages": "Verfügbare Untertitelsprachen abrufen... (wird automatisch Fallback versuchen, wenn Probleme auftreten)",
        "found_languages": "{count} verfügbare Untertitelsprachen gefunden",
        "language_settings": "Spracheinstellungen",
        "source_language": "Quell-Untertitelsprache",
        "source_language_help": "Wählen Sie die zu übersetzende Quell-Untertitelsprache aus",
        "target_language": "Ziel-Übersetzungssprache",
        "target_language_help": "Wählen Sie die Zielsprache für die Übersetzung aus",
        "auto_generated": "Automatisch generiert",
        "start_translation": "Übersetzung starten",
        "start_button": "KI-Übersetzung starten",
        "initializing": "Übersetzungsaufgabe initialisieren...",
        "downloading": "Originale Untertitel herunterladen... (mit youtube-transcript-api, wird automatisch zu yt-dlp wechseln, wenn fehlgeschlagen)",
        "translation_completed": "Übersetzung abgeschlossen!",
        "task_completed": "Übersetzungsaufgabe abgeschlossen!",
        "subtitle_preview": "Untertitel-Vorschau",
        "translated_content": "Übersetzte Untertitelinhalte",
        "download_button": "Übersetzte Untertiteldatei herunterladen",
        "translated_count": "{count} Untertiteleinträge übersetzt",
        "file_not_found": "Übersetzungsdatei nicht gefunden",
        "translation_error": "Fehler beim Übersetzungsprozess aufgetreten",
        "translation_failed": "Übersetzung fehlgeschlagen",
        "error_occurred": "Fehler bei der Übersetzung aufgetreten: {error}",
        "error_details": "Fehlerdetails",
        "no_subtitles": "Dieses Video hat keine verfügbaren Untertitel",
        "failed_get_languages": "Abrufen der Untertitelsprachen fehlgeschlagen: {error}",
        "invalid_url": "Ungültiger YouTube-Link, bitte überprüfen Sie das URL-Format",
        "footer": "Erstellt mit LangGraph + OpenAI"
    },
    "es": {
        "name": "Español",
        "page_title": "Traductor de Subtítulos de YouTube IA",
        "page_description": "Herramienta de traducción de subtítulos de video de YouTube de alta calidad impulsada por IA",
        "language_selector": "Seleccionar idioma de interfaz",
        "features": "Características",
        "usage_instructions": "Instrucciones de uso",
        "features_list": """
        - 🧠 Traducción consciente del contexto IA
        - 🎯 Garantía de consistencia terminológica
        - 📝 Soporte para múltiples formatos de subtítulos
        - 🚀 Procesamiento inteligente por fragmentos
        - ✅ Validación automática de formato
        - 🔄 Solución de respaldo yt-dlp
        """,
        "usage_list": """
        1. Ingrese el enlace del video de YouTube
        2. Seleccione el idioma de subtítulos fuente
        3. Seleccione el idioma de traducción objetivo
        4. Haga clic en iniciar traducción
        5. Descargue los resultados de traducción
        """,
        "video_link": "Enlace de Video de YouTube",
        "video_link_placeholder": "Por favor ingrese la URL del video de YouTube",
        "video_link_help": "Soporta varios formatos de enlaces de YouTube",
        "video_preview": "Vista Previa del Video",
        "getting_languages": "Obteniendo idiomas de subtítulos disponibles... (intentará automáticamente respaldo si ocurren problemas)",
        "found_languages": "Encontrados {count} idiomas de subtítulos disponibles",
        "language_settings": "Configuración de Idioma",
        "source_language": "Idioma de Subtítulos Fuente",
        "source_language_help": "Seleccione el idioma de subtítulos fuente para traducir",
        "target_language": "Idioma de Traducción Objetivo",
        "target_language_help": "Seleccione el idioma objetivo para la traducción",
        "auto_generated": "Generado automáticamente",
        "start_translation": "Iniciar Traducción",
        "start_button": "Iniciar Traducción IA",
        "initializing": "Inicializando tarea de traducción...",
        "downloading": "Descargando subtítulos originales... (usando youtube-transcript-api, cambiará automáticamente a yt-dlp si falla)",
        "translation_completed": "¡Traducción completada!",
        "task_completed": "¡Tarea de traducción completada!",
        "subtitle_preview": "Vista Previa de Subtítulos",
        "translated_content": "Contenido de subtítulos traducidos",
        "download_button": "Descargar Archivo de Subtítulos Traducidos",
        "translated_count": "Traducidas {count} entradas de subtítulos",
        "file_not_found": "Archivo de traducción no encontrado",
        "translation_error": "Ocurrió un error durante el proceso de traducción",
        "translation_failed": "Traducción fallida",
        "error_occurred": "Ocurrió un error durante la traducción: {error}",
        "error_details": "Detalles del Error",
        "no_subtitles": "Este video no tiene subtítulos disponibles",
        "failed_get_languages": "Falló la obtención de idiomas de subtítulos: {error}",
        "invalid_url": "Enlace de YouTube inválido, por favor verifique el formato de URL",
        "footer": "Construido con LangGraph + OpenAI"
    },
    "ru": {
        "name": "Русский",
        "page_title": "ИИ-переводчик субтитров YouTube",
        "page_description": "Высококачественный инструмент перевода субтитров видео YouTube на основе ИИ",
        "language_selector": "Выберите язык интерфейса",
        "features": "Возможности",
        "usage_instructions": "Инструкции по использованию",
        "features_list": """
        - 🧠 ИИ-перевод с учетом контекста
        - 🎯 Гарантия терминологической согласованности
        - 📝 Поддержка множественных форматов субтитров
        - 🚀 Интеллектуальная обработка фрагментов
        - ✅ Автоматическая проверка формата
        - 🔄 Резервное решение yt-dlp
        """,
        "usage_list": """
        1. Введите ссылку на видео YouTube
        2. Выберите язык исходных субтитров
        3. Выберите целевой язык перевода
        4. Нажмите начать перевод
        5. Скачайте результаты перевода
        """,
        "video_link": "Ссылка на видео YouTube",
        "video_link_placeholder": "Пожалуйста, введите URL видео YouTube",
        "video_link_help": "Поддерживает различные форматы ссылок YouTube",
        "video_preview": "Предварительный просмотр видео",
        "getting_languages": "Получение доступных языков субтитров... (автоматически попробует резервный вариант при возникновении проблем)",
        "found_languages": "Найдено {count} доступных языков субтитров",
        "language_settings": "Настройки языка",
        "source_language": "Язык исходных субтитров",
        "source_language_help": "Выберите язык исходных субтитров для перевода",
        "target_language": "Целевой язык перевода",
        "target_language_help": "Выберите целевой язык для перевода",
        "auto_generated": "Автоматически сгенерированные",
        "start_translation": "Начать перевод",
        "start_button": "Начать ИИ-перевод",
        "initializing": "Инициализация задачи перевода...",
        "downloading": "Скачивание оригинальных субтитров... (используется youtube-transcript-api, автоматически переключится на yt-dlp при сбое)",
        "translation_completed": "Перевод завершен!",
        "task_completed": "Задача перевода завершена!",
        "subtitle_preview": "Предварительный просмотр субтитров",
        "translated_content": "Переведенное содержимое субтитров",
        "download_button": "Скачать файл переведенных субтитров",
        "translated_count": "Переведено {count} записей субтитров",
        "file_not_found": "Файл перевода не найден",
        "translation_error": "Произошла ошибка в процессе перевода",
        "translation_failed": "Перевод не удался",
        "error_occurred": "Произошла ошибка во время перевода: {error}",
        "error_details": "Детали ошибки",
        "no_subtitles": "У этого видео нет доступных субтитров",
        "failed_get_languages": "Не удалось получить языки субтитров: {error}",
        "invalid_url": "Недействительная ссылка YouTube, пожалуйста, проверьте формат URL",
        "footer": "Создано с помощью LangGraph + OpenAI"
    },
    "it": {
        "name": "Italiano",
        "page_title": "Traduttore di Sottotitoli YouTube IA",
        "page_description": "Strumento di traduzione sottotitoli video YouTube di alta qualità alimentato da IA",
        "language_selector": "Seleziona lingua dell'interfaccia",
        "features": "Caratteristiche",
        "usage_instructions": "Istruzioni per l'uso",
        "features_list": """
        - 🧠 Traduzione IA consapevole del contesto
        - 🎯 Garanzia di coerenza terminologica
        - 📝 Supporto per formati sottotitoli multipli
        - 🚀 Elaborazione intelligente a blocchi
        - ✅ Convalida automatica del formato
        - 🔄 Soluzione di fallback yt-dlp
        """,
        "usage_list": """
        1. Inserisci il link del video YouTube
        2. Seleziona la lingua dei sottotitoli sorgente
        3. Seleziona la lingua di traduzione target
        4. Clicca per iniziare la traduzione
        5. Scarica i risultati della traduzione
        """,
        "video_link": "Link Video YouTube",
        "video_link_placeholder": "Inserisci l'URL del video YouTube",
        "video_link_help": "Supporta vari formati di link YouTube",
        "video_preview": "Anteprima Video",
        "getting_languages": "Ottenimento delle lingue dei sottotitoli disponibili... (proverà automaticamente il fallback se si verificano problemi)",
        "found_languages": "Trovate {count} lingue di sottotitoli disponibili",
        "language_settings": "Impostazioni Lingua",
        "source_language": "Lingua Sottotitoli Sorgente",
        "source_language_help": "Seleziona la lingua dei sottotitoli sorgente da tradurre",
        "target_language": "Lingua di Traduzione Target",
        "target_language_help": "Seleziona la lingua target per la traduzione",
        "auto_generated": "Generato automaticamente",
        "start_translation": "Inizia Traduzione",
        "start_button": "Inizia Traduzione IA",
        "initializing": "Inizializzazione task di traduzione...",
        "downloading": "Download sottotitoli originali... (usando youtube-transcript-api, passerà automaticamente a yt-dlp se fallisce)",
        "translation_completed": "Traduzione completata!",
        "task_completed": "Task di traduzione completato!",
        "subtitle_preview": "Anteprima Sottotitoli",
        "translated_content": "Contenuto sottotitoli tradotti",
        "download_button": "Scarica File Sottotitoli Tradotti",
        "translated_count": "Tradotte {count} voci di sottotitoli",
        "file_not_found": "File di traduzione non trovato",
        "translation_error": "Si è verificato un errore durante il processo di traduzione",
        "translation_failed": "Traduzione fallita",
        "error_occurred": "Si è verificato un errore durante la traduzione: {error}",
        "error_details": "Dettagli Errore",
        "no_subtitles": "Questo video non ha sottotitoli disponibili",
        "failed_get_languages": "Fallito nell'ottenere le lingue dei sottotitoli: {error}",
        "invalid_url": "Link YouTube non valido, controlla il formato URL",
        "footer": "Costruito con LangGraph + OpenAI"
    },
    "pt": {
        "name": "Português",
        "page_title": "Tradutor de Legendas YouTube IA",
        "page_description": "Ferramenta de tradução de legendas de vídeo YouTube de alta qualidade alimentada por IA",
        "language_selector": "Selecionar idioma da interface",
        "features": "Recursos",
        "usage_instructions": "Instruções de uso",
        "features_list": """
        - 🧠 Tradução IA consciente do contexto
        - 🎯 Garantia de consistência terminológica
        - 📝 Suporte para múltiplos formatos de legendas
        - 🚀 Processamento inteligente por chunks
        - ✅ Validação automática de formato
        - 🔄 Solução de fallback yt-dlp
        """,
        "usage_list": """
        1. Digite o link do vídeo YouTube
        2. Selecione o idioma das legendas fonte
        3. Selecione o idioma de tradução alvo
        4. Clique para iniciar tradução
        5. Baixe os resultados da tradução
        """,
        "video_link": "Link do Vídeo YouTube",
        "video_link_placeholder": "Por favor digite a URL do vídeo YouTube",
        "video_link_help": "Suporta vários formatos de links YouTube",
        "video_preview": "Prévia do Vídeo",
        "getting_languages": "Obtendo idiomas de legendas disponíveis... (tentará automaticamente fallback se ocorrerem problemas)",
        "found_languages": "Encontrados {count} idiomas de legendas disponíveis",
        "language_settings": "Configurações de Idioma",
        "source_language": "Idioma das Legendas Fonte",
        "source_language_help": "Selecione o idioma das legendas fonte para traduzir",
        "target_language": "Idioma de Tradução Alvo",
        "target_language_help": "Selecione o idioma alvo para tradução",
        "auto_generated": "Gerado automaticamente",
        "start_translation": "Iniciar Tradução",
        "start_button": "Iniciar Tradução IA",
        "initializing": "Inicializando tarefa de tradução...",
        "downloading": "Baixando legendas originais... (usando youtube-transcript-api, mudará automaticamente para yt-dlp se falhar)",
        "translation_completed": "Tradução concluída!",
        "task_completed": "Tarefa de tradução concluída!",
        "subtitle_preview": "Prévia das Legendas",
        "translated_content": "Conteúdo das legendas traduzidas",
        "download_button": "Baixar Arquivo de Legendas Traduzidas",
        "translated_count": "Traduzidas {count} entradas de legendas",
        "file_not_found": "Arquivo de tradução não encontrado",
        "translation_error": "Ocorreu um erro durante o processo de tradução",
        "translation_failed": "Tradução falhou",
        "error_occurred": "Ocorreu um erro durante a tradução: {error}",
        "error_details": "Detalhes do Erro",
        "no_subtitles": "Este vídeo não tem legendas disponíveis",
        "failed_get_languages": "Falhou ao obter idiomas das legendas: {error}",
        "invalid_url": "Link YouTube inválido, por favor verifique o formato da URL",
        "footer": "Construído com LangGraph + OpenAI"
    }
} 