from application import app, db
from flask import redirect, render_template, request, url_for
from application.roster.shifts import Shift
from application.roster.forms import ShiftForm

@app.route("/roster/new/")
def shifts_form():
    return render_template("shifts/shift.html", form=ShiftForm())


@app.route("/roster/", methods=["POST"])
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


