import sys
sys.dont_write_bytecode = True

from flask import Flask, render_template, request, redirect, url_for
from utils.init import *
from utils.db import * 

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

        elif action == "delete":
            delete_tournament(tournament_name) 

    tournament_names = get_tournaments_names()
    return render_template("manage-tournaments.html", tournaments=tournament_names)

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
    print(get_teams(tournament))
    


    
    return render_template("manage-teams.html")

@app.route("/rounds", methods=["GET", "POST"])
def rounds():
    return True

@app.route("/edit-scores", methods=["GET", "POST"])
def editscores():
    return True

@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    return True

if __name__ == "__main__":
    print("🛠️  Starting checks...")
    if db_checks() == True:
        print("✅ Database ")

    print("⏳ Starting Web Server")
    app.run(debug=True)