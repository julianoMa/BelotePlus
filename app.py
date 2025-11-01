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


import sys
sys.dont_write_bytecode = True

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

from common import *
from core import *
from data import *
from services import *
from interfaces import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Register routes
register_bps(app)

# Load multi-languages support
load_translations()

@app.context_processor
def inject_language():
    """inject lang in all templates"""
    lang = request.cookies.get('language', 'fr')
    return {
        'current_lang': lang,
        't': get_all_translations(lang)
    }

@app.route("/set-language/<lang>")
def set_language(lang):
    """change user lang"""
    if lang not in ['fr', 'en']:
        lang = 'fr'
    
    resp = make_response(redirect(request.referrer or url_for('index')))
    resp.set_cookie('language', lang, max_age=31536000)
    return resp

if __name__ == "__main__":
    print("🛠️  Starting checks...")
    if db_checks() == True:
        print("✅ Database ")
        
    start_server(app)