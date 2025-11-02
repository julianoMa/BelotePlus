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
from data.db import get_tournaments_names, get_rounds
from services.player_service import get_players_screen_data

players_bp = Blueprint("players", __name__)

@players_bp.route("/players-screen", methods=["GET", "POST"])
def players():
    tournaments = get_tournaments_names()
    tournament = "none"
    rounds = 0
    round_selected = 0 
    data = {"teams_points": [], "repartition": []}

    if request.method == "POST":
        action = request.form.get("action")

        if action == "tournaments":
            tournament = request.form.get('tournaments', '')

            if tournament == "":
                return redirect(url_for("players.players"))
            else:
                rounds = get_rounds(tournament)

        elif action == "rounds":
            tournament = request.form.get('tournament', '')
            round_selected = request.form.get('rounds-select', 0)
            rounds = request.form.get('rounds-a', 0)

            data = get_players_screen_data(tournament, round_selected)
                
    return render_template("players-screen.html", tournaments=tournaments, tournament=tournament, rounds=int(rounds), round=int(round_selected), teams_points=data["teams_points"], repartition=data["repartition"])