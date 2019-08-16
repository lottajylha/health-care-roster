from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, RadioField, IntegerField, validators

positions = [
    ('Doctor', 'Doctor'),
    ('Nurse', 'Nurse'),
    ('Practical nurse', 'Practical nurse')
    ]
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class SignupForm(FlaskForm):

    name = StringField("Name", [validators.Length(min=4, max=100), validators.Required()])
    username = StringField("Username", [validators.Length(min=4, max=100), validators.Required()])
    password = PasswordField("Password", [validators.Length(min=4, max=100), validators.Required()])
    position = RadioField("Position", [validators.Required()], choices=positions)
    
    class Meta:
        csrf = False