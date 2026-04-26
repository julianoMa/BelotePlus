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


import data
import common
import core

rounds_bp = Blueprint("rounds", __name__)

@rounds_bp.route("/rounds", methods=["GET", "POST"])
def rounds():
    if request.method == "POST":
        points1 = request.form.getlist("points1[]")
        points2 = request.form.getlist("points2[]")
        current_round = request.form.get("round")

        tournament_name = request.form.get("tournament")
        total_rounds = data.get_rounds(tournament_name)

        core.process_points(tournament_name, current_round, points1, points2)

        current_round = int(current_round) + 1

        data.update_step(tournament_name, current_round)

        if int(current_round) > int(total_rounds):
            return redirect(url_for("ranking.ranking", tournament=tournament_name))

        return redirect(url_for("rounds.rounds", tournament=tournament_name, round=current_round))
    

    current_round = request.args.get("round")

    tournament_name = request.args.get("tournament")
    total_rounds = data.get_rounds(tournament_name)
    check = data.check_repartition(tournament_name)
    odd = data.get_odd(tournament_name)
    odd_match = None
    r = []

    if check is None:
        core.generate_repartition(tournament_name)

    repartition = data.get_repartition(data.get_tournament_id(tournament_name), current_round)

    r = common.repartition_ast(repartition)
   
    if int(current_round) > int(total_rounds):
        return redirect(url_for("ranking.ranking", tournament=tournament_name))

    # Removes the match that will not be played from the list, and put it in another variable
    if odd:
        odd_team = str(data.get_teams_number(tournament_name))
        match = next(m for m in r if odd_team in (m['team1'], m['team2']))
        team = match['team2'] if match['team1'] == odd_team else match['team1']
        r = [m for m in r if m != match]

        data.save_points(tournament_name, current_round, odd_team, 0)
        data.save_points(tournament_name, current_round, team, 1200)
        
    return render_template("concours.html", tournament=tournament_name, round=current_round, repartition=r, odd=team)