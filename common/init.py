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