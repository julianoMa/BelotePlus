import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .models import Base, Tournament, Team, Ranking, TeamPoints, Repartition


# config db
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'belote.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

# engine et session
engine = create_engine(DATABASE_URL, echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def get_session():
    """Context manager pour gérer automatiquement les sessions"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def init_db():
    """Initialise la base de données en créant toutes les tables"""
    Base.metadata.create_all(engine)


def get_tables():
    """Retourne la liste des tables dans la base de données"""
    inspector = inspect(engine)
    return [(table,) for table in inspector.get_table_names()]


# ======================
# TOURNAMENTS
# ======================

def get_tournaments_names():
    """Récupère tous les noms de tournois"""
    with get_session() as session:
        tournaments = session.query(Tournament.name).order_by(Tournament.id).all()
        return [t.name for t in tournaments]


def create_tournament(name, rounds_number, tables_number):
    """Crée un nouveau tournoi"""
    with get_session() as session:
        tournament = Tournament(
            name=name,
            rounds_number=rounds_number,
            tables_number=tables_number,
            step=0
        )
        session.add(tournament)


def get_tournament_id(tournament_name):
    """Récupère l'ID d'un tournoi par son nom"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        return tournament.id if tournament else None


def get_tournament_by_name(tournament_name):
    """Récupère un tournoi par son nom"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            # detach object from session before returning, so it can be used outside
            session.expunge(tournament)
        return tournament


def delete_tournament(tournament_name):
    """Supprime un tournoi par son nom"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            session.delete(tournament)


def get_step(tournament_name):
    """Récupère l'étape actuelle d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        return tournament.step if tournament else 0


def update_step(tournament_name, step):
    """Met à jour l'étape d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            tournament.step = step


def get_rounds(tournament_name):
    """Récupère le nombre de rounds d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        return tournament.rounds_number if tournament else 0


# ======================
# TEAMS
# ======================

def get_teams(tournament_name):
    """Récupère toutes les équipes d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if not tournament:
            return []
        
        teams = session.query(Team).filter_by(tournament_id=tournament.id).all()
        # convert to tuples for compatibility with previous implementation
        return [(t.id, tournament_name, t.player1, t.player2) for t in teams]


def add_team(tournament_name, player1, player2):
    """Ajoute une équipe à un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            team = Team(
                tournament_id=tournament.id,
                player1=player1,
                player2=player2
            )
            session.add(team)


def delete_team(team_id, tournament_name):
    """Supprime une équipe d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            team = session.query(Team).filter_by(
                id=team_id,
                tournament_id=tournament.id
            ).first()
            if team:
                session.delete(team)


# ======================
# REPARTITION
# ======================

def update_repartition(tournament_name, round_num, table_number, teams):
    """Met à jour la répartition des équipes pour un round"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            repartition = Repartition(
                tournament_id=tournament.id,
                round=round_num,
                tablenumber=table_number,
                teams=teams
            )
            session.add(repartition)


def check_repartition(tournament_name):
    """Vérifie si une répartition existe pour un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if not tournament:
            return None
        
        repartition = session.query(Repartition).filter_by(
            tournament_id=tournament.id
        ).first()
        return (repartition.round,) if repartition else None


def clear_repartition():
    """Supprime toutes les répartitions"""
    with get_session() as session:
        session.query(Repartition).delete()


def get_repartition(round_num):
    """Récupère la répartition pour un round spécifique"""
    with get_session() as session:
        repartitions = session.query(Repartition).filter_by(round=round_num).all()
        # convert to tuples for compatibility with previous implementation
        return [(r.tournament_id, r.round, r.tablenumber, r.teams) for r in repartitions]


# ======================
# POINTS
# ======================

def save_points(tournament_name, round_num, team_id, points):
    """Sauvegarde les points d'une équipe pour un round"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            team_points = TeamPoints(
                tournament_id=tournament.id,
                round_id=round_num,
                team_id=team_id,
                points=points
            )
            session.add(team_points)

def clear_points():
    """Supprime tous les points"""
    with get_session() as session:
        session.query(TeamPoints).delete()


def get_points(tournament_name, team_id):
    """Récupère tous les points d'une équipe dans un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if not tournament:
            return []
        
        points = session.query(TeamPoints.points).filter_by(
            tournament_id=tournament.id,
            team_id=team_id
        ).all()
        return points


# ======================
# RANKING
# ======================

def save_ranking(tournament_name, team_id, points):
    """Sauvegarde le classement d'une équipe"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            ranking = Ranking(
                tournament_id=tournament.id,
                team_id=team_id,
                points=points
            )
            session.add(ranking)


def get_ranking(tournament_name):
    """Récupère le classement d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if not tournament:
            return []
        
        rankings = session.query(Ranking.team_id).filter_by(
            tournament_id=tournament.id
        ).order_by(Ranking.points.desc()).all()
        return [r.team_id for r in rankings]


def clear_previous_ranking(tournament_name):
    """Supprime le classement précédent d'un tournoi"""
    with get_session() as session:
        tournament = session.query(Tournament).filter_by(name=tournament_name).first()
        if tournament:
            session.query(Ranking).filter_by(tournament_id=tournament.id).delete()
