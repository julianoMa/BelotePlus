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