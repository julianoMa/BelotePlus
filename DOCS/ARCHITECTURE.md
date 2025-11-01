# Architecture du projet

## Vue d'ensemble

BelotePlus utilise les principes de clean architecture afin d'avoir un code maintenable et facile à comprendre pour les nouveaux contributeurs.

## Structure du projet

### Dossiers principaux

1. **`common/`** : Contient le code d'utilité générale et les checks
    - `init.py` : Test basique et initialisations
    - `utils.py` : Fonctions utilitaires

2. **`core/`** : Contient le coeur du code de BelotePlus, des packages indépendants.
    - `belote.py` : Fonctions pour le jeu de belote en lui-même
    - `translations.py` : Support multi-langues

3. **`data/`** : Contient le code en relation avec la base de donnée
    - `db.py` : Session SQLAlchemy, fonctions pour intéragir avec la BDD
    -  `models.py` : Modèles ORM

4. **`services/`** : Contient le code faisant le lien entre plusieurs couches du projet
    - `player_screen.py` : Récupération des données pour l'écran des joueurs

5. **`interfaces/`** : Contient tout le code agissant avec l'extérieur du project (API) et les routes
    - `routes/` : Enregistrement de toutes les routes de Flask