from common import *
from data import *

def get_players_screen_data(tournament, round_selected):
    """
    Returns all data needed to render the players screen.
    tournament: string name
    round_selected: int, current round
    """

    teams_points = []

    if tournament and round_selected:
        teams = get_teams(tournament)
        for team in teams:
            team_id = team[0]
            points = get_points(tournament, team_id)
            selected_points = points[:int(round_selected)]
            total = sum(p[0] for p in selected_points)
            teams_points.append({
                "team_id": team_id,
                "points": selected_points,
                "total": total
            })

        repartition = get_repartition(get_tournament_id(tournament), round_selected)
        
        r = repartition_ast(repartition)

    return {
        "teams_points": teams_points,
        "repartition": r
    }