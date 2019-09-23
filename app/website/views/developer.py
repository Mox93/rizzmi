from functools import wraps
from flask import render_template, url_for, redirect, request  # , session
from flask_wtf import FlaskForm, RecaptchaField
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired, Email, Length, EqualTo
from website import site_bp
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from models.developer import DeveloperModel
from common.util import is_safe_url


login_manager.login_view = "site.dev_login"


@login_manager.user_loader
def load_user(user_id):
    return DeveloperModel.find_by_id(user_id)


def unique(form, field):
    print(">>> Check for uniqueness")
    user = DeveloperModel.find_by_(field.id, field.data)
    print(">>> Check was successful")
    if user:
        raise ValidationError(f"'{field.data}' already exists.")


def redirect_active_user_to(endpoint):
    def active_user_check(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if current_user.is_active:
                return redirect(url_for(endpoint))
            return func(*args, **kwargs)
        return func_wrapper
    return active_user_check


class DevRegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=25), unique])
    email = StringField("Email", validators=[InputRequired(), Email("Invalid email."), unique])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password', validators=[EqualTo('password', 'Passwords must match')])
    recapcha = RecaptchaField()


class DevLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me")
    recapcha = RecaptchaField()


@site_bp.route("/developers/register", methods=["GET", "POST"])
@redirect_active_user_to("site.dev_home")
def dev_register():
    form = DevRegisterForm()

    if form.validate_on_submit():
        print(f">>> Register Form Valid")
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        # noinspection PyArgumentList
        new_user = DeveloperModel(username=form.username.data,
                                  email=form.email.data,
                                  password=hashed_password)
        try:
            new_user.save()
        except Exception as e:
            return f"<h2> Error </h2>" \
                   f"<p> {str(e)} </p>"

        login_user(new_user, remember=False)
        return redirect(url_for("site.dev_profile"))
    print(f">>> Register Form Invalid")
    return render_template("dev_registration.html", form=form)


@site_bp.route("/developers/login", methods=["GET", "POST"])
@redirect_active_user_to("site.dev_home")
def dev_login():
    form = DevLoginForm()

    if form.validate_on_submit():
        print(f">>> Login Form Valid")
        user = DeveloperModel.find_by_username(form.username.data)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            url = request.args.get("next")  # or session.get("next")

            if url and is_safe_url(url):
                return redirect(url)

            return redirect(url_for("site.dev_profile"))
        else:
            return render_template("dev_login.html", form=form, error_msg="Wrong Username or Password!")
    print(f">>> Login Form Invalid")
    return render_template("dev_login.html", form=form)


@site_bp.route("/developers/profile", methods=["Get"])
@login_required
def dev_profile():
    return render_template("dev_profile.html")


@site_bp.route("/developers", methods=["Get"])
@login_required
def dev_home():
    return render_template("dev_home.html")


@site_bp.route("/developers/logout", methods=["Get"])
@login_required
def dev_logout():
    logout_user()
    return redirect(url_for("site.homepage"))

