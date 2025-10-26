from utils.db import get_teams, get_rounds, update_repartition, clear_repartition
from random import shuffle


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

    return rounds
