from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('game', __name__)

@bp.route('/')
def index():
    return render_template('start_game.html')

@bp.route('/getinfo', methods=('GET','POST'))
def get_info():
    print("Recieved Information")
