import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('game', __name__)
AUTH = a.AUTH

@bp.route('/',methods=('GET','POST'))
def index():
    if request.method == 'POST':

        name = request.form["title"]
        people = request.form["body"].split("\n")
        formatted_people = []

        for person in people:
            person = person.split(",")
            formatted_people.append({"nickname":person[0].strip(), "phone_number": person[1].strip()})

        
        groupid = gs.create_group(AUTH)
        gs.add_members(AUTH, groupid, formatted_people)
        botid = gs.create_bot(AUTH, groupid)
        gs.send_message(botid, "Hello, and welcome to the game of mafia")

        
    return render_template('start_game.html')

@bp.route('/getinfo', methods=('GET','POST'))
def get_info():
    print("Recieved Information")
