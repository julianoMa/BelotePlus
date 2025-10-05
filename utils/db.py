import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data/belote.db')

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
        player1 TEXT NOT NULL,
        player2 TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rounds (
        id INTEGER PRIMARY KEY,
        tournament_id INTEGER NOT NULL,
        number INTEGER NOT NULL,
        FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams_points (
        round_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        points INTEGER,
        PRIMARY KEY (round_id, team_id),
        FOREIGN KEY (round_id) REFERENCES rounds(id),
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY,
        round_id INTEGER NOT NULL,
        tablenumber INTEGER,
        FOREIGN KEY (round_id) REFERENCES rounds(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS table_teams (
        table_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        PRIMARY KEY (table_id, team_id),
        FOREIGN KEY (table_id) REFERENCES tables(id),
        FOREIGN KEY (team_id) REFERENCES teams(id)
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

def delete_tournament(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tournaments WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_step(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT step FROM tournaments WHERE name = ?", (name,))
    step = cursor.fetchone()
    conn.close()

    return step[0]