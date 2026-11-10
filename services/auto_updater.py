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

import re
import time

import requests
from flask import request

from config.settings import VERSION

RELEASES_URL = "https://api.github.com/repos/julianoMa/BelotePlus/releases/latest"
CHECK_INTERVAL = 6 * 60 * 60  # seconds between two checks on GitHub
REQUEST_TIMEOUT = 3  # seconds, so the home page never hangs when offline

def get_newest_tag():
    """Renvoie le tag de la dernière release GitHub, ou None si on n'a pas pu le récupérer"""
    try:
        response = requests.get(RELEASES_URL, timeout=REQUEST_TIMEOUT)
        tag = response.json()["tag_name"]
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        # No connection, timeout, rate limit, invalid answer...
        return None

    return tag if isinstance(tag, str) else None

def get_latest_version():
    """Renvoie (dernière version connue, vérification faite maintenant ?).

    La version est lue dans le cookie tant que la dernière vérification date de moins de
    6h ; sinon GitHub est interrogé. En cas d'échec, l'ancienne version connue est gardée
    (ou None) et la prochaine tentative n'aura lieu que dans 6h.
    """
    cached = request.cookies.get("last_version")

    try:
        age = time.time() - float(request.cookies.get("last_update"))
    except (TypeError, ValueError):
        age = None

    if cached and age is not None and 0 <= age <= CHECK_INTERVAL:
        return cached, False

    return get_newest_tag() or cached, True

def parse_version(tag):
    """Convertit un tag comme 'v0.3.1' en (0, 3, 1), ou None si ce n'est pas une version"""
    numbers = re.findall(r"\d+", tag or "")
    return tuple(int(n) for n in numbers) if numbers else None

def compare_versions(latest, current=VERSION):
    """True si la version actuelle est à jour (ou plus récente que la dernière release)"""
    latest_parsed = parse_version(latest)
    current_parsed = parse_version(current)

    if latest_parsed is None or current_parsed is None:
        return True  # Unknown latest version: do not bother the user

    return current_parsed >= latest_parsed
