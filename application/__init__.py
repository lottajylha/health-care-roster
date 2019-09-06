from flask import Flask
from flask_bcrypt import Bcrypt
import sys
import logging

app = Flask(__name__)

flask_bcrypt = Bcrypt(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://snnlswkguzzund:752839388705fd379c1a0fdc85226a809ee3a6e632dd12721875db83e28deadb@ec2-23-21-186-85.compute-1.amazonaws.com:5432/dforhgl806k8lt'
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from application.roster import shifts
from application.roster import views
from application.auth import models
from application.auth.models import User
from application.auth import views
from application.users import views
from application import views

try: 
    db.create_all()
    employer_created = User.query.filter_by(username="employer").first()
    if employer_created == None:
        password = "$2b$10$O7QM/L0fZE9PtYtA2o20auy8jgMcoiUgie7/AzI8Vrb9y1keXm6J2"
        employer = User("Employer", "employer", password.decodecode('utf8'), "Employer")
        db.session().add(employer)
        db.session().commit()
except:
    pass