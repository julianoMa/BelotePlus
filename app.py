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


import sys
sys.dont_write_bytecode = True # To prevent creation of "__pycache__" folder

from flask import Flask, render_template, request, redirect, url_for, flash
import ast

from utils.init import *
from utils.db import * 
from utils.belote import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage-tournaments", methods=["GET", "POST"])
def tournaments():
    if request.method == "POST":
        tournament_name = request.form.get("tournament")
        action = request.form.get("action")

        if tournament_name == None:
            return redirect(url_for("tournaments"))

        total_rounds = get_rounds(tournament_name)

        if action == "open":
            step = get_step(tournament_name)
            if step == 0:
                return redirect(url_for("teams", tournament=tournament_name))
            elif step <= total_rounds:
                return redirect(url_for("rounds", tournament=tournament_name, round=step))
            elif step > total_rounds:
                return redirect(url_for("ranking", tournament=tournament_name))

        elif action == "delete":
            delete_tournament(tournament_name) 

    try:
        tournament_names = get_tournaments_names()
        return render_template("manage-tournaments.html", tournaments=tournament_names)
    except sqlite3.OperationalError:
        return redirect(url_for("index"))

@app.route("/new-tournament", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        tournament_name = request.form['tournament_name']
        rounds_number = request.form['rounds_number']
        table_number = request.form['table_number']

        create_tournament(tournament_name, rounds_number, table_number)
        return redirect(url_for("tournaments"))

    return render_template("new-tournament.html")

@app.route("/manage-teams", methods=["GET", "POST"])
def teams():
    tournament = request.args.get("tournament")
    
    if request.method == "POST":
        action = request.form.get("action")
        tournament = request.form['tournament']
        teams_list = get_teams(tournament)

        if (action in ["start", "delete"] and not teams_list):
            flash("Vous devez créer une équipe avant d utiliser ce bouton", "error")
            return redirect(url_for("index"))

        if action == "create":
            player1 = request.form['player1']
            player2 = request.form['player2']
            tournament = request.form['tournament']

            add_team(tournament, player1, player2)

            return redirect(url_for("teams", tournament=tournament))
        
        if action == "delete":
            id = request.form['team']
            tournament_name = request.form['tournament']
            
            delete_team(id, tournament_name)

            return redirect(url_for("teams", tournament=tournament_name))
        
        if action == "start":
            tournament_name = request.form['tournament']

            update_step(tournament_name, 1)

            return redirect(url_for("rounds", tournament=tournament_name, round=1))

    teams_list = get_teams(tournament)
    teams = []

    for id, tournament, player1, player2 in teams_list:
        teams.append({"id": id, "player1": player1, "player2": player2})

    return render_template("manage-teams.html", tournament=tournament, teams=teams)

@app.route("/rounds", methods=["GET", "POST"])
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
            return redirect(url_for("ranking", tournament=tournament_name))

        return redirect(url_for("rounds", tournament=tournament_name, round=current_round))
    

    current_round = request.args.get("round")

    tournament_name = request.args.get("tournament")
    total_rounds = get_rounds(tournament_name)
    check = check_repartition(tournament_name)
    r = []

    if check is None:
        generate_repartition(current_round, tournament_name)

    repartition = get_repartition(current_round)

    for _, cround, table, teams in repartition:
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
        r.append({"table": table, "team1": teams[0], "team2": teams[1], "round": cround})
   
    if int(current_round) > int(total_rounds):
        return redirect(url_for("ranking", tournament=tournament_name))
        
    return render_template("concours.html", tournament=tournament_name, round=current_round, repartition=r)

@app.route("/edit-scores", methods=["GET", "POST"])
def editscores():
    return True

@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    tournament_name = request.args.get("tournament")

    ranking = generate_leaderboard(tournament_name)

    return render_template("leaderboard.html", tournament=tournament_name, ranking=ranking)

@app.route("/archives", methods=["GET", "POST"])
def archives():
    return True

if __name__ == "__main__":
    print("🛠️  Starting checks...")
    if db_checks() == True:
        print("✅ Database ")
        
    start_server(app)