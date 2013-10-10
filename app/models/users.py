# stdlib imports
import datetime

# local imports
from app import db


class User(db.Document):

    created = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    user_id = db.StringField(max_length=255, required=True, primary_key=True)
    email = db.StringField(max_length=255, required=True)
    name = db.StringField(max_length=255, required=True)
    avatar = db.StringField(max_length=255)

    def __unicode__(self):
        return self.user_id

    meta = {
        'indexes': ['-created', 'user_id'],
        'ordering': ['name']
    }

    def to_dict(self):
        return {
            'created': self.created.isoformat(),
            'user_id': self.user_id,
            'avatar': self.avatar,
            'email': self.email,
            'name': self.name,
        }
