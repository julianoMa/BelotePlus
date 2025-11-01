import ast

def repartition_ast(repartition):
    """Convertis des strings en objets Python"""
    r = []
    for tournament, cround, table, teams in repartition:
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
        r.append({"tournament": tournament, "round": cround, "table": table, "team1": teams[0], "team2": teams[1]})

    return r 