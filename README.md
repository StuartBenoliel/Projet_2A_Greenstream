# Greenstream - Projet 2A

L’industrie de la vidéo à la demande (VOD) a connu une croissance exponentielle au cours de la
dernière décennie, offrant aux consommateurs un accès instantané à des milliers de contenus multi-
médias. Cependant, cette commodité n’est pas sans conséquences sur l’environnement. La consom-
mation croissante de données pour le streaming vidéo contribue significativement à l’empreinte
carbone mondiale.

Dans ce contexte, le projet "GreenStream" émerge comme une solution innovante et écologique pour
aborder ce défi. GreenStream est une API REST conçue pour aider à réduire l’impact carbone des
services de VOD, tels que Netflix, Amazon Prime, Disney+, et bien d’autres. Cette API propose des
fonctionnalités essentielles pour les consommateurs et les fournisseurs de VOD, en s’appuyant sur
des données en temps réel fournies par l’API ElectricityMaps.

## Installation

1. Cloner le projet.

2. Utilisez `pip` pour installer les dépendances à partir du fichier `requirements.txt` :
```bash
pip install -r requirements.txt
```

## Mise en garde

Ce projet informatique utilise un fichier regions_fournisseurs-cloud.csv contenue dans le module data.
Ce fichier a été préalablement traité et doit être impérativement utilisé par notre application.

## Usage

Remplissez les valeurs manquantes du module .env :
- token_em par votre clé API de Electricity Map.
- token_admin par le choix de votre clé API Administateur.
- PASSWORD par le mot de passe de votre système de base de données.
Modifier les autres variables au besoin. 

Pour une première utilisation ou pour ré-initialiser les base de données,
lancer le fichier main.py contenue dans src.
Enfin, lancer le fichier app.py pour lancer l'API.
