# File for code that runs when a new game is made
import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a
import random, json
import MafiaGame.db_access as db

BASE_URL = "http://76.250.32.204:5000"
AUTH = a.AUTH


# Sets up the groupme part of the application
def set_up_game_groups(name, formatted_people, mafia):
    groupid = gs.create_group(AUTH, "GroupMe Mafia: " + name)
    gs.add_members(AUTH, groupid, formatted_people)
    botid = gs.create_bot(AUTH, groupid, callback=f"{BASE_URL}/callback/{groupid}/main")

    mafiaid = gs.create_group(AUTH, "GroupMe Mafia: " + name + " [The Mafia]")
    gs.add_members(AUTH, mafiaid, mafia)
    mafiabotid = gs.create_bot(AUTH, mafiaid, callback=f"{BASE_URL}/callback/{groupid}/mafia")

    # Get user id numbers
    users = gs.get_user_ids(AUTH, groupid)
    users = {users[key]: key for key in users.keys()}
    for person in formatted_people:
        person['id'] = users[person['nickname']]

    return {"gameid": groupid, "botid": botid, "mafiaid": mafiaid, "mafiabotid": mafiabotid,
            "players": formatted_people}


# Sends the welcome messages
def send_welcome_messages(game_dict):
    gs.send_message(game_dict["botid"], "Hello, and welcome to GroupMe Mafia. You are the Villagers")
    gs.send_message(game_dict["mafiabotid"], "Welcome, to the Mafia.")


# Entry point
def set_up_game(name, formatted_people):
    size = len(formatted_people)
    num_mafia = int(size / 5) + 1

    mafia = []

    for person in formatted_people:
        person["role"] = "Villager"

    i = 0
    while i < num_mafia:
        index = random.randint(0, size - 1)
        while formatted_people[index]["role"] == "Mafia":
            index = random.randint(0, size)
        formatted_people[index]["role"] = "Mafia"
        mafia.append(formatted_people[index])
        i += 1

    # game is dict that holds fields for groupid, botid, mafiaid, mafiabotid, and people
    game = set_up_game_groups(name, formatted_people, mafia)
    send_welcome_messages(game)
    db.make_game_table(game)
