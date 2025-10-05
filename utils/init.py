import os
from utils.db import *

def db_checks():
    if not os.path.exists('data/belote.db'):
        open("data/belote.db", "x")

    if len(get_tables()) == 0:
        init_db()

    return True