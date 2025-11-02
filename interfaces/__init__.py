# This package contains code that interact with outer layers like routes, APIs, real-time data, etc :
# - routes/        :     Contains all routes for Flask.

from .routes import *

def register_bps(app):
    """Importe et enregistre tous les Blueprints du projet"""
    app.register_blueprint(edit_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(manage_tournaments_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(ranking_bp)
    app.register_blueprint(rounds_bp)