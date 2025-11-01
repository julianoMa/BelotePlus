from flask import Blueprint, render_template, request, redirect, url_for
from data.db import create_tournament

register_bp = Blueprint("register", __name__)

@register_bp.route("/new-tournament", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        tournament_name = request.form['tournament_name']
        rounds_number = request.form['rounds_number']
        table_number = request.form['table_number']

        create_tournament(tournament_name, rounds_number, table_number)
        return redirect(url_for("tournaments.tournaments"))

    return render_template("new-tournament.html")