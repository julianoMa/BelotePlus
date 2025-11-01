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
