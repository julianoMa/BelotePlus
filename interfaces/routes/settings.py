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

import data

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings")
def settings():
    return render_template(
        "settings.html",
        tournaments_count=len(data.get_tournaments_names()),
        reset_done=request.args.get("reset") == "done",
    )

@settings_bp.route("/settings/reset", methods=["POST"])
def reset():
    # The two confirmation modals are on the client side: this field makes sure
    # the request really comes from the confirmed form and not from a stray POST.
    if request.form.get("confirm") == "reset":
        data.reset_database()
        return redirect(url_for("settings.settings", reset="done"))

    return redirect(url_for("settings.settings"))
