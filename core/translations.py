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

import json
import os

translations_data = {}

def load_translations():
    """load translations from json file"""
    global translations_data
    translations_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'js', 'translations.json')
    try:
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations_data = json.load(f)
    except Exception as e:
        print(f"err loading translations: {e}")
        translations_data = {}

def get_translation(key, lang='fr'):
    """get specific translation for key and lang"""
    if not translations_data:
        load_translations()
    return translations_data.get(lang, {}).get(key, key)

def get_all_translations(lang='fr'):
    """get all translations for lang"""
    if not translations_data:
        load_translations()
    return translations_data.get(lang, {})
