from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField, validators

class ShiftForm(FlaskForm):

    days = [
    ("2019-09-02","2019-09-02"),
    ("2019-09-03","2019-09-03"),
    ("2019-09-04","2019-09-04"),
    ("2019-09-05","2019-09-05"),
    ("2019-09-06","2019-09-06"),
    ("2019-09-07","2019-09-07"),
    ("2019-09-08","2019-09-08")
    ]

    hours = [
    ("7-8","7-8"),
    ("8-9","8-9"),
    ("9-10","9-10"),
    ("10-11","10-11"),
    ("11-12","11-12"),
    ("12-13","12-13"),
    ("13-14","13-14"),
    ("14-15","14-15"),
    ("15-16","15-16"),
    ("16-17","16-17")
    ]
    
    day = RadioField("Day", [validators.Required()],choices=days)
    hour = RadioField("Hour", [validators.Required()], choices=hours)
    doctorsNeeded = IntegerField("Doctors needed", [validators.NumberRange(min=0, max=15)])
    nursesNeeded = IntegerField("Nurses needed", [validators.NumberRange(min=0, max=15)])
    practicalNursesNeeded = IntegerField("Practical nurses needed", [validators.NumberRange(min=0, max=15)])
    addshift = SubmitField("Add shift", [validators.Required()])

    class Meta:
        csrf = False