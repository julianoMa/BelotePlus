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