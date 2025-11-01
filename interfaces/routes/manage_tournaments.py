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