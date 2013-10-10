# stdlib imports
import datetime

# third-party imports
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import session
from flask.views import MethodView

# local imports
from app import db
from app.models.games import Game
from app.lib.oauth import get_user

# declare blueprint
api = Blueprint('api', __name__)


class ListView(MethodView):

    def get(self):
        """List all open games
        """

        # authorise the user or return a 401
        user = get_user(session)
        if user is None:
            return jsonify(error='401 Unauthorized'), 401

        # get datetime exactly one day ago
        window = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        # run query and serialise to python dict
        games_owned_dicts = [x.to_dict() for x in Game.objects.filter(created_at__gt=window).filter(started=False).filter(ended=False).filter(creator=user.user_id)]
        games_unowned_dicts = [x.to_dict() for x in Game.objects.filter(created_at__gt=window).filter(started=False).filter(ended=False).filter(creator__ne=user.user_id)]
        # return as JSON response
        return jsonify(owned=games_owned_dicts, unowned=games_unowned_dicts)

    def post(self):
        """Create a new game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # create new game
        max_players = request.form.get('max_players', 4)
        game = Game.new_game(player_id=player.user_id, max_players=int(max_players))
        # return as JSON response
        return jsonify(**game.to_dict())


class DetailView(MethodView):

    def get(self, game_id):
        """Get Details of a single game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # get game from db
        try:
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return jsonify(error='404 Not Found'), 404

        # return as JSON response
        return jsonify(**game.to_dict())

    def post(self, game_id):
        """Join a game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # get game from db
        try:
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return jsonify(error='404 Not Found'), 404

        # add player to game
        print type(player)
        game = game.add_player(player.user_id)
        if not player.user_id in game.players:
            return jsonify(error='403 Forbidden'), 403

        # return as JSON response
        return jsonify(**game.to_dict())


class DeleteView(MethodView):

    def post(self, game_id):
        """Delete a game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # get game from db
        try:
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return jsonify(error='404 Not Found'), 404

        # ensure player is the game's creator
        if not player.user_id == game.creator:
            return jsonify(error='403 Forbidden'), 403

        # mark the game as started and publish signal to other clients
        game = game.remove()

        # return as JSON response
        return jsonify(**{'result': 'deleted'})


class StartView(MethodView):

    def post(self, game_id):
        """Start a game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # get game from db
        try:
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return jsonify(error='404 Not Found'), 404

        # ensure player is the game's creator
        if not player.user_id == game.creator:
            return jsonify(error='403 Forbidden'), 403

        # mark the game as started and publish signal to other clients
        game = game.start()

        # return as JSON response
        return jsonify(**game.to_dict())


class LeaveView(MethodView):

    def post(self, game_id):
        """Leave a game
        """

        # authorise the user or return a 401
        player = get_user(session)
        if player is None:
            return jsonify(error='401 Unauthorized'), 401

        # get game from db
        try:
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return jsonify(error='404 Not Found'), 404

        # ensure player is the game's creator
        if not player.user_id in game.players:
            return jsonify(error='403 Forbidden'), 403

        # leave the game and let the other players know
        game = game.remove_player(player.user_id)

        # return as JSON response
        return jsonify(**game.to_dict())


# register blueprint urls
api.add_url_rule('/', view_func=ListView.as_view('api-games-list'))
api.add_url_rule('/<game_id>/', view_func=DetailView.as_view('api-games-detail'))
api.add_url_rule('/<game_id>/delete/', view_func=DeleteView.as_view('api-games-delete'))
api.add_url_rule('/<game_id>/leave/', view_func=LeaveView.as_view('api-games-leave'))
api.add_url_rule('/<game_id>/start/', view_func=StartView.as_view('api-games-start'))
