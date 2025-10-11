import os
import io
import sys
import contextlib
import re
import time

from utils.db import *

def start_server(app):
    time.sleep(1.0)
    print("⏳ Starting web server...")
    time.sleep(1.2)

    buffer = io.StringIO()

    print("✅ Web server started")
    time.sleep(0.6)
    print("💻 Access the app on http://127.0.0.1:5000/")

    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        app.run(debug=True)


def db_checks():
    if not os.path.exists('data/belote.db'):
        open("data/belote.db", "x")
        time.sleep(0.8)
        print("⏳ Creating Database...")

    if len(get_tables()) == 0:
        time.sleep(0.9)
        print("⏳ Initializing Database...")
        init_db()

    return True