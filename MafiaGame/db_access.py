from MafiaGame.create_sqltables import Player, Vote, Game, db

#engine = create_engine('sqlite:///sqllite_test.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = db.session


def make_game_table(game):
    player_list = []
    for m in game['players']:
        p = Player(id=m["id"], name=m["nickname"], role=m["role"], phone_number=m["phone_number"])
        session.add(p)
        player_list.append(p)

    game = Game(id=game['gameid'], bot_id=game['botid'], mafia_id=game['mafiaid'], mafia_bot_id=game['mafiabotid'],
                players=player_list)
    session.commit()
    return game

def add_vote(vote, game):
    v = Vote(id_from = vote["id_from"], id_for = vote["id_for"], game_id = game["id"], game = game)
    v.add()
    v.commit()

def get_votes(game_id):
    session.query(Vote).filter(Vote.game_id == game_id)


def clear_votes(game_id):
    for vote in get_votes:
        db.session.remove(vote)
        db.commit()

def get_mafia_members(game_id):
    return get_players(game_id).filter(Player.role == "Mafia")


def get_players(game_id):
    return session.query(Player).filter(Player.game_id == game_id)

def get_player(player_id):
    return session.query(Player).filter(Player.id == player_id)

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
