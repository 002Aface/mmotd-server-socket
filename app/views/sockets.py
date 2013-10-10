# third-party imports
from flask import Blueprint
from flask import Response
from flask import jsonify
from flask import request
from flask import session
from socketio import socketio_manage

# local imports
from app.lib.namespace import RoomNamespace
from app.lib.namespace import LobbyNamespace
from app.lib.oauth import get_user

# declare blueprint
sockets = Blueprint('sockets', __name__)


@sockets.route('/<path:rest>')
def push_stream(rest):
    """SocketIO connection handler
    """

    # authorise the user or return a 401
    player = get_user(session)
    if player is None:
        return jsonify(error='401 Unauthorized'), 401

    try:
        # socketio never actually uses the request object we pass in, it's just
        # for convenience, so we just pass in the player object itself, to
        # avoid flask throwing errors about using the request out of context
        socketio_manage(request.environ, {'/lobby': LobbyNamespace, '/room': RoomNamespace}, player)
    except:
        sockets.logger.error("Exception in socket", exc_info=True)
    return Response()
