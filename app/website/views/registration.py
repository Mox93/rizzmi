from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from website import site_bp


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("What should we call you?")])
    password = PasswordField("Password", validators=[InputRequired("Keep you account safe!"),
                                                     Length(min=8, message="This password is too short!")])
    recapcha = RecaptchaField()


@site_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        return f"<h1>Thank you {form.username.data} for registering.</h1>"

    return render_template("registration.html", form=form)


