from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from MafiaGame.create_sqltables import Player, Base, Vote, Game

engine = create_engine('sqlite:///sqllite_test.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


def make_game_table(game):
    player_list = []
    for m in game['players']:
        p = Player(id=m["id"], name=m["nickname"], role=m["role"], phone_number=m["phone_number"])
        session.add(p)
        player_list.append(p)

    return Game(id=game['gameid'], bot_id=game['botid'], mafia_id=game['mafiaid'], mafia_bot_id=game['mafiabotid'],
                players=player_list)


def get_mafia_members(game_id):
    return session.query(Player).filter(Player.game_id == game_id).filter(Player.role == "Mafia")


def get_game(game_id):
    result = session.query(Game).filter(Game.id == game_id).all()
    if len(result) != 1:
        return None
    return result[0]


def get_game_from_mafia(mafia_game_id):
    result = session.query(Game).filter(Game.mafia_id == mafia_game_id).all()
    if len(result) != 1:
        return None
    return result[0]
