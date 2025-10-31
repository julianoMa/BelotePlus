from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Tournament(Base):
    __tablename__ = 'tournaments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    rounds_number = Column(Integer, nullable=False)
    tables_number = Column(Integer, nullable=False)
    step = Column(Integer, default=0, nullable=False)
    
    # relations
    teams = relationship('Team', back_populates='tournament', cascade='all, delete-orphan')
    rankings = relationship('Ranking', back_populates='tournament', cascade='all, delete-orphan')
    teams_points = relationship('TeamPoints', back_populates='tournament', cascade='all, delete-orphan')
    repartitions = relationship('Repartition', back_populates='tournament', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Tournament(id={self.id}, name='{self.name}', rounds={self.rounds_number})>"


class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    player1 = Column(String, nullable=False)
    player2 = Column(String, nullable=False)
    
    # relations
    tournament = relationship('Tournament', back_populates='teams')
    rankings = relationship('Ranking', back_populates='team', cascade='all, delete-orphan')
    points = relationship('TeamPoints', back_populates='team', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Team(id={self.id}, player1='{self.player1}', player2='{self.player2}')>"


class Ranking(Base):
    __tablename__ = 'ranking'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    points = Column(Integer, nullable=False, default=0)
    
    # relations
    tournament = relationship('Tournament', back_populates='rankings')
    team = relationship('Team', back_populates='rankings')
    
    def __repr__(self):
        return f"<Ranking(tournament_id={self.tournament_id}, team_id={self.team_id}, points={self.points})>"


class TeamPoints(Base):
    __tablename__ = 'teams_points'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    round_id = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    points = Column(Integer, default=0)
    
    # relations
    tournament = relationship('Tournament', back_populates='teams_points')
    team = relationship('Team', back_populates='points')
    
    def __repr__(self):
        return f"<TeamPoints(tournament_id={self.tournament_id}, round={self.round_id}, team_id={self.team_id}, points={self.points})>"


class Repartition(Base):
    __tablename__ = 'repartition'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    round = Column(Integer, nullable=False)
    tablenumber = Column(Integer, nullable=False)
    teams = Column(String, nullable=False)  # Stocké comme string représentant un tuple
    
    # relations
    tournament = relationship('Tournament', back_populates='repartitions')
    
    def __repr__(self):
        return f"<Repartition(tournament_id={self.tournament_id}, round={self.round}, table={self.tablenumber})>"
