from utils.db import *
from random import shuffle
import ast

def generate_repartition(round, tournament_name):
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
    repartition = get_repartition(round)
    n = -1

    for _, _, _, teams in repartition:
        n += 1
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
            save_points(tournament, round, teams[0], points1[n])
            save_points(tournament, round, teams[1], points2[n])

    return

def generate_leaderboard(tournament_name):
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