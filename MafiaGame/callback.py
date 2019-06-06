import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a
import MafiaGame.db_access as db

BASE_URL = "http://76.250.32.204:5000"
AUTH = a.AUTH


# Ran when user sends !help command
def help_handler(bot_id, chat_type):
    if chat_type == 'main':
        gs.send_message(bot_id, "Vote on who the mafia is!")
    elif chat_type == 'mafia':
        gs.send_message(bot_id, "Trick the villagers")


def vote_handler(bot_id, game_id, user, tagged):
    players = db.get_players(game_id)
    if len(tagged) > 1:
        gs.send_message(bot_id, "You can only vote for one person!")
    elif len(tagged) < 1:
        gs.send_message(bot_id, "I did not recognize that person. Make sure you do !vote @[person name]")
    else:
        gs.send_message(bot_id, "Your vote has been counted!")


def callback(game_id, chat_type, message):
    text = message["text"].strip()
    user = message['user_id']
    game = db.get_game(game_id)
    bot_id = game.bot_id
    mentions = []
    for item in message['attachments']:
        if item['type'] == 'mentions':
            mentions=item['user_ids']

    if text.startswith("!help"):
        help_handler(bot_id, chat_type)
    elif text.startswith("!vote"):
        vote_handler(bot_id, game_id, user, mentions)
