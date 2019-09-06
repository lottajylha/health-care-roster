from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, validators
from application.auth.models import User

class UsersForm(FlaskForm):
    
    weekMin = IntegerField("Minimum hours", [validators.Optional(strip_whitespace=True),validators.NumberRange(min=0, max=50, message="Week minimum must be an integer between 0 and 50.")])
    weekMax = IntegerField("Maximum hours", [validators.Optional(strip_whitespace=True),validators.NumberRange(min=0, max=50, message="Week maximum must be an integer between 0 and 50.")])
 
    class Meta:
        csrf = False
