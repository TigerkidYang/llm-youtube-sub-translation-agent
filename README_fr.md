<div align="center">
  <h1>🎬 Traducteur IA de Sous-titres YouTube 🌍</h1>
  <p>
    Une application web avancée alimentée par l'IA pour la traduction de haute qualité et contextuelle des sous-titres vidéo YouTube avec intégration de lecteur vidéo en temps réel.
  </p>
  <p>
    <!-- Badges -->
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.46%2B-FF6B6B.svg" alt="Streamlit 1.46+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licence : MIT"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues"><img src="https://img.shields.io/github/issues/tigerkidyang/llm-youtube-sub-translation-agent" alt="Issues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Bienvenues"></a>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/stargazers"><img src="https://img.shields.io/github/stars/tigerkidyang/llm-youtube-sub-translation-agent?style=social" alt="GitHub Stars"></a>
  </p>
  <p>
    🌐 Lire ce README dans d'autres langues :
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a> | <a href="README_zh_TW.md">繁體中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a> | <a href="README_de.md">Deutsch</a> | <a href="README_es.md">Español</a> | <a href="README_pt.md">Português</a> | <a href="README_it.md">Italiano</a> | <a href="README_ru.md">Русский</a>
  </p>
</div>

Ce projet fournit une application web sophistiquée pour traduire les sous-titres de vidéos YouTube en utilisant une technologie IA avancée. Construit avec Streamlit et alimenté par LangGraph, il offre une interface intuitive avec lecture vidéo en temps réel, affichage de sous-titres synchronisés et mise en cache intelligente pour des performances optimales.

## 🌟 Fonctionnalités Principales

### 🎥 **Expérience Vidéo Interactive**

- **Lecteur YouTube Intégré** : Regardez des vidéos directement dans l'app avec sous-titres synchronisés
- **Contrôle de Superposition de Sous-titres** : Basculez les sous-titres de superposition vidéo on/off en un clic
- **Synchronisation Temps Réel** : Les sous-titres se synchronisent automatiquement avec la lecture vidéo
- **Support Plein Écran** : Expérience de lecteur optimisée pour toutes les tailles d'écran

### 🧠 **Traduction Alimentée par l'IA**

- **Traitement Contextuel** : Génère une mémoire de traduction complète incluant glossaire, analyse des locuteurs et directives stylistiques
- **Traduction par Chunks** : Divise intelligemment les sous-titres en segments gérables pour la précision
- **Validation Qualité** : Vérification automatique de format et mécanismes de nouvelle tentative pour une sortie fiable
- **Modèles IA Multiples** : Modèles configurables pour extraction, génération de contexte et traduction

### 🚀 **Performance et Fiabilité**

- **Cache Intelligent** : Détecte et réutilise automatiquement les traductions existantes
- **Méthodes d'Extraction Duales** : youtube-transcript-api principal avec sauvegarde yt-dlp
- **Suivi de Progression** : Progression de traduction en temps réel avec mises à jour détaillées du statut
- **Récupération d'Erreur** : Gestion d'erreurs robuste avec sauvegardes élégantes

### 🌍 **Support Multilingue**

- **Interface Internationalisée** : 11 langues d'interface supportées
- **Détection Automatique de Langue** : Découvre toutes les langues de sous-titres disponibles
- **Support de Traduction Large** : Traduit vers toute langue supportée par les modèles IA

### 📁 **Gestion de Fichiers**

- **Organisation Automatique** : Nommage de fichiers intelligent et stockage en dossiers dédiés
- **Format SRT** : Format de sous-titres standard industriel pour compatibilité maximale
- **Téléchargement en Un Clic** : Accès facile aux fichiers de sous-titres traduits

## 🛠️ Installation et Configuration

### Prérequis

- Python 3.9 ou supérieur
- Clé API OpenAI (requise pour la traduction IA)
- Navigateur web moderne (Chrome, Firefox, Safari ou Edge)

### Démarrage Rapide

**1. Cloner le Dépôt**

```bash
git clone https://github.com/tigerkidyang/llm-youtube-sub-translation-agent.git
cd llm-youtube-sub-translation-agent
```

**2. Créer un Environnement Virtuel**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Installer les Dépendances**

```bash
pip install -r requirements.txt
```

**4. Configurer l'Environnement**

Créer un fichier `.env` dans la racine du projet et ajouter votre clé API OpenAI :

```env
# Requis
OPENAI_API_KEY=votre_clé_api_openai

# Configurations optionnelles (valeurs par défaut affichées)
TRANSCRIPT_OUTPUT_DIR=transcripts
AGENT_CHUNK_SIZE=50
AGENT_MAX_TRANSLATION_RETRIES=2
YOUTUBE_API_MAX_RETRIES=1
YOUTUBE_API_RETRY_DELAY_SECONDS=3
EXTRACTION_MODEL=gpt-4.1
TRANSLATION_MODEL=gpt-4.1
CONTEXT_MODEL=o3-mini
```

**5. Lancer l'Application**

```bash
python run_streamlit.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à `http://localhost:8501`.

## 🎯 Utilisation

### Flux de Travail de Base

1. **Démarrer l'Application** : Exécuter `python run_streamlit.py`
2. **Entrer l'URL Vidéo** : Coller tout lien de vidéo YouTube
3. **Sélectionner les Langues** : Choisir les langues source et cible parmi les options détectées
4. **Configurer les Modèles** (Optionnel) : Sélectionner les modèles IA pour différentes étapes de traitement
5. **Commencer la Traduction** : Cliquer "Commencer la Traduction IA" et surveiller la progression
6. **Regarder et Télécharger** : Profiter de la vidéo traduite avec sous-titres synchronisés et télécharger les fichiers

## ⚙️ Configuration

### Variables d'Environnement

| Variable                        | Description                            | Défaut        |
| ------------------------------- | -------------------------------------- | ------------- |
| `OPENAI_API_KEY`                | Clé API OpenAI (requis)                | -             |
| `TRANSCRIPT_OUTPUT_DIR`         | Répertoire des fichiers de sous-titres | `transcripts` |
| `AGENT_CHUNK_SIZE`              | Taille des chunks de traitement        | `50`          |
| `AGENT_MAX_TRANSLATION_RETRIES` | Nombre max de nouvelles tentatives     | `2`           |
| `EXTRACTION_MODEL`              | Modèle IA d'extraction de sous-titres  | `gpt-4.1`     |
| `TRANSLATION_MODEL`             | Modèle IA de traduction                | `gpt-4.1`     |
| `CONTEXT_MODEL`                 | Modèle IA de génération de contexte    | `o3-mini`     |

## 🤝 Contribution

Nous accueillons les contributions ! Voici comment commencer :

1. **Forker le Dépôt** : Cliquer le bouton "Fork" sur GitHub
2. **Créer une Branche Fonctionnalité** : `git checkout -b feature/your-feature-name`
3. **Implémenter les Changements** : Implémenter vos améliorations
4. **Tester Soigneusement** : Vérifier que toutes les fonctionnalités marchent
5. **Soumettre une Pull Request** : Créer une PR détaillée avec description

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour les détails.

---

<div align="center">
  <p>Fait avec ❤️ pour la communauté mondiale</p>
  <p>
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent">⭐ Mettre une étoile au projet</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">🐛 Signaler un Bug</a> •
    <a href="https://github.com/tigerkidyang/llm-youtube-sub-translation-agent/issues">💡 Demander une Fonctionnalité</a>
  </p>
</div>
