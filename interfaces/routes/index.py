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

from flask import Blueprint, render_template, request, make_response

import services
from config.settings import VERSION

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    check_update = services.check_update_timestamp()
    tag = VERSION

    if check_update is None: # Not yet created
        tag = services.get_newest_tag()
    if check_update is False: # Created more than 6hr ago
        tag = services.get_newest_tag()

    response = make_response(render_template("index.html", current=VERSION, latest=tag, compare=services.compare_versions()))

    if check_update is None: # Not yet created
        response.set_cookie("last_update", str(time.time()), max_age=31536000, path="/")
        response.set_cookie("last_version", tag, max_age=31536000, path="/")
    elif check_update is False: # Created more than 6hr ago
        response.set_cookie("last_update", str(time.time()), max_age=31536000, path="/")
        response.set_cookie("last_version", tag, max_age=31536000, path="/")

    return response