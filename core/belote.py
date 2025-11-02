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

from data import *
from random import shuffle
import ast

def generate_repartition(tournament_name):
    """Crée la répartition des équipes pour un tournois entier"""
    teams = get_teams(tournament_name)
    shuffle(teams)
    
    rounds_number = get_rounds(tournament_name)

    team_names = [f"{t[0]}" for t in teams]
    n = len(team_names)

    table_needed = n // 2
    rounds = []

    for r in range(rounds_number):
        pairs = []
        for i in range(table_needed):
            t1 = team_names[i]
            t2 = team_names[-i - 1]
            pairs.append((t1, t2))
        rounds.append(pairs)

        team_names = [team_names[-1]] + team_names[:-1]

    clear_repartition()
    for i in range(len(rounds)): 
        for t in range(table_needed):
            update_repartition(tournament_name, i+1, t+1, str(rounds[i][t]))

    return True

def process_points(tournament, round, points1, points2):
    """Sauvegarde les points d'une partie"""
    repartition = get_repartition(get_tournament_id(tournament), round)
    n = -1

    for _, _, _, teams in repartition:
        n += 1
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
            save_points(tournament, round, teams[0], points1[n])
            save_points(tournament, round, teams[1], points2[n])

    return

def generate_leaderboard(tournament_name):
    """Calcule le classement d'un tournois"""
    teams = len(get_teams(tournament_name))

    clear_previous_ranking(tournament_name)
    
    for i in range(teams):
        points = get_points(tournament_name, i+1)
        total = 0

        for point in points:
            total = total + point[0]

        save_ranking(tournament_name, i+1, total)
    
    leaderboard = get_ranking(tournament_name)

    return leaderboard