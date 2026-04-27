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

import data

def start_server(app):
    """Démarre le serveur"""
    print("⏳ Starting web server...")

    print("✅ Web server started")
    print("💻 App is launched on http://127.0.0.1:8080/")

    import webbrowser
    webbrowser.open("http://127.0.0.1:8080")

    from waitress import serve
    serve(app, host="0.0.0.0", port=8080, threads=4)


def db_checks():
    """Crée la base de donnée si elle n'existe pas et l'initialise avec les tables"""
    if not os.path.exists(data.DB_PATH):
        os.makedirs(os.path.dirname(data.DB_PATH), exist_ok=True)
        open(data.DB_PATH, "x")
        print("⏳ Creating Database...")

    if len(data.get_tables()) == 0:
        print("⏳ Initializing Database...")
        data.init_db()

    return True