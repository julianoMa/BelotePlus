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

import ast

def repartition_ast(repartition):
    """Convertis des strings en objets Python"""
    r = []
    for tournament, cround, table, teams in repartition:
        if isinstance(teams, str):
            teams = ast.literal_eval(teams)
        r.append({"tournament": tournament, "round": cround, "table": table, "team1": teams[0], "team2": teams[1]})

    return r 