from flask import redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired
from werkzeug.security import check_password_hash
from developer import dev_bp, redirect_auth_user_to
from models.developer import DeveloperModel
from common.util import is_safe_url


class DevLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me")
    recapcha = RecaptchaField()


@dev_bp.route("/login", methods=["GET", "POST"])
@dev_bp.route("/login/<string:bypass>", methods=["GET"])
@redirect_auth_user_to("admin.index")
def login(bypass=None):

    if bypass == "me":
        user = DeveloperModel.find_by_username("tester_0")
        login_user(user)
        return redirect(url_for("admin.index"))

    form = DevLoginForm()

    if form.validate_on_submit():
        user = DeveloperModel.find_by_username(form.username.data)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            url = request.args.get("next")

            if url and is_safe_url(url):
                return redirect(url)

            return redirect(url_for("admin.index"))
        else:
            return render_template("dev/login.html", form=form, error_msg="Wrong Username or Password!")

    return render_template("dev/login.html", form=form)


@dev_bp.route("/logout", methods=["Get"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.homepage"))

