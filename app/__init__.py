# stdlib imports
import os
import urlparse

# third-party imports
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from gevent import monkey

# define WSGI app
app = Flask(__name__)

# configure mongo
try:
    mongohq_uri = os.environ['MONGOHQ_URL']
    url = urlparse.urlparse(mongohq_uri)
    app.config["MONGODB_SETTINGS"] = {
        'DB': url.path[1:],
        'USERNAME': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    }
except KeyError:
    app.config["MONGODB_SETTINGS"] = {'DB': "mmotd"}

app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# connect to database
db = MongoEngine(app)


def register_blueprints(app):
    # local imports (Prevents circular imports)
    from views.api import api
    from views.auth import auth
    from views.sockets import sockets
    from views.templates import templates
    # register blueprints
    app.register_blueprint(api, url_prefix='/api/games')
    app.register_blueprint(auth)
    app.register_blueprint(sockets, url_prefix='/socket.io')
    app.register_blueprint(templates)

# register blueprints with our WSGI app
register_blueprints(app)


# monkey patch ALL THE THINGS
monkey.patch_all()
