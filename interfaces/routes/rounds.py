from flask import Blueprint, render_template, request, redirect, url_for
from data.db import get_rounds, update_step, check_repartition, get_repartition, get_tournament_id
from common.utils import repartition_ast
from core.belote import generate_repartition, process_points

rounds_bp = Blueprint("rounds", __name__)

@rounds_bp.route("/rounds", methods=["GET", "POST"])
def rounds():
    if request.method == "POST":
        points1 = request.form.getlist("points1[]")
        points2 = request.form.getlist("points2[]")
        current_round = request.form.get("round")

        tournament_name = request.form.get("tournament")
        total_rounds = get_rounds(tournament_name)

        process_points(tournament_name, current_round, points1, points2)

        current_round = int(current_round) + 1

        update_step(tournament_name, current_round)

        if int(current_round) > int(total_rounds):
            return redirect(url_for("ranking.ranking", tournament=tournament_name))

        return redirect(url_for("rounds.rounds", tournament=tournament_name, round=current_round))
    

    current_round = request.args.get("round")

    tournament_name = request.args.get("tournament")
    total_rounds = get_rounds(tournament_name)
    check = check_repartition(tournament_name)
    r = []

    if check is None:
        generate_repartition(current_round, tournament_name)

    repartition = get_repartition(get_tournament_id(tournament_name), current_round)

    r = repartition_ast(repartition)
   
    if int(current_round) > int(total_rounds):
        return redirect(url_for("ranking.ranking", tournament=tournament_name))
        
    return render_template("concours.html", tournament=tournament_name, round=current_round, repartition=r)