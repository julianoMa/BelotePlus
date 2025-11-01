from flask import Blueprint, render_template, request
from core.belote import generate_leaderboard

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route("/ranking", methods=["GET", "POST"])
def ranking():
    tournament_name = request.args.get("tournament")

    ranking = generate_leaderboard(tournament_name)

    return render_template("leaderboard.html", tournament=tournament_name, ranking=ranking)