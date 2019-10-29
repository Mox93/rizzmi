from flask import render_template, request, redirect, url_for, abort, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired
from website import site_bp
from models.form import FormTemplateModel, FormMapModel
from models.field import EmbeddedFieldModel


class FieldProp(FlaskForm):
    question = StringField("Question")
    input_type = SelectField("Input Type", choices=EmbeddedFieldModel.input_type.choices)
    description = TextAreaField("Description")
    required = BooleanField("Required")


@site_bp.route("/forms", methods=["GET", "POST"])
# @login_required
def form_list():

    if request.method == "POST":
        _id = request.form.get("_id")
        new_name = request.form.get("new_name")
        form = FormTemplateModel.find_by_id(_id)

        if form and new_name:
            form.name = new_name
            form.save()

        return redirect(url_for("site.form_list"))  # We do this to change the request method from POST to GET

    forms = FormTemplateModel.find_all(sort_keys=["-_modified_date"])
    return render_template("form_list.html", elements=forms, title="Forms")


@site_bp.route("/forms/delete", methods=["GET", "POST"])
# @login_required
def form_delete():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormTemplateModel.find_by_id(_id)

        if form:
            form.delete()

    return redirect(url_for("site.form_list"))


@site_bp.route("/forms/new", methods=["GET", "POST"])
# @login_required
def form_new():
    fields = [EmbeddedFieldModel(question="Untitled Question")]
    form = FormTemplateModel(fields=fields)
    form.save()

    entry = FormMapModel(form=form)
    entry.save()

    form.links = [entry.id]
    form.save()

    return redirect(url_for("site.form_edit", _id=form.id))


@site_bp.route("/forms/<string:_id>", methods=["GET", "POST"])
# @login_required
def form_edit(_id):
    form = FormTemplateModel.find_by_id(_id)

    if request.method == "POST" and form:
        for field in request.form:
            if hasattr(form, field):
                setattr(form, field, request.form[field])

        form.save()
        return '', 204

    if form:
        return render_template("form_edit.html", element=form,
                               input_types=EmbeddedFieldModel.input_type.choices)

    abort(404)


@site_bp.route("/forms/<string:form_id>/<string:field_id>", methods=["GET", "POST"])
# @login_required
def form_field_edit(form_id, field_id):

    if request.method == "POST":
        form = FormTemplateModel.find_by_id(form_id)
        field = form.find_field_by_id(field_id) if form else None

        if field:
            field_prop = FieldProp(request.form, obj=form)
            field_prop.populate_obj(field)

            form.save()
            return '', 204

    abort(404)


@site_bp.route("/forms/<string:form_id>/new", methods=["GET", "POST"])
# @login_required
def form_field_add(form_id):
    form = FormTemplateModel.find_by_id(form_id)

    if form:
        new_field = EmbeddedFieldModel()

        form.fields.append(new_field)
        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    abort(404)


@site_bp.route("/forms/<string:form_id>/<string:field_id>/new", methods=["GET", "POST"])
# @login_require
def form_field_duplicate(form_id, field_id):
    form = FormTemplateModel.find_by_id(form_id)

    if form:
        i, field = form.find_field_by_id(field_id, index=True)

        if field:
            new_field = EmbeddedFieldModel()

            field_prop = FieldProp(obj=field)
            field_prop.populate_obj(new_field)

            form.fields.insert(i + 1, new_field)
            form.save()
            return redirect(url_for("site.form_edit", _id=form.id))

    abort(404)


@site_bp.route("/forms/<string:form_id>/<string:field_id>/delete", methods=["GET", "POST"])
# @login_required
def form_field_delete(form_id, field_id):
    form = FormTemplateModel.find_by_id(form_id)

    if form:
        i, field = form.find_field_by_id(field_id, index=True)

        if field:
            form.fields.pop(i)
            form.save()
            return redirect(url_for("site.form_edit", _id=form.id))

    abort(404)


@site_bp.route("/forms/<string:_id>/entry", methods=["GET", "POST"])
def form_entry(_id):
    class F(FlaskForm):
        pass

    entry = FormMapModel.find_by_id(_id)

    for field in entry.form.fields:
        validators = []
        if field.required:
            validators.append(InputRequired())

        setattr(F, f"field_{field._id}", StringField(field.question or "", validators=validators))

    form = F()

    if request.method == "POST":
        return redirect(url_for("site.form_reply", _id=_id))

    return render_template("form_entry.html", form=form, element=entry.form)


@site_bp.route("/forms/<string:_id>/reply", methods=["GET", "POST"])
def form_reply(_id):
    return "<h2> Thank you form filling in the form </h2>"

# ============================================================================


@site_bp.route("/forms-json/<string:_id>", methods=["GET", "POST"])
# @login_required
def form_edit_json(_id):
    form = FormTemplateModel.find_by_id(_id)

    if form:
        if request.method == "POST":
            for field in request.get_json():
                if hasattr(form, field):
                    setattr(form, field, request.get_json()[field])

            form.save()

        return jsonify(form.json()), 200

    abort(404)


