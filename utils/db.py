import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'belote.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    return tables

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        rounds_number INTEGER,
        tables_number INTEGER,
        step INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        tournament_id INTEGER NOT NULL,
        player1 TEXT NOT NULL,
        player2 TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranking (
        tournament_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        points INTEGER NOT NULL,
        FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams_points (
        tournament_id INTEGER NOT NULL,
        round_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        points INTEGER,
        FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
        FOREIGN KEY (round_id) REFERENCES rounds(id),
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS repartition (
        tournament_id INTEGER NOT NULL,
        round INTEGER NOT NULL,
        tablenumber INTEGER NOT NULL,
        teams INTEGER NOT NULL,
        FOREIGN KEY (round) REFERENCES rounds(id),
        FOREIGN KEY (teams) REFERENCES teams(id)
    )
    """)

    conn.commit()
    conn.close()

def get_tournaments_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM tournaments ORDER BY id")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()

    return names

def create_tournament(name, rounds_number, tables_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tournaments (name, rounds_number, tables_number, step) VALUES (?, ?, ?, ?)",
                   (name, rounds_number, tables_number, 0))
    conn.commit()
    conn.close()

def get_tournament_id(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id from tournaments WHERE name = ?", (tournament_name,))
    tournament_id = cursor.fetchone()
    conn.close()

    return tournament_id[0]

def delete_tournament(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tournaments WHERE name = ?", (tournament_name,))
    conn.commit()
    conn.close()

def get_step(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT step FROM tournaments WHERE name = ?", (tournament_name,))
    step = cursor.fetchone()
    conn.close()

    return step[0]

def get_teams(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE tournament_id = ?", (tournament_name,))
    teams = cursor.fetchall()
    conn.close()

    return teams

def add_team(tournament_name, player1, player2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teams (tournament_id, player1, player2) VALUES (?, ?, ?)",
                   (tournament_name, player1, player2))
    conn.commit()
    conn.close()

def delete_team(id, tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams WHERE id = ? AND tournament_id = ?", (id, tournament_name,))
    conn.commit()
    conn.close()

def update_step(tournament_name, step):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tournaments SET step = ? WHERE name = ?",(step, tournament_name,))
    conn.commit()
    conn.close()

def get_rounds(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rounds_number FROM tournaments WHERE name = ?",(tournament_name,))
    rounds_number = cursor.fetchall()
    conn.close()

    return rounds_number[0][0]

def update_repartition(tournament_name, round, table_number, teams):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO repartition (tournament_id, round, tablenumber, teams) VALUES (?, ?, ?, ?)",
                   (tournament_name, round, table_number, teams,))
    conn.commit()
    conn.close()

def check_repartition(tournament_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT round FROM repartition WHERE tournament_id = ?",(tournament_name,))
    result = cursor.fetchone()
    conn.close()

    return result

def clear_repartition():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM repartition")
    conn.commit()
    conn.close()

def get_repartition(round):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM repartition WHERE round = ?",(round,))
    repartition = cursor.fetchall()
    conn.close()

    return repartition

def save_points(tournament, round, team, point):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teams_points (tournament_id, round_id, team_id, points) VALUES (?, ?, ?, ?)",
                   (tournament, round, team, point,))
    conn.commit()
    conn.close()

def clear_points():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams_points")
    conn.commit()
    conn.close()

def get_points(tournament, team):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM teams_points WHERE tournament_id = ? AND team_id = ?",(tournament, team,))
    result = cursor.fetchall()
    conn.close()

    return result

def save_ranking(tournament, team, points):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ranking (tournament_id, team_id, points) VALUES (?, ?, ?)",
                   (tournament, team, points))
    conn.commit()
    conn.close()

def get_ranking(tournament):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT team_id FROM ranking WHERE tournament_id = ? ORDER BY points DESC""", (tournament,))
    result = cursor.fetchall()
    conn.close()

    ranking = [row[0] for row in result]
    return ranking

def clear_previous_ranking(tournament):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM ranking WHERE tournament_id = ?""",(tournament,))
    conn.commit()
    conn.close()