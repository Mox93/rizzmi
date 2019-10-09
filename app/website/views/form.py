from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from website import site_bp
from models.form import FormModel
from models.field import EmbeddedFieldModel
from common.util import PY_DTYPES


class FieldProp(FlaskForm):
    displayed_text = StringField("Question")
    data_type = SelectField("Input Type", choices=list(PY_DTYPES.keys()))
    help_text = TextAreaField("Description")
    required = BooleanField("Required")


@site_bp.route("/forms", methods=["GET", "POST"])
@login_required
def form_list():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormModel.find_by_id(_id)
        new_name = request.form.get("new_name")

        if form and new_name:
            form.name = new_name
            form.save()

        return redirect(url_for("site.form_list"))

    forms = FormModel.find_all(sort_keys=["-_modified_date"])
    return render_template("list.html", elements=forms, title="Forms")


@site_bp.route("/forms/delete", methods=["GET", "POST"])
@login_required
def form_delete():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormModel.find_by_id(_id)

        if form:
            form.delete()

    return redirect(url_for("site.form_list"))


@site_bp.route("/forms/<string:_id>", methods=["GET", "POST"])
@site_bp.route("/forms/new", methods=["POST"])
@login_required
def form_edit(_id=None):

    if not _id:
        fields = [EmbeddedFieldModel(displayed_text="Untitled Question")]
        form = FormModel(fields=fields)

        # TODO instead of saving just create an id for the from
        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    form = FormModel.find_by_id(_id)

    if request.method == "POST":

        for field in request.form:
            if hasattr(form, field):
                setattr(form, field, request.form[field])

        form.save()
        return '', 204
        # return redirect(url_for("site.form_edit", _id=form.id))

    if form:
        return render_template("form_edit.html", element=form, d_types=PY_DTYPES.keys())

    abort(404)


@site_bp.route("/forms/<string:form_id>/<string:field_id>", methods=["GET", "POST"])
@login_required
def form_field_edit(form_id, field_id):

    if request.method == "POST":
        form = FormModel.find_by_id(form_id)
        field = form.find_field_by_id(field_id) if form else None

        if field:
            field_prop = FieldProp(request.form, obj=form)
            field_prop.populate_obj(field)

            print("From EDIT")
            print(field_prop.required.data)
            print(field.required)

            form.save()
            return '', 204
            # return redirect(url_for("site.form_edit", _id=form.id))

    return abort(404)  # redirect(url_for("site.form_edit", _id=form_id))


@site_bp.route("/forms/<string:form_id>/<string:field_id>/new", methods=["GET", "POST"])
@site_bp.route("/forms/<string:form_id>/new", methods=["GET", "POST"])
@login_required
def form_field_add(form_id, field_id=None):
    form = FormModel.find_by_id(form_id)

    if form:
        new_field = EmbeddedFieldModel()

        if not field_id:
            form.fields.append(new_field)
            form.save()
            return redirect(url_for("site.form_edit", _id=form.id))

        i, field = form.find_field_by_id(field_id, index=True)

        field_prop = FieldProp(obj=field)
        field_prop.populate_obj(new_field)

        print("From ADD")
        print(field_prop.required.data)
        print(new_field.required)

        form.fields.insert(i+1, new_field)
        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    abort(404)


@site_bp.route("/forms/<string:form_id>/<string:field_id>/delete", methods=["GET", "POST"])
@login_required
def form_field_delete(form_id, field_id):
    form = FormModel.find_by_id(form_id)

    if form:
        i, field = form.find_field_by_id(field_id, index=True)

        if field:
            form.fields.pop(i)
            form.save()

            return redirect(url_for("site.form_edit", _id=form.id))

    return abort(404)

