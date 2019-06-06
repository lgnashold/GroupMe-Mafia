import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a
import random
import MafiaGame.db_access as db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('game', __name__)
AUTH = a.AUTH
BASE_URL = "http://76.250.32.204:5000"

@bp.route('/',methods=('GET','POST'))
def index():
    if request.method == 'POST':

        name = request.form["title"]
        people = request.form["body"].split("\n")
        formatted_people = []

        for person in people:
            person = person.split(",")
            formatted_people.append({"nickname":person[0].strip(), "phone_number": person[1].strip()})
        
        set_up_game(name,formatted_people)
        
    return render_template('start_game.html')

@bp.route('/getinfo', methods=('GET','POST'))
def get_info():
    print("Recieved Information")

# Type is either 'mafia', 'main', or 'user'
@bp.route('/callback/<groupid>/<group_type>', methods = ['POST'])
def callback(groupid, group_type):
    data = json.loads(request.get_json())
    text = data['text'].strip()
    if( text.startswith("!help")):
        # We would put the method that actually handled commands here
        print("Help message") 
    return 'Success'


def set_up_game(name, formatted_people):
    
    size = len(formatted_people)
    num_mafia = int(size/5) + 1
    
    mafia = []

    for person in formatted_people:
        person["role"] = "Villager"

    i = 0
    while i < num_mafia:
        index = random.randint(0, size-1)
        while(formatted_people[index]["role"] == "Mafia"):
            index = random.randint(0, size)
        formatted_people[index]["role"] = "Mafia"
        mafia.append(formatted_people[index])
        i+=1
    
    groupid = gs.create_group(AUTH, "GroupMe Mafia: " + name)
    gs.add_members(AUTH, groupid, formatted_people)
    botid = gs.create_bot(AUTH, groupid, callback = f"{BASE_URL}/callback/{groupid}/main")
    
    mafiaid = gs.create_group(AUTH, "GroupMe Mafia: " + name + " [The Mafia]")
    gs.add_members(AUTH,mafiaid, mafia)
    mafiabotid = gs.create_bot(AUTH,mafiaid, callback = f"{BASE_URL}/callback/{groupid}/mafia")

    gs.send_message(botid, "Hello, and welcome to GroupMe Mafia. You are the Villagers")
    gs.send_message(mafiabotid, "Welcome, to the Mafia.")
    
    
