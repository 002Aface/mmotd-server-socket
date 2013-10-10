"""
SocketIO namespaces
"""
# stdlib imports
import datetime
import json

# third-party imports
from gevent.greenlet import Greenlet
from socketio.namespace import BaseNamespace

# local imports
from app import app
from app import db
from app.models.games import Game
from app.lib.transport import publish
from app.lib.transport import subscribe


class RoomNamespace(BaseNamespace):

    def validate(self, game_id):
        # check if user is allowed to subscribe to this channel
        player = self.request
        try:
            # attempt to pull the game from mongo so we can validate against it
            # (we probably don't want to call mongo here every time, so could
            # be made MUCH more efficient)
            game = Game.objects.get(pk=game_id)
        except db.DoesNotExist:
            return False
        if player.user_id not in game.players:
            return False
        return True

    def listener(self, channel, callback=lambda x: x):
        # subscribe to the specified channel, triggering the callback each time
        # a message is received
        for msg in subscribe(channel, callback):
            try:
                pmsg = json.loads(msg['data'])
            except TypeError:
                continue
            try:
                self.emit(pmsg['type'], pmsg['message'])
            except (KeyError, TypeError):
                app.logger.error('Unable to process message: %s' % str(msg))

    def on_chat(self, message):
        # validate that user is actually allowed to perform these actions (we
        # should probably replace this with actual channel auth negotiation at
        # the namespace level)
        game_id = message.pop('game_id')
        if not self.validate(game_id):
            self.emit('error', {'error': 'unauthorized'})
            return
        # augment the chat message with some additional info and push it into redis
        message['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
        message['name'] = self.request.name
        channel_id = game_id + '-room'
        publish(channel_id, json.dumps({'type': 'chat', 'message': message}))

    def on_subscribe(self, message):
        # validate that user is actually allowed to perform these actions (we
        # should probably replace this with actual channel auth negotiation at
        # the namespace level)
        game_id = message.pop('game_id')
        if not self.validate(game_id):
            self.emit('error', {'error': 'unauthorized'})
            return
        # spawn a thread to listen for messages from redis
        channel_id = game_id + '-room'
        Greenlet.spawn(self.listener, channel_id)


class LobbyNamespace(BaseNamespace):

    def listener(self, channel, callback=lambda x: x):
        # subscribe to the specified channel, triggering the callback each time
        # a message is received
        for msg in subscribe(channel, callback):
            try:
                pmsg = json.loads(msg['data'])
            except TypeError:
                continue
            try:
                self.emit(pmsg['type'], pmsg['message'])
            except (KeyError, TypeError):
                app.logger.error('Unable to process message: %s' % str(msg))

    def on_subscribe(self, message):
        # spawn a thread to listen for messages from redis
        Greenlet.spawn(self.listener, 'lobby')
