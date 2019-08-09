from application import app, db
from flask import redirect, render_template, request, url_for
from application.roster.shifts import Shift

days = [
    "2019-09-02",
    "2019-09-03",
    "2019-09-04",
    "2019-09-05",
    "2019-09-06",
    "2019-09-07",
    "2019-09-08"
]

hours = [
    "7-8",
    "8-9",
    "9-10",
    "10-11",
    "11-12",
    "12-13",
    "13-14",
    "14-15",
    "15-16",
    "16-17"
]

@app.route("/roster/new/")
def shifts_form():
    return render_template("shifts/shift.html", hours=hours, days=days)


@app.route("/roster/", methods=["POST"])
def create_shift():
    NewShift = Shift(request.form["day"], request.form["hour"], request.form.get("doctorsNeeded"), request.form.get("nursesNeeded"),request.form.get("practicalNursesNeeded"))

    db.session().add(NewShift)
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


