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
    if not form.validate():
        return render_template("users/userlistform.html", users=User.query.all(), form = form)

    hours = User.get_weekminmax(user_id)
    weekmin = hours[0][0]
    weekmax = hours[0][1]
    if not form.weekMin.data == None:
        weekmin = form.weekMin.data
    if not form.weekMax.data == None:
        weekmax = form.weekMax.data
    
    if weekmax >= weekmin:
        User.set_weekminmax(user_id, weekmin, weekmax)
        return redirect(url_for("users_index"))
    else:
        return render_template("users/userlistform.html", users=User.query.all(), form=form, error="Week minimum must be less than week maximum.")
    
    return redirect(url_for("users_index"))

@app.route("/users/get/<user_id>/", methods=["GET"])
@login_required()
def get_info(user_id):
    return render_template("users/usershifts.html", shifts=User.find_user_shifts(current_user.id))
