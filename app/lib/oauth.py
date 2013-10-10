# stdlib imports
import json
import urllib2

# third-party imports
from flask import session
from flask_oauth import OAuth

# local imports
from app import db
from app.models.users import User


# init the oauth client
oauth = OAuth()
google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key='963889333964.apps.googleusercontent.com',
    consumer_secret='IPAGcrzCEmCu6CumkoKx4e3l'
)


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def get_user(session):
    """
    Given a session (dict-like object), returns a user object, or None if
    not logged in
    """

    # check if we already have a user id in the session, if so attempt to pull
    # the user data from mongo
    user_id = session.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except db.DoesNotExist:
        pass
    else:
        return user

    # if we don't already have user details stored then check if we have an
    # access token retrieved via the oauth process
    access_token = session.get('access_token')
    if access_token is None:
        return None

    # build the request object
    headers = {'Authorization': 'OAuth '+ access_token[0]}
    req = urllib2.Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)

    # make the request, catching any http errors
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError:
        return None
    else:
        user_data = json.loads(res.read())
        user = User(user_id=user_data['id'], email=user_data['email'], name=user_data['name'])
        if 'picture' in user_data:
            user.avatar = user_data['picture']
        else:
            user.avatar = 'https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg'
        user = user.save()
        return user
