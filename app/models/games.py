# stdlib imports
import datetime
import json
import uuid

# third-party imports
from flask import url_for

# local imports
from app import db
from app.lib.transport import publish
from app.models.users import User


class Game(db.Document):

    uuid = db.StringField(max_length=255, required=True, primary_key=True)
    creator = db.StringField(max_length=255, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    max_players = db.IntField(required=True)
    players = db.ListField(db.StringField())

    # game start/end times and bools to quickly check status
    started = db.BooleanField(default=False)
    start_time = db.DateTimeField()
    ended = db.BooleanField(default=False)
    end_time = db.DateTimeField()

    @property
    def game_url(self):
        return url_for('templates.game', game_id=self.uuid)

    @property
    def room_url(self):
        return url_for('templates.room', game_id=self.uuid)

    def __unicode__(self):
        return self.uuid

    meta = {
        'indexes': ['-created_at', 'uuid', 'creator', 'started', 'ended'],
        'ordering': ['-created_at']
    }

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'created': self.created_at.strftime('%Y-%m-%d %H:%M:%S') + ' UTC',
            'max_players': self.max_players,
            'game_url': self.game_url,
            'room_url': self.room_url,
            'players': self.get_players(),
        }

    def get_players(self):
        return [User.objects.get(pk=p).to_dict() for p in self.players]

    def add_player(self, player_id):
        """Adds a player to the game"""
        if len(self.players) >= self.max_players:
            return self
        # publish a players changed event to any connected clients
        publish(self.uuid + '-room', json.dumps({'type': 'players_changed', 'message': {}}))
        # check if user is already in this game
        if player_id in self.players:
            return self
        # add player to the game and save
        self.players.append(player_id)
        game = self.save()
        publish('lobby', json.dumps({'type': 'game_changed', 'message': {}}))
        return game

    def remove_player(self, player_id):
        """Removes a player from the game"""
        try:
            del self.players[self.players.index(player_id)]
        except KeyError:
            return self
        else:
            game = self.save()
            publish(self.uuid + '-room', json.dumps({'type': 'players_changed', 'message': {}}))
            publish('lobby', json.dumps({'type': 'game_changed', 'message': {}}))
            return game

    def remove(self):
        publish('lobby', json.dumps({'type': 'game_deleted', 'message': {'game_id': self.uuid}}))
        publish(self.uuid + '-room', json.dumps({'type': 'game_deleted', 'message': {'game_id': self.uuid}}))
        return self.delete()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.start_time = datetime.datetime.utcnow()
        publish('lobby', json.dumps({'type': 'game_started', 'message': {}}))
        publish(self.uuid + '-room', json.dumps({'type': 'game_started', 'message': {}}))
        return self.save()

    def end(self):
        if self.ended:
            return self
        if not self.started:
            self.started = True
            self.start_time = datetime.datetime.utcnow()
        self.ended = True
        self.end_time = datetime.datetime.utcnow()
        return self.save()

    @classmethod
    def new_game(cls, player_id, max_players=4):
        uuidstr = str(uuid.uuid4())
        game = cls(uuid=uuidstr, max_players=int(max_players), creator=player_id)
        game.players = [str(player_id)]
        game = game.save()
        publish('lobby', json.dumps({'type': 'game_created', 'message': game.to_dict()}))
        return game

    @classmethod
    def get_game(cls, game_id):
        return cls.objects.get(uuid=game_id)
