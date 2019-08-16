from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import text

app = Flask(__name__)

bcrypt = Bcrypt(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("postgres://snnlswkguzzund:752839388705fd379c1a0fdc85226a809ee3a6e632dd12721875db83e28deadb@ec2-23-21-186-85.compute-1.amazonaws.com:5432/dforhgl806k8lt")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"    
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
    if os.environ.get("HEROKU"):
         stmt = text("INSERT INTO account (name, username, password, position, weekMin, weekMax)"
                    " VALUES ('Username', 'username', '|$2b$12$3EqwG.UrapGKnsi.Sg2jxuL.WKvFO06Og5ZXOUpqNkfQt0G4TRYI2', 'Employer', 0, 0);")
        db.engine.execute(stmt)
except:
    pass