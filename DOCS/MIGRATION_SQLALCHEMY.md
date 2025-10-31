# Architecture de la Base de Données

## Vue d'ensemble

BelotePlus utilise SQLAlchemy ORM pour gérer sa base de données. Ce système permet de manipuler les données de manière sécurisée et intuitive en travaillant avec des objets Python plutôt qu'avec du SQL brut.

## Structure du projet

### Fichiers principaux

1. **`utils/models.py`** : Définit tous les modèles de données
   - `Tournament` : Représente un tournoi
   - `Team` : Représente une équipe de joueurs
   - `Ranking` : Stocke le classement des équipes
   - `TeamPoints` : Enregistre les points par round
   - `Repartition` : Gère la répartition des équipes sur les tables

2. **`utils/db.py`** : Contient toutes les fonctions d'accès à la base de données
   - Gère les sessions SQLAlchemy
   - Fournit un context manager pour les transactions
   - Expose des fonctions de haut niveau pour manipuler les données

3. **`migrate_db.py`** : Script utilitaire pour migrer une ancienne base de données

## Pourquoi SQLAlchemy ?

1. **Sécurité** : Protection automatique contre les injections SQL
2. **Maintenabilité** : Code plus lisible et plus facile à faire évoluer
3. **Relations** : Gestion automatique des liens entre tables
4. **Cascades** : Suppression en cascade des données liées (supprimer un tournoi supprime automatiquement ses équipes)
5. **Type Safety** : Vérification des types au niveau du code
6. **Portabilité** : Possibilité de changer de SGBD (PostgreSQL, MySQL, etc.) sans modifier le code

## Installation

Pour installer les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## Modèles de données

### Tournament (Tournoi)

Représente un tournoi de belote.

- `id` : Identifiant unique du tournoi
- `name` : Nom du tournoi (doit être unique)
- `rounds_number` : Nombre total de rounds dans le tournoi
- `tables_number` : Nombre de tables disponibles
- `step` : Étape actuelle du tournoi (0 = configuration, 1+ = numéro du round en cours)

### Team (Équipe)

Représente une équipe de deux joueurs.

- `id` : Identifiant unique de l'équipe
- `tournament_id` : Référence vers le tournoi auquel appartient l'équipe
- `player1` : Nom du premier joueur
- `player2` : Nom du second joueur

### Ranking (Classement)

Stocke le classement général d'une équipe dans un tournoi.

- `id` : Identifiant unique de l'entrée
- `tournament_id` : Référence vers le tournoi
- `team_id` : Référence vers l'équipe
- `points` : Total des points accumulés

### TeamPoints (Points des équipes)

Enregistre les points obtenus par une équipe lors d'un round spécifique.

- `id` : Identifiant unique de l'entrée
- `tournament_id` : Référence vers le tournoi
- `round_id` : Numéro du round
- `team_id` : Référence vers l'équipe
- `points` : Points obtenus lors de ce round

### Repartition

Gère la répartition des équipes sur les tables pour chaque round.

- `id` : Identifiant unique de l'entrée
- `tournament_id` : Référence vers le tournoi
- `round` : Numéro du round
- `tablenumber` : Numéro de la table
- `teams` : Liste des équipes (stockée au format string)

## Utilisation de la base de données

### Fonctions de haut niveau

Le fichier `utils/db.py` expose des fonctions simples pour manipuler les données sans avoir à écrire de requêtes SQL :

```python
from utils import db

# créer un tournoi
db.create_tournament("Mon Tournoi", rounds=5, tables=3)

# ajouter une équipe
db.add_team("Mon Tournoi", "Alice", "Bob")

# récup les classements
rankings = db.get_ranking("Mon Tournoi")
```

Ces fonctions gèrent automatiquement les transactions et la fermeture des sessions.

### Accès direct aux modèles (usage avancé)

Pour des opérations plus complexes, vous pouvez utiliser directement les modèles SQLAlchemy :

```python
from utils.db import get_session, Tournament, Team

# ex: récup un tournoi avec toutes ses équipes
with get_session() as session:
    tournament = session.query(Tournament).filter_by(name="Mon Tournoi").first()
    teams = tournament.teams  # relation auto
    print(f"Le tournoi {tournament.name} a {len(teams)} équipes")
```

Le context manager `get_session()` garantit que la session est correctement fermée, même en cas d'erreur.

### Requêtes complexes

SQLAlchemy permet de construire des requêtes avancées de manière intuitive :

```python
from utils.db import get_session, Team, Ranking

with get_session() as session:
    # récup les 3 meilleures équipes tous tournois confondus
    top_teams = session.query(Team, Ranking.points)\
        .join(Ranking)\
        .order_by(Ranking.points.desc())\
        .limit(3)\
        .all()
```

## Migration d'une ancienne base de données

Si vous disposez d'une base de données créée avant l'utilisation de SQLAlchemy, utilisez le script de migration :

```bash
python migrate_db.py
```

Ce script effectue les opérations suivantes :

- Crée une sauvegarde de votre base actuelle
- Migre toutes les données vers la nouvelle structure
- Conserve l'intégralité de vos tournois, équipes et classements
