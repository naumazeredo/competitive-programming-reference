import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.flask.client import OAuth

# TODO: refactor in multiple files?

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))

oauth = OAuth(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

import cpref.views
