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

from flask import Blueprint, render_template, request, redirect, url_for
from data.db import create_tournament

register_bp = Blueprint("register", __name__)

@register_bp.route("/new-tournament", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        tournament_name = request.form['tournament_name']
        rounds_number = request.form['rounds_number']
        table_number = request.form['table_number']

        create_tournament(tournament_name, rounds_number, table_number)
        return redirect(url_for("tournaments.tournaments"))

    return render_template("new-tournament.html")