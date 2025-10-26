import sys
sys.dont_write_bytecode = True # To prevent creation of "__pycache__" folder

from flask import Flask, render_template, request, redirect, url_for
from utils.init import *
from utils.db import * 
from utils.belote import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage-tournaments", methods=["GET", "POST"])
def tournaments():
    if request.method == "POST":
        tournament_name = request.form.get("tournament")
        action = request.form.get("action")

        if action == "open":
            step = get_step(tournament_name)
            if step == 0:
                return redirect(url_for("teams", tournament=tournament_name))
            elif step == 1 or step == 2 or step == 3 or step == 4:
                return redirect(url_for("rounds", tournament=tournament_name, round=step))

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
        return redirect("/")

    return render_template("new-tournament.html")

@app.route("/manage-teams", methods=["GET", "POST"])
def teams():
    tournament = request.args.get("tournament")
    
    if request.method == "POST":
        action = request.form.get("action")

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

            return redirect(url_for("rounds", tournament=tournament_name))

    teams_list = get_teams(tournament)
    teams = []

    for id, tournament, player1, player2 in teams_list:
        teams.append({"id": id, "player1": player1, "player2": player2})

    return render_template("manage-teams.html", tournament=tournament, teams=teams)

@app.route("/rounds", methods=["GET", "POST"])
def rounds():
    current_round = request.args.get("round")
    tournament_name = request.args.get("tournament")

    if current_round == "1":
        repartition = generate_repartition(current_round, tournament_name)
    
    return render_template("concours.html")

@app.route("/edit-scores", methods=["GET", "POST"])
def editscores():
    return True

@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    return True

@app.route("/archives", methods=["GET", "POST"])
def archives():
    return True

if __name__ == "__main__":
    print("🛠️  Starting checks...")
    if db_checks() == True:
        print("✅ Database ")
        
    start_server(app)