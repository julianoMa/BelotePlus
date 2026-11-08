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
from sqlalchemy.exc import IntegrityError

import data

register_bp = Blueprint("register", __name__)

def _parse_positive_int(value):
    """Returns the value as an int >= 1, or None if it is not valid."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None

    return number if number >= 1 else None

@register_bp.route("/new-tournament", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Keep what the user typed so the form can be shown again with an error
        values = {
            "name": request.form.get("tournament_name", "").strip(),
            "rounds": request.form.get("rounds_number", "").strip(),
            "tables": request.form.get("table_number", "").strip(),
        }

        rounds_number = _parse_positive_int(values["rounds"])
        table_number = _parse_positive_int(values["tables"])

        error = None

        if not values["name"]:
            error = "error_tournament_name_empty"
        elif rounds_number is None or table_number is None:
            error = "error_invalid_number"
        elif values["name"].casefold() in (name.casefold() for name in data.get_tournaments_names()):
            error = "error_tournament_exists"

        if error is None:
            try:
                data.create_tournament(values["name"], rounds_number, table_number)
                return redirect(url_for("tournaments.tournaments"))
            except IntegrityError:
                # Same name created between the check above and the insert
                error = "error_tournament_exists"

        return render_template("new-tournament.html", error=error, values=values)

    return render_template("new-tournament.html", error=None, values={})
