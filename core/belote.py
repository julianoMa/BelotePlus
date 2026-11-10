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

from random import shuffle

import data
import common

def max_rounds(teams_number):
    """Nombre maximum de parties où aucune paire d'équipes ne se rencontre deux fois.

    Avec n équipes (une équipe « IMPAIR » est ajoutée si n est impair), chaque équipe
    ne peut affronter que les n-1 autres : au-delà, des rencontres se répètent.
    """
    total = teams_number + teams_number % 2
    return max(total - 1, 0)

def tables_needed(teams_number):
    """Nombre de tables nécessaires pour jouer une partie (l'équipe « IMPAIR » ne joue pas)"""
    return teams_number // 2

def build_schedule(team_ids, rounds_number):
    """Calcule les rencontres de chaque partie avec la méthode du cercle (round-robin).

    Une équipe reste fixe, les autres tournent autour : sur n-1 parties, chaque équipe
    rencontre exactement une fois toutes les autres. Renvoie une liste de parties,
    chaque partie étant une liste de tuples (equipe1, equipe2).
    """
    teams = list(team_ids)
    n = len(teams)

    if n % 2:
        raise ValueError("Le nombre d'équipes doit être pair")
    if rounds_number > max_rounds(n):
        raise ValueError(f"Impossible de jouer {rounds_number} parties avec {n} équipes sans rencontre en double (maximum : {max_rounds(n)})")

    fixed = teams[0]
    rotating = teams[1:]
    rounds = []

    for _ in range(rounds_number):
        line = [fixed] + rotating
        rounds.append([(line[i], line[n - 1 - i]) for i in range(n // 2)])
        rotating = [rotating[-1]] + rotating[:-1]

    return rounds

def generate_repartition(tournament_name):
    """Crée la répartition des équipes pour un tournois entier"""
    teams = data.get_teams(tournament_name)
    shuffle(teams)

    team_names = [f"{t[0]}" for t in teams]

    # Securité : on ne peut pas dépasser n-1 parties sans rencontre en double
    rounds_number = min(data.get_rounds(tournament_name), max_rounds(len(team_names)))

    rounds = build_schedule(team_names, rounds_number)

    data.clear_repartition()
    for i, pairs in enumerate(rounds):
        for t, pair in enumerate(pairs):
            data.update_repartition(tournament_name, i+1, t+1, str(pair))

    return True

def process_points(tournament, round, points1, points2):
    """Sauvegarde les points d'une partie"""
    repartition = data.get_repartition(data.get_tournament_id(tournament), round)
    r = common.repartition_ast(repartition)
    n = -1
    odd = data.get_odd(tournament)

    if odd:
        odd_team = str(data.get_teams_number(tournament))
        match = next(m for m in r if odd_team in (m['team1'], m['team2']))
        r = [m for m in r if m != match]

    for match in r:
        n += 1

        team1 = match["team1"]
        team2 = match["team2"]

        data.save_points(tournament, round, team1, points1[n])
        data.save_points(tournament, round, team2, points2[n])

    return

def generate_leaderboard(tournament_name):
    """Calcule le classement d'un tournois"""
    teams = len(data.get_teams(tournament_name))

    data.clear_previous_ranking(tournament_name)
    
    for i in range(teams):
        points = data.get_points(tournament_name, i+1)
        total = 0

        for point in points:
            total = total + point[0]

        data.save_ranking(tournament_name, i+1, total)
    
    leaderboard = data.get_ranking(tournament_name)

    return leaderboard