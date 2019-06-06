import os
import sys
#from sqlalchemy import Column, ForeignKey, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
#from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Base = declarative_base()

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True) #groupme membership id
    name = db.Column(db.String(250), nullable=False) #groupme nickname
    phone_number = db.Column(db.String(250), nullable=False) #groupme phone number
    role = db.Column(db.String(250), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship("Game", back_populates = "players")

class Vote(db.Model):
    __tablename__ = 'votes'

    id_from = db.Column(db.Integer, primary_key=True) #membership id
    id_for = db.Column(db.Integer, nullable=False) #membership id for who the vote is for
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship("Game", back_populates = "votes")

class Game(db.Model):
    __tablename__ = "games"
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, nullable=False)
    mafia_id = db.Column(db.Integer, nullable=False)
    mafia_bot_id = db.Column(db.Integer, nullable=False)
    players = db.relationship("Player", back_populates="game")
    votes = db.relationship("Vote", back_populates="game")
  


def init_db():
    db.drop_all()
    db.create_all()
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = db.create_engine('sqlite:///sqllite_test.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.

