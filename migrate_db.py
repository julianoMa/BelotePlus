# BelotePlus - Gestionnaire de concours de belote
# Copyright (C) 2025  Juliano Martins - Un Ange pour Juliano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Script de migration de l'ancienne base de données SQLite vers SQLAlchemy
À exécuter une seule fois si vous avez une base de données existante
"""

import sqlite3
import os
import shutil
from datetime import datetime

from utils.db import (
    init_db, get_session, 
    Tournament, Team, Ranking, TeamPoints, Repartition
)

DB_PATH = os.path.join(os.path.dirname(__file__), 'belote.db')
BACKUP_PATH = os.path.join(os.path.dirname(__file__), f'belote_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')


def check_old_db_exists():
    """Vérifie si une ancienne base de données existe"""
    if not os.path.exists(DB_PATH):
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Vérifie si ce sont les anciennes tables (sans colonnes id pour ranking, etc.)
        return 'tournaments' in tables and 'teams' in tables
    except Exception:
        return False


def migrate_database():
    """Migre les données de l'ancienne base vers la nouvelle"""
    if not check_old_db_exists():
        print("❌ Aucune ancienne base de données à migrer")
        return False
    
    print("🔄 Migration de la base de données en cours...")
    
    # Faire une sauvegarde
    print(f"💾 Création d'une sauvegarde : {BACKUP_PATH}")
    shutil.copy2(DB_PATH, BACKUP_PATH)
    
    try:
        # Connexion à l'ancienne base
        old_conn = sqlite3.connect(DB_PATH)
        old_cursor = old_conn.cursor()
        
        # Récupération des données
        old_cursor.execute("SELECT * FROM tournaments")
        tournaments_data = old_cursor.fetchall()
        
        old_cursor.execute("SELECT * FROM teams")
        teams_data = old_cursor.fetchall()
        
        old_cursor.execute("SELECT * FROM ranking")
        ranking_data = old_cursor.fetchall()
        
        old_cursor.execute("SELECT * FROM teams_points")
        teams_points_data = old_cursor.fetchall()
        
        old_cursor.execute("SELECT * FROM repartition")
        repartition_data = old_cursor.fetchall()
        
        old_conn.close()
        
        # Suppression de l'ancienne base
        os.remove(DB_PATH)
        
        # Création de la nouvelle structure
        print("🔧 Création de la nouvelle structure...")
        init_db()
        
        # Migration des données
        with get_session() as session:
            # Mapping des anciens IDs de tournois vers les noms
            tournament_mapping = {}
            
            print("📋 Migration des tournois...")
            for row in tournaments_data:
                old_id, name, rounds_number, tables_number, step = row
                tournament = Tournament(
                    name=name,
                    rounds_number=rounds_number,
                    tables_number=tables_number,
                    step=step if step is not None else 0
                )
                session.add(tournament)
                session.flush()  # Pour obtenir l'ID
                tournament_mapping[old_id] = (tournament.id, name)
            
            print("👥 Migration des équipes...")
            team_mapping = {}
            for row in teams_data:
                old_id, tournament_id, player1, player2 = row
                if tournament_id in tournament_mapping:
                    new_tournament_id, _ = tournament_mapping[tournament_id]
                    team = Team(
                        tournament_id=new_tournament_id,
                        player1=player1,
                        player2=player2
                    )
                    session.add(team)
                    session.flush()
                    team_mapping[old_id] = team.id
            
            print("🏆 Migration des classements...")
            for row in ranking_data:
                if len(row) >= 3:  # Vérifie qu'on a au moins 3 colonnes
                    tournament_id, team_id, points = row[:3]
                    if tournament_id in tournament_mapping and team_id in team_mapping:
                        new_tournament_id, _ = tournament_mapping[tournament_id]
                        new_team_id = team_mapping[team_id]
                        ranking = Ranking(
                            tournament_id=new_tournament_id,
                            team_id=new_team_id,
                            points=points if points is not None else 0
                        )
                        session.add(ranking)
            
            print("📊 Migration des points...")
            for row in teams_points_data:
                if len(row) >= 4:
                    tournament_id, round_id, team_id, points = row[:4]
                    if tournament_id in tournament_mapping and team_id in team_mapping:
                        new_tournament_id, _ = tournament_mapping[tournament_id]
                        new_team_id = team_mapping[team_id]
                        team_points = TeamPoints(
                            tournament_id=new_tournament_id,
                            round_id=round_id,
                            team_id=new_team_id,
                            points=points if points is not None else 0
                        )
                        session.add(team_points)
            
            print("🎲 Migration des répartitions...")
            for row in repartition_data:
                if len(row) >= 4:
                    tournament_id, round_num, tablenumber, teams = row[:4]
                    if tournament_id in tournament_mapping:
                        new_tournament_id, _ = tournament_mapping[tournament_id]
                        repartition = Repartition(
                            tournament_id=new_tournament_id,
                            round=round_num,
                            tablenumber=tablenumber,
                            teams=str(teams)
                        )
                        session.add(repartition)
        
        print("✅ Migration terminée avec succès !")
        print(f"💾 Sauvegarde conservée dans : {BACKUP_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        print(f"🔄 Restauration de la sauvegarde...")
        if os.path.exists(BACKUP_PATH):
            shutil.copy2(BACKUP_PATH, DB_PATH)
            print("✅ Base de données restaurée")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("MIGRATION DE LA BASE DE DONNÉES BELOTEPLUS")
    print("=" * 50)
    print()
    
    if check_old_db_exists():
        response = input("Une ancienne base de données a été détectée. Voulez-vous la migrer ? (oui/non) : ")
        if response.lower() in ['oui', 'o', 'yes', 'y']:
            migrate_database()
        else:
            print("Migration annulée.")
    else:
        print("Aucune ancienne base de données détectée.")
        print("Initialisation d'une nouvelle base de données...")
        init_db()
        print("✅ Nouvelle base de données créée !")
