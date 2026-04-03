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

import requests

from config.settings import VERSION

def get_newest_tag():
    url = f"https://api.github.com/repos/julianoMa/BelotePlus/releases/latest"

    try:
        tag = requests.get(url).json()["tag_name"]
    except KeyError:
        return VERSION
    except requests.exceptions.ConnectionError:
        return VERSION

    return tag

def compare_versions():
    latest = get_newest_tag()

    if latest != VERSION:
        return False
    else:
        return True