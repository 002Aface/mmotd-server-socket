# stdlib imports
import datetime

# third-party imports
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

# local imports
from app.lib.oauth import get_user
from app.models.games import Game

# declare blueprint
templates = Blueprint('templates', __name__)


@templates.route("/")
def index():
    """Render splash page, no auth required
    """
    return render_template("index.html")


@templates.route("/lobby/")
def lobby():
    """Render lobby page, auth required
    """
    # authorise user
    player = get_user(session)
    if player is None:
        flash('You need to log in before you can access that page', 'warning')
        return redirect(url_for('.index'))

    # render lobby template if authorised
    return render_template("lobby/lobby.html", user=player)


@templates.route("/lobby/<game_id>/")
def room(game_id):
    """Render lobby page, auth required
    """
    # get game from db
    game = Game.objects.get(pk=game_id)
    if game is None:
        return render_template("404.html"), 404

    # authorise the user or redirect to index
    player = get_user(session)
    if player is None:
        flash('You need to log in before you can access that page', 'warning')
        return redirect(url_for('.index'))

    # if the game has already started, don't allow anyone else into the room
    if game.started:
        flash('Sorry, that game has already started', 'warning')
        return redirect(url_for('.lobby'))

    # add player to game
    game = game.add_player(player.user_id)
    if not player.user_id in game.players:
        flash('Sorry, that game is full', 'warning')
        return redirect(url_for('.lobby'))

    # timestamp to show as first message in chat
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'

    # render lobby template if authorised
    return render_template("lobby/room.html", user=player, game=game, timestamp=timestamp)


@templates.route("/game/<game_id>/")
def game(game_id):
    """Render lobby page, auth required
    """
    # get game from db
    game = Game.objects.get(pk=game_id)
    if game is None:
        return render_template("404.html"), 404

    # authorise the user or redirect to index
    player = get_user(session)
    if player is None:
        flash('You need to log in before you can access that page', 'warning')
        return redirect(url_for('.index'))

    # if the game has already ended, don't allow anyone else into the room
    if game.ended:
        flash('Sorry, that game has ended', 'warning')
        return redirect(url_for('.lobby'))

    # ensure player is in this game
    if not player.user_id in game.players:
        flash('You are not authorised to access that game', 'warning')
        return redirect(url_for('.lobby'))

    # render lobby template if authorised
    return render_template("game/game.html", user=player)
