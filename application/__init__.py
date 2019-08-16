from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("postgres://mqnevcyqglnvvt:1b731a8ee6ee13309e34cda9e3f7c70844bfade93119013aa29d7a3cbb1c7b05@ec2-54-163-226-238.compute-1.amazonaws.com:5432/d6lkkr0943c0mm")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///roster.db"    
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from application.roster import shifts
from application.roster import views
from application.auth import models
from application.auth.models import User
from application.auth import views
from application.users import views
from application import views

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try: 
    db.create_all()
except:
    pass