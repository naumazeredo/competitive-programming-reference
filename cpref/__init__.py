import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
#from flask_oauthlib.client import OAuth
from authlib.flask.client import OAuth

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))


def fetch_token():
    return session['github_token']


oauth = OAuth(app)
oauth.register(
    'github',
    #request_token_params={'scope': 'user'},
    api_base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    fetch_token=fetch_token
)

github = oauth.github

db = SQLAlchemy(app)

import cpref.views
