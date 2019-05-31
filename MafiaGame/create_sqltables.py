import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True) #groupme membership id
    name = Column(String(250), nullable=False) #groupme nickname
    phone_number = Column(String(250), nullable=False) #groupme phone number
    role = Column(String(250), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("Game", back_populates = "players")

class Vote(Base):
    __tablename__ = 'votes'

    id_from = Column(Integer, primary_key=True) #membership id
    id_for = Column(Integer, nullable=False) #membership id for who the vote is for
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("Game", back_populates = "votes")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, nullable=False)
    mafia_id = Column(Integer, nullable=False)
    mafia_bot_id = Column(Integer, nullable=False)
    players = relationship("Player", back_populates="game")
    votes = relationship("Vote", back_populates="game")
  
    
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqllite_test.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
