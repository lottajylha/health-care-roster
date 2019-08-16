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
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            if ((current_user.position != position) and (position != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route("/users/", methods=["GET"])
@login_required('Employer')
def users_index():
    return render_template("users/userlistform.html", users=User.query.all(), form=UsersForm())

@app.route("/users/<user_id>/", methods=["POST"])
@login_required('Employer')
def set_weekhours(user_id):
    form = UsersForm(request.form)
    print('user id: ' + user_id)
    hours = User.get_weekminmax(user_id)
    weekMin = hours[0]
    weekMax = hours[0]
    if form.weekMin.data:
        weekMin = form.weekMin.data
    if form.weekMax.data:
        weekMax = form.weekMax.data
    User.set_weekminmax(user_id, weekMin, weekMax)
  
    return redirect(url_for("users_index"))

@app.route("/users/get/<user_id>/", methods=["GET"])
@login_required()
def get_info(user_id):
    return render_template("users/usershifts.html", shifts=User.find_user_shifts(current_user.id))
