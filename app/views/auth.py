# third-party imports
from flask import Blueprint
from flask import redirect
from flask import session
from flask import url_for

# local imports
from app.lib.oauth import google

# declare blueprint
auth = Blueprint('auth', __name__)


@auth.route('/login/')
def login():
    """Redirect to google for login
    """
    callback=url_for('.authorized', _external=True)
    return google.authorize(callback=callback)


@auth.route('/authorized/')
@google.authorized_handler
def authorized(resp):
    """Callback url after successful login
    """
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('templates.lobby'))
