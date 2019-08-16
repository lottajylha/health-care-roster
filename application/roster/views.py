from application import app, db
from flask import redirect, render_template, request, url_for
from application.roster.shifts import Shift
from application.auth.models import User
from application.roster.forms import ShiftForm
from flask_login import login_required, current_user
from functools import wraps
from flask_login import LoginManager
from jinja2 import Template

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

@app.route("/", methods=["GET"])
def roster():
    return redirect(url_for("roster_index"))

@app.route("/roster/new/")
@login_required('Employer')
def shifts_form():
    return render_template("shifts/shift.html", form=ShiftForm())


@app.route("/roster/", methods=["POST"])
@login_required('Employer')
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
    shifts = Shift.query.all()
    employees = []
    status = []
    is_user_shift = []
    for shift in shifts:
        shift_employees = Shift.find_users(shift.id)
        if len(shift_employees) > 0:
            employees.append(shift_employees)
        else:
            employees.append(["No employees in this shift"])
        if current_user.is_authenticated:
            if User.user_has_shift(current_user.id, shift.id):
                is_user_shift.append("Yes")
            else:
                is_user_shift.append("No")
        else:
            is_user_shift.append("No")
        status.append(Shift.status(shift.id))
    return render_template("shifts/list.html", shifts = shifts, employees=employees, status=status, usershifts=is_user_shift)

@app.route("/roster/<shift_id>/<user_id>/", methods=["POST"])
@login_required()
def set_shift(shift_id, user_id):
    if User.user_has_shift(user_id, shift_id):
        User.remove_shift(user_id, shift_id)
    else:
        need_employees_in_shift = True
        user_position = User.get_position(user_id)
        if user_position == 'Doctor':
            if Shift.doctorsNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Doctor') == 0:
                need_employees_in_shift = False
        elif user_position == 'Nurse':
            if Shift.nursesNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Nurse') == 0:
                need_employees_in_shift = False
        elif user_position == 'Practical nurse':
            if Shift.practicalNursesNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Practical nurse') == 0:
                need_employees_in_shift = False
        if need_employees_in_shift:
            User.add_shift(user_id, shift_id)
  
    return redirect(url_for("roster_index"))


@app.route("/roster/<shift_id>/", methods=["POST"])
@login_required('Employer')
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


