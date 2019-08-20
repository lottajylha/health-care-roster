from application import app, db, flask_bcrypt
from flask import render_template, request, redirect, url_for
from application.auth.models import User
from application.auth.forms import LoginForm, SignupForm
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, RadioField, IntegerField

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_manager.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route("/auth/new/")
def signup_form():
    return render_template("auth/signupform.html", form=SignupForm())


@app.route("/auth/", methods=["POST"])
def auth_signup():
    form = SignupForm(request.form)

    if not form.validate():
        return render_template("auth/signupform.html", form = form)

    duplicate_username = User.query.filter_by(username=form.username.data).first()
    if duplicate_username:
        return render_template("auth/signupform.html", form = form,
                            error = "Username is not available.")
    else:
        encoded_password = form.password.data.encode('utf-8')
        password_hash = flask_bcrypt.generate_password_hash(encoded_password, 10)
        user = User(form.name.data, form.username.data, password_hash, form.position.data)

        db.session().add(user)
        db.session().commit()

        return redirect(url_for("roster_index"))


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    
    username = form.username.data
    password = form.password.data
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return render_template("auth/loginform.html", form = form,
                            error = "Username was not found.")
    else:
        password_hash = user.password
        is_password_correct = flask_bcrypt.check_password_hash(password_hash, password)
        if not is_password_correct:
            return render_template("auth/loginform.html", form = form,
                                error = "Password is incorrect.")
        else: 
            login_user(user)
            return redirect(url_for("roster_index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("roster_index"))  