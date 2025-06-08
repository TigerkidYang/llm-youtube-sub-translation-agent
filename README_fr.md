<div align="center">
  <h1>🎬 Agent de Traduction de Sous-titres YouTube LLM 🌍</h1>
  <p>
    Un agent IA avancé pour la traduction de haute qualité et sensible au contexte des sous-titres de vidéos YouTube, utilisant LangGraph.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Lisez ce README dans d'autres langues :
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | Français | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Ce projet met en œuvre un agent IA avancé, multi-étapes, qui automatise la traduction des sous-titres de vidéos YouTube. Il utilise le framework LangGraph pour créer un pipeline robuste et intelligent qui va au-delà de la simple traduction pour garantir la cohérence contextuelle et une haute qualité.

L'agent récupère d'abord les sous-titres, analyse le texte intégral pour générer une "mémoire de traduction" (comprenant un glossaire et un guide de style), puis traduit le contenu morceau par morceau, en validant chaque sortie avant de finaliser le résultat dans un nouveau fichier `.srt`.

## 📖 Table des Matières

- [✨ Fonctionnalités Clés](#-fonctionnalités-clés)
- [🚀 Comment Ça Marche : Le Flux de Travail de l'Agent](#-comment-Ça-marche--le-flux-de-travail-de-lagent)
- [🛠️ Configuration et Installation](#️-configuration-et-installation)
- [🏃 Comment Exécuter](#-comment-exécuter)
- [🤝 Contribuer](#-contribuer)
- [📄 Licence](#-licence)

## ✨ Fonctionnalités Clés

-   **Configuration Interactive** : 🗣️ Invite l'utilisateur à fournir le lien de la vidéo YouTube et les langues source/cible souhaitées.
-   **Traduction Sensible au Contexte** : 🧠 Avant de traduire, l'agent génère un guide contextuel complet (base de la vidéo, glossaire, descriptions des voix et conseils de style) pour garantir des traductions de haute qualité et cohérentes.
-   **Traitement par Morceaux** : 🧩 Divise les sous-titres en morceaux gérables pour un traitement efficace et fiable par le modèle linguistique.
-   **Robuste et Auto-Correcteur** : 💪 Comprend une étape de validation qui vérifie les erreurs de formatage dans la sortie traduite du LLM (comme le markdown indésirable) et relance automatiquement avec des instructions correctives.
-   **Flux de Travail à États** : 🔄 Construit avec `langgraph` pour gérer le processus complexe multi-étapes de manière claire, résiliente et observable.
-   **Gestion Automatique des Fichiers** : 📂 Nomme et enregistre intelligemment les fichiers `.srt` originaux et traduits finaux dans un répertoire `transcripts` dédié.

## 🚀 Comment Ça Marche : Le Flux de Travail de l'Agent

L'agent fonctionne comme une machine à états, passant par une série d'étapes définies pour accomplir la tâche de traduction.

1.  **Obtenir le Lien de la Vidéo** : 🔗 L'agent commence par demander à l'utilisateur une URL de vidéo YouTube.
2.  **Lister les Langues Disponibles** : 📜 Il appelle l'API YouTube Transcript pour trouver toutes les langues de sous-titres disponibles pour la vidéo et les affiche.
3.  **Obtenir les Choix de Langue** : 🎯 L'utilisateur sélectionne la langue des sous-titres originaux à traduire et spécifie la langue cible.
4.  **Récupérer les Sous-titres** : 📥 Un agent outil alimenté par LLM est invoqué. Il appelle correctement l'outil `fetch_youtube_srt` pour télécharger les sous-titres originaux et les enregistre sous forme de fichier `.srt` (par exemple, `transcripts/video_id_en.srt`).
5.  **Préparer la Traduction** : ⚙️ Le fichier `.srt` téléchargé est analysé et son contenu est divisé en petits morceaux de texte numérotés en fonction de la `CHUNK_SIZE`.
6.  **Générer le Contexte de Traduction** : 💡 L'agent envoie le texte *entier* des sous-titres originaux à un LLM pour générer une "mémoire de traduction". Ce document essentiel contient un glossaire des termes clés, des descriptions des voix et des tons des locuteurs, ainsi que des conseils de traduction pour garantir la cohérence.
7.  **Traduire les Morceaux (Boucle)** : 🔁 L'agent parcourt chaque morceau de texte.  
    a.  **Traduire** : Le morceau actuel est envoyé au LLM pour traduction, accompagné de la mémoire de traduction pour le contexte.  
    b.  **Valider** : La sortie du LLM est vérifiée pour son exactitude. Plus précisément, il s'assure que la sortie est du texte brut et non enveloppée dans des blocs de code markdown. Si la validation échoue, l'agent réessaie la traduction jusqu'à un maximum défini.  
    c.  **Agréger** : Le texte traduit et validé est ajouté à une liste. Si un morceau échoue de manière répétée à la validation, le texte original est utilisé comme substitut pour éviter la perte de données.  
8.  **Finaliser la Traduction** : ✅ Une fois tous les morceaux traduits, l'agent reconstruit une liste complète de sous-titres traduits, la reconvertit au format SRT et l'enregistre dans un nouveau fichier (par exemple, `transcripts/video_id_en_fr.srt`).
9.  **Fin** : 🎉 Le processus est terminé.

## 🛠️ Démarrage Rapide

**1. Cloner le Dépôt**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Créer un Environnement Virtuel Python**

Il est fortement recommandé d'utiliser un environnement virtuel.

```bash
# Pour Windows
python -m venv venv
venv\Scripts\activate

# Pour macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Installer les Dépendances**

Installez tous les paquets Python requis à partir de `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configurer les Variables d'Environnement**

L'agent nécessite une clé API et d'autres configurations.

Tout d'abord, renommez le fichier d'environnement d'exemple `.env.example` en `.env`.

```bash
# Pour Windows
rename .env.example .env

# Pour macOS/Linux
mv .env.example .env
```

Ensuite, ouvrez le nouveau fichier `.env` et ajoutez votre clé API OpenAI. Le fichier contiendra également des valeurs par défaut facultatives que vous pouvez personnaliser.

```env
# Requis
OPENAI_API_KEY="your_openai_api_key_here"

# Facultatif : Vous pouvez remplacer ces valeurs par défaut
# J'ai des commentaires dans .env.example pour vous dire ce qu'elles sont.
TRANSCRIPT_OUTPUT_DIR="transcripts"
AGENT_CHUNK_SIZE="50"
AGENT_MAX_TRANSLATION_RETRIES="2"
YOUTUBE_API_MAX_RETRIES="20"
YOUTUBE_API_RETRY_DELAY_SECONDS="3"
EXTRACTION_MODEL="o3-mini"
TRANSLATION_MODEL="o3-mini"
```

## 🏃 Comment Exécuter

Exécutez le script `Agent.py` depuis votre terminal. L'agent vous guidera à travers le processus de manière interactive.

```bash
python Agent.py
```

Vous serez invité à entrer le lien de la vidéo YouTube, puis à sélectionner les langues. L'agent affichera des journaux détaillés dans la console à mesure qu'il exécute chaque étape du flux de travail. Une fois terminé, vous trouverez les fichiers `.srt` originaux et traduits dans le répertoire `transcripts`.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations ou si vous trouvez des problèmes, n'hésitez pas à :

1.  Forker le dépôt.
2.  Créer une nouvelle branche (`git checkout -b feature/your-feature-name`).
3.  Effectuer vos modifications.
4.  Valider vos modifications (`git commit -m 'Add some feature'`).
5.  Pousser vers la branche (`git push origin feature/your-feature-name`).
6.  Ouvrir une Pull Request.

Veuillez vous assurer de mettre à jour les tests le cas échéant.

## 📄 Licence

Ce projet est sous licence MIT. Vous trouverez plus de détails dans le fichier `LICENSE` s'il est inclus dans le dépôt, ou reportez-vous aux [termes de la licence MIT](https://opensource.org/licenses/MIT).
