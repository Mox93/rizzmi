from flask import redirect, url_for, render_template
from flask_wtf import FlaskForm, RecaptchaField
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash
from developer import dev_bp, redirect_auth_user_to, unique
from models.user import DeveloperModel


class DevRegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=25), unique])
    email = StringField("Email", validators=[InputRequired(), Email("Invalid email."), unique])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password', validators=[EqualTo('password', 'Passwords must match')])
    recapcha = RecaptchaField()


@dev_bp.route("/register", methods=["GET", "POST"])
@redirect_auth_user_to("admin.index")
def register():
    form = DevRegisterForm()

    if form.validate_on_submit():
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
        return redirect(url_for("profile.index"))

    return render_template("dev/registration.html", form=form)


@dev_bp.route("/delete", methods=["GET"])
@login_required
def delete():
    current_user.delete()
    logout_user()
    return redirect(url_for("site.homepage"))


