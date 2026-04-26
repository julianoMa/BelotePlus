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

def generate_repartition(tournament_name):
    """Crée la répartition des équipes pour un tournois entier"""
    teams = data.get_teams(tournament_name)
    shuffle(teams)
    
    rounds_number = data.get_rounds(tournament_name)

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

    data.clear_repartition()
    for i in range(len(rounds)): 
        for t in range(table_needed):
            data.update_repartition(tournament_name, i+1, t+1, str(rounds[i][t]))

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