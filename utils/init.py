import os
import time

from utils.db import *

def start_server(app):
    print("⏳ Starting web server...")

    print("✅ Web server started")
    print("💻 App is launched on http://127.0.0.1:5000/")

    app.run()


def db_checks():
    if not os.path.exists('belote.db'):
        open("belote.db", "x")
        time.sleep(0.8)
        print("⏳ Creating Database...")

    if len(get_tables()) == 0:
        time.sleep(0.9)
        print("⏳ Initializing Database...")
        init_db()

    return True