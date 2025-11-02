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
from data.db import get_rounds, get_step, delete_tournament, get_tournaments_names

manage_tournaments_bp = Blueprint("tournaments", __name__)

@manage_tournaments_bp.route("/manage-tournaments", methods=["GET", "POST"])
def tournaments():
    if request.method == "POST":
        tournament_name = request.form.get("tournament")
        action = request.form.get("action")

        if tournament_name == None:
            return redirect(url_for("tournaments.tournaments"))

        total_rounds = get_rounds(tournament_name)

        if action == "open":
            step = get_step(tournament_name)
            if step == 0:
                return redirect(url_for("teams.teams", tournament=tournament_name))
            elif step <= total_rounds:
                return redirect(url_for("rounds.rounds", tournament=tournament_name, round=step))
            elif step > total_rounds:
                return redirect(url_for("ranking.ranking", tournament=tournament_name))

        elif action == "delete":
            delete_tournament(tournament_name) 

    try:
        tournament_names = get_tournaments_names()
        return render_template("manage-tournaments.html", tournaments=tournament_names)
    except Exception:
        return redirect(url_for("index.index"))