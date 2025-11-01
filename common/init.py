import os
import time

from data import *

def start_server(app):
    """Démarre le serveur"""
    print("⏳ Starting web server...")

    print("✅ Web server started")
    print("💻 App is launched on http://127.0.0.1:5000/")

    app.run()


def db_checks():
    """Crée la base de donnée si elle n'existe pas et l'initialise avec les tables"""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        open(DB_PATH, "x")
        time.sleep(0.8)
        print("⏳ Creating Database...")

    if len(get_tables()) == 0:
        time.sleep(0.9)
        print("⏳ Initializing Database...")
        init_db()

    return True