from application import app, db
from flask import redirect, render_template, request, url_for
from application.roster.shifts import Shift
from application.roster.forms import ShiftForm
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


@app.route("/roster/new/")
@login_required('doctor')
def shifts_form():
    return render_template("shifts/shift.html", form=ShiftForm())


@app.route("/roster/", methods=["POST"])
@login_required('doctor')
def create_shift():
    form = ShiftForm(request.form)

    if not form.validate():
        return render_template("shifts/shift.html", form = form)

    shift = Shift(form.day.data, form.hour.data, form.doctorsNeeded.data, form.nursesNeeded.data, form.practicalNursesNeeded.data)

    db.session().add(shift)
    db.session().commit()
  
    return redirect(url_for("roster_index"))

@app.route("/roster/", methods=["GET"])
def roster_index():
    return render_template("shifts/list.html", shifts = Shift.query.all())

@app.route("/roster/<shift_id>/", methods=["POST"])
@login_required('doctor')
def shift_set_staff_needed(shift_id):

    if request.form.get("d+"):
        shift = Shift.query.get(shift_id)
        shift.doctorsNeeded = shift.doctorsNeeded+1
        db.session().commit()
    elif request.form.get("d-"):
        shift = Shift.query.get(shift_id)
        shift.doctorsNeeded = max(shift.doctorsNeeded-1,0)
        db.session().commit()
    elif request.form.get("n+"):
        shift = Shift.query.get(shift_id)
        shift.nursesNeeded = shift.nursesNeeded+1
        db.session().commit()
    elif request.form.get("n-"):
        shift = Shift.query.get(shift_id)
        shift.nursesNeeded = max(shift.nursesNeeded-1,0)
        db.session().commit()
    elif request.form.get("pn+"):
        shift = Shift.query.get(shift_id)
        shift.practicalNursesNeeded = shift.practicalNursesNeeded+1
        db.session().commit()
    elif request.form.get("pn-"):
        shift = Shift.query.get(shift_id)
        shift.practicalNursesNeeded = max(shift.practicalNursesNeeded-1,0)
        db.session().commit()

    return redirect(url_for("roster_index"))


