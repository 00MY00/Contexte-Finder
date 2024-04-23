# Contexte-Finder



# Project Vector Finder

![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue.svg)
![Windows](https://img.shields.io/badge/Windows-compatible-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)
![Milvus](https://img.shields.io/badge/Milvus-v2.4.0--rc.1-blue.svg)

## Objectifs du projet

Ce projet vise à développer un script Python capable de transformer des mots extraits de textes en vecteurs et de les stocker dans Milvus, une base de données vectorielle. Le système permet de retrouver les fichiers les plus pertinents en fonction des requêtes des utilisateurs, en comparant les vecteurs générés à ceux stockés dans la base de données, sans utiliser de modèles de langage à grande échelle (LLM).

## Fonctionnalités

- **Extraction de contexte** : Récupère les mots clés du texte pour contextualiser la recherche.
- **Transformation en vecteurs** : Convertit les mots en vecteurs utilisables pour la recherche vectorielle.
- **Stockage et requête** : Utilise Milvus pour stocker et interroger les vecteurs, permettant de retrouver rapidement les fichiers pertinents.

## Installation

Pour mettre en place le projet, suivez ces étapes :

1. **Installer PIP pour Windows** : Assurez-vous que PIP est installé sur votre machine pour gérer les paquets Python.
2. **Clonage du projet** :
    ```bash
    git clone <url_to_repository>
    cd <repository_name>
    ```
3. **Installation de Docker** :
    - Exécutez le script Powershell `Installe_Docker_app.ps1` pour configurer les bases de données nécessaires via Docker.
    - Utilisez cette commande pour lancer les services :
      ```bash
      wget https://github.com/milvus-io/milvus/releases/download/v2.4.0-rc.1/milvus-standalone-docker-compose.yml -O docker-compose.yml
      docker compose up -d
      ```
4. **Configuration initiale** :
    - Vérifiez que `InstallPacketAtStart` dans `Configs.conf` est mis sur `True` pour installer les dépendances nécessaires au premier lancement.

## Utilisation

- **Ajouter des documents** : Placez les fichiers texte dans le dossier `DOCs`.
- **Exécuter le script principal** :
    ```bash
    python Main.py
    ```
- **Trouver des documents** :
    - Lancez `Prompt_Doc_Finder.py` pour commencer à rechercher des documents.
    - Utilisez la commande `Help` pour obtenir des informations sur les commandes disponibles.

## Paramétrage

Le projet permet une personnalisation poussée grâce aux paramètres suivants :

- `NB_vecteur_Proche` : Nombre de vecteurs à considérer lors de la recherche.
- `Precision` : Ajuste la précision de la recherche, influençant la vitesse et l'efficacité.
- `FirstContextTrigger` : Mots clés pour l'extraction de contexte dans les textes.
- `ResumeWordSize` : Taille minimale des mots à considérer pour le contexte.
- `MaxVarcharLength` : Longueur maximale des champs de texte dans Milvus.

## Contribution

Les contributions à ce projet sont les bienvenues. Veuillez suivre les bonnes pratiques de développement et soumettre des pull requests pour toute proposition d'amélioration.

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
