import MafiaGame.groupme_services as gs
import MafiaGame.AUTHTOKEN as a
import random, json
import MafiaGame.db_access as db
import MafiaGame.setup as setup
import MafiaGame.callback as cb

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('game', __name__)
AUTH = a.AUTH
BASE_URL = "http://76.250.32.204:5000"


@bp.route('/', methods=('GET', 'POST'))
def index():
    # what to do if input isn't right
    def input_error(message):
        return "formatting error"

    if request.method == 'POST':

        name = request.form["title"]
        people = request.form["body"].split("\n")
        formatted_people = []

        for person in people:
            person = person.split(",")
            if len(person) == 2:
                formatted_people.append({"nickname": person[0].strip(), "phone_number": person[1].strip()})
            else:
                return input_error("a person is not correctly formatted")
        if len(formatted_people) < 1:
            input_error("not enough people")
        setup.set_up_game(name, formatted_people)

    return render_template('start_game.html')


@bp.route('/getinfo', methods=('GET', 'POST'))
def get_info():
    print("Recieved Information")


# Type is either 'mafia', 'main', or 'user'
@bp.route('/callback/<groupid>/<group_type>', methods=['POST'])
def callback(groupid, group_type):
    data = request.get_json()
    cb.callback(groupid, group_type, data)
    return 'Success'
