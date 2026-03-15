from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Tournament(Base):
    __tablename__ = 'tournaments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    rounds_number = Column(Integer, nullable=False)
    tables_number = Column(Integer, nullable=False)
    odd = Column(Boolean, default=False, nullable=False)
    step = Column(Integer, default=0, nullable=False)
    
    teams = relationship('Team', back_populates='tournament', cascade='all, delete-orphan')
    rankings = relationship('Ranking', back_populates='tournament', cascade='all, delete-orphan')
    teams_points = relationship('TeamPoints', back_populates='tournament', cascade='all, delete-orphan')
    repartitions = relationship('Repartition', back_populates='tournament', cascade='all, delete-orphan')

class Team(Base):
    __tablename__ = 'teams'

    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), primary_key=True)
    team_id = Column(Integer, primary_key=True) 

    player1 = Column(String, nullable=False)
    player2 = Column(String, nullable=False)

    tournament = relationship('Tournament', back_populates='teams')
    
    # Added overlaps to silence warnings and explicit foreign_keys
    rankings = relationship(
        'Ranking', 
        back_populates='team', 
        cascade='all, delete-orphan',
        foreign_keys='[Ranking.tournament_id, Ranking.team_id]',
        overlaps="rankings,tournament"
    )
    points = relationship(
        'TeamPoints', 
        back_populates='team', 
        cascade='all, delete-orphan',
        foreign_keys='[TeamPoints.tournament_id, TeamPoints.team_id]',
        overlaps="teams_points,tournament"
    )

class Ranking(Base):
    __tablename__ = 'ranking'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ['tournament_id', 'team_id'],
            ['teams.tournament_id', 'teams.team_id'],
            ondelete='CASCADE'
        ),
    )

    # Added overlaps to the parent relationships
    tournament = relationship('Tournament', back_populates='rankings', overlaps="rankings")
    team = relationship(
        'Team', 
        back_populates='rankings', 
        foreign_keys=[tournament_id, team_id],
        overlaps="rankings,tournament"
    )

class TeamPoints(Base):
    __tablename__ = 'teams_points'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, nullable=False)
    round_id = Column(Integer, nullable=False)
    points = Column(Integer, default=0)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ['tournament_id', 'team_id'],
            ['teams.tournament_id', 'teams.team_id'],
            ondelete='CASCADE'
        ),
    )

    tournament = relationship('Tournament', back_populates='teams_points', overlaps="points")
    team = relationship(
        'Team', 
        back_populates='points', 
        foreign_keys=[tournament_id, team_id],
        overlaps="teams_points,tournament"
    )

class Repartition(Base):
    __tablename__ = 'repartition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False)
    round = Column(Integer, nullable=False)
    tablenumber = Column(Integer, nullable=False)
    teams = Column(String, nullable=False) 
    
    tournament = relationship('Tournament', back_populates='repartitions')