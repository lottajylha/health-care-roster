from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, validators
from application.auth.models import User

class UsersForm(FlaskForm):
    
    userform = RadioField("Employee", [validators.Required()], choices=[])
    weekMin = IntegerField("Minimum hours", [validators.NumberRange(min=0, max=50)])
    weekMax = IntegerField("Maximum hours", [validators.NumberRange(min=0, max=50)])
 
    class Meta:
        csrf = False
