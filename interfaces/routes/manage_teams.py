from flask import Blueprint, render_template, request, redirect, url_for, flash
from data.db import get_teams, add_team, delete_team, update_step

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/manage-teams", methods=["GET", "POST"])
def teams():
    tournament = request.args.get("tournament")
    
    if request.method == "POST":
        action = request.form.get("action")
        tournament = request.form['tournament']
        teams_list = get_teams(tournament)

        if (action in ["start", "delete"] and not teams_list):
            flash("Vous devez créer une équipe avant d utiliser ce bouton", "error")
            return redirect(url_for("index.index"))

        if action == "create":
            player1 = request.form['player1']
            player2 = request.form['player2']
            tournament = request.form['tournament']

            add_team(tournament, player1, player2)

            return redirect(url_for("teams.teams", tournament=tournament))
        
        if action == "delete":
            id = request.form['team']
            tournament_name = request.form['tournament']
            
            delete_team(id, tournament_name)

            return redirect(url_for("teams.teams", tournament=tournament_name))
        
        if action == "start":
            tournament_name = request.form['tournament']

            update_step(tournament_name, 1)

            return redirect(url_for("rounds.rounds", tournament=tournament_name, round=1))

    teams_list = get_teams(tournament)
    teams = []

    for id, tournament, player1, player2 in teams_list:
        teams.append({"id": id, "player1": player1, "player2": player2})

    return render_template("manage-teams.html", tournament=tournament, teams=teams)