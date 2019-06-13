import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a
import MafiaGame.db_access as db
from collections import defaultdict

BASE_URL = "http://76.250.32.204:5000"
AUTH = a.AUTH


# Ran when user sends !help command
def help_handler(bot_id, chat_type):
    if chat_type == 'main':
        gs.send_message(bot_id, "Vote on who the mafia is!")
    elif chat_type == 'mafia':
        gs.send_message(bot_id, "Trick the villagers")


def handle_majority(bot_id, game_id, force_night = False):
    # Parses dictionary
    votes = db.get_votes(game_id)
    if votes is None:
        return None
    final_votes = defaultdict(list)
    for vote in votes:
        final_votes[vote.id_for].append(vote.id_from)
    votes = final_votes

    players = db.get_players(game_id)
    max = 0
    top = None
    message = ''
    for vote_for, votes_from in votes.items():
        vote_for = db.get_player(vote_for)
        votes_from = [db.get_player(x).name for x in votes_from]
        count = len(votes_from)
        message += f'{vote_for.name} received {count} votes ( {", ".join(votes_from)})\n'
        if count > max:
            max = count
            top = vote_for
    summary = ''
    if max > len(players) / 2:
        summary = f'{top.name.title()} has been hanged. They were a {top.role}. '
    else:
        summary = 'No majority was reached :(. '
        if not force_night:
            return
    summary += "It is now nighttime. No talking."
    gs.send_message(bot_id, message)
    gs.send_message(bot_id, summary)


def update_votes(bot_id, game_id, user, tagged):
    players = db.get_players(game_id)
    if len(tagged) > 1:
        gs.send_message(bot_id, "You can only vote for one person!")
    elif len(tagged) < 1:
        gs.send_message(bot_id, "I did not recognize that person. Make sure you do !vote @[person name]")
    else:
        db.add_vote(user, tagged[0], game_id)
        try:
            gs.send_message(bot_id, "Your vote has been counted!")
        except:
            gs.send_message(bot_id, "An error occured counting your vote")
        handle_majority(bot_id, game_id)


def callback(game_id, chat_type, message):
    print(message['attachments'])
    text = message["text"].strip()
    user = message['user_id']
    game = db.get_game(game_id)
    if game is None:
        return
    bot_id = game.bot_id
    mentions = []
    for item in message['attachments']:
        if item['type'] == 'mentions':
            mentions=item['user_ids']

    if text.startswith("!help"):
        help_handler(bot_id, chat_type)
    elif text.startswith("!vote"):
        update_votes(bot_id, game_id, user, mentions)
