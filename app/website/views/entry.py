from flask import render_template, request, redirect, url_for, abort
from website import site_bp
from models.entry import EntryModel
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired


@site_bp.route("/forms/<string:_id>/entry", methods=["GET", "POST"])
def form_entry(_id):
    class F(FlaskForm):
        pass

    entry = EntryModel.find_by_id(_id)

    for field in entry.form.fields:
        setattr(F, f"field_{field._id}", StringField(field.displayed_text, validators=[InputRequired(field.help_text)]))

    form = F()

    if request.method == "POST":
        return "<h2> Thank you form filling in the form </h2>"

    return render_template("form_entry.html", form=form, element=entry.form)

