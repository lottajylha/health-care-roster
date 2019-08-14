from application import app, db
from flask import redirect, render_template, request, url_for
from application.roster.shifts import Shift
from application.users.forms import UsersForm
from application.auth.models import User
from flask_login import login_required, current_user
from functools import wraps
from flask_login import LoginManager

login_manager = app.login_manager

def login_required(position="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_manager.unauthorized()
            if ((current_user.position != position) and (position != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route("/users/set/")
def users_form():
    return render_template("users/userlistform.html", form=UsersForm())

@app.route("/users/", methods=["GET"])
def users_index():
    return render_template("users/userlistform.html", users=User.query.all(), form=UsersForm())

@app.route("/users/<user_id>/", methods=["POST"])
def set_weekhours(user_id):
    form = UsersForm(request.form)
    print('user id: ' + user_id)
    user = User.query.get(user_id)
    
    user.weekMin = form.weekMin.data
    user.weekMax = form.weekMax.data
    db.session().commit()
  
    return redirect(url_for("users_index"))