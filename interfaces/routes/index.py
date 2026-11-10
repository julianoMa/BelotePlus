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

import time

from flask import Blueprint, render_template, make_response

import services
from config.settings import VERSION

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    latest, refreshed = services.get_latest_version()

    response = make_response(render_template(
        "index.html",
        current=VERSION,
        latest=latest or VERSION,
        compare=services.compare_versions(latest),
    ))

    if refreshed:
        response.set_cookie("last_update", str(time.time()), max_age=31536000, path="/")
        if latest:
            response.set_cookie("last_version", latest, max_age=31536000, path="/")

    return response
