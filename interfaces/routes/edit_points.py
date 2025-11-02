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

from flask import Blueprint, render_template, request, redirect, url_for
from data.db import get_tournaments_names, get_rounds, get_teams, save_points

edit_bp = Blueprint("edit", __name__)

@edit_bp.route("/edit-points", methods=["GET", "POST"])
def edit():
    tournaments = get_tournaments_names()
    tournament = "none"
    rounds = 0
    round_selected = 0
    teams = []
    team_selected = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "tournaments":
            tournament = request.form.get("tournaments")
            rounds = get_rounds(tournament)
        
        elif action == "rounds":
            tournament = request.form.get("tournament")
            rounds = request.form.get("rounds-a")
            round_selected = request.form.get("rounds-select")

            teams = get_teams(tournament)
            teams = [(team[0], team[2], team[3]) for team in teams]

        elif action == "team":
            tournament = request.form.get("tournament")
            rounds = request.form.get("rounds-a")
            round_selected = request.form.get("round_selected")
            team_selected = request.form.get("team-select")

        elif action == "points":
            tournament = request.form.get("tournament")
            round_selected = request.form.get("round_selected")
            team_selected = request.form.get("team_selected")
            points = request.form.get("point-input")

            team_id = team_selected[1]

            save_points(tournament, int(round_selected), int(team_id), int(points))
            
            return redirect(url_for("edit.edit"))

    return render_template("edit-points.html", tournaments=tournaments, tournament=tournament, rounds=int(rounds), round_selected=int(round_selected), teams=teams, team_selected=team_selected)