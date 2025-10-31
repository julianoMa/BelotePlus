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
sys.dont_write_bytecode = True

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import ast

from utils.init import *
from utils.db import * 
from utils.belote import *
from utils.translations import load_translations, get_all_translations

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_translations()

@app.context_processor
def inject_language():
    """inject lang in all templates"""
    lang = request.cookies.get('language', 'fr')
    return {
        'current_lang': lang,
        't': get_all_translations(lang)
    }

@app.route("/set-language/<lang>")
def set_language(lang):
    """change user lang"""
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    resp = make_response(redirect(request.referrer or url_for('index')))
    resp.set_cookie('language', lang, max_age=31536000)
    return resp

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
    except Exception:
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

    repartition = get_repartition(tournament_name, current_round)

    for _, cround, table, teams in repartition:
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
        r.append({"table": table, "team1": teams[0], "team2": teams[1], "round": cround})
   
    if int(current_round) > int(total_rounds):
        return redirect(url_for("ranking", tournament=tournament_name))
        
    return render_template("concours.html", tournament=tournament_name, round=current_round, repartition=r)

@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    tournament_name = request.args.get("tournament")

    ranking = generate_leaderboard(tournament_name)

    return render_template("leaderboard.html", tournament=tournament_name, ranking=ranking)

@app.route("/players-screen", methods=["GET", "POST"])
def players():
    tournaments = get_tournaments_names()
    tournament = "none"
    rounds = 0
    round_selected = 0 
    teams_points = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "tournaments":
            tournament = request.form.get('tournaments', '')

            if tournament == "":
                return redirect(url_for("players"))
            else:
                rounds = get_rounds(tournament)

        elif action == "rounds":
            tournament = request.form.get('tournament', '')
            round_selected = request.form.get('rounds-select', 0)
            rounds = request.form.get('rounds-a', 0)

            if not round_selected:
                return redirect(url_for("players"))
            
            # Getting teams points

            teams_points = []
            teams = get_teams(tournament)
            
            for team in teams:
                team_id = team[0]
                points = get_points(tournament, team_id)
                selected_points = points[:int(round_selected)]

                total = 0
                for point in selected_points:
                    total = total + point[0]

                
                teams_points.append({
                    "team_id": team_id,
                    "points": selected_points,
                    "total": total
                })

            # Getting repartition 

            r = []
            repartition = get_repartition(tournament, round_selected)

            for _, _, table, teams in repartition:
                if isinstance(teams, str):
                    teams = ast.literal_eval(teams)
                r.append({"table": table, "team1": teams[0], "team2": teams[1]})
                
    return render_template("players-screen.html", tournaments=tournaments, tournament=tournament, rounds=int(rounds), round=int(round_selected), teams_points=teams_points, repartition=r)

@app.route("/edit-scores", methods=["GET", "POST"])
def editscores():
    return True

#@app.route("/archives", methods=["GET", "POST"])
#def archives():
#    return True

if __name__ == "__main__":
    print("🛠️  Starting checks...")
    if db_checks() == True:
        print("✅ Database ")
        
    start_server(app)