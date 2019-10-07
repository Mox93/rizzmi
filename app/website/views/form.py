from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required
from website import site_bp
from models.form import FormModel
from models.field import EmbeddedFieldModel
from common.util import PY_DTYPES


@site_bp.route("/forms", methods=["GET", "POST"])
# @login_required
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


@site_bp.route("/forms/<string:_id>", methods=["GET", "POST"])
# @login_required
def form_edit(_id):

    if request.method == "POST":
        form = FormModel.find_by_id(_id)

        print(request.form)

        for field in request.form:
            if hasattr(form, field):
                print(f"field = {field}")
                setattr(form, field, request.form[field])

        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    if _id == "new":
        fields = [EmbeddedFieldModel(name="Untitled Question")]
        form = FormModel(fields=fields)

        # TODO instead of saving just create an id for the from
        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    form = FormModel.find_by_id(_id)

    if form:
        return render_template("form_edit.html", element=form, d_types=PY_DTYPES.keys())

    abort(404)


@site_bp.route("/forms/delete", methods=["GET", "POST"])
# @login_required
def form_delete():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormModel.find_by_id(_id)

        if form:
            form.delete()

    return redirect(url_for("site.form_list"))


@site_bp.route("/forms/<string:form_id>/<string:field_id>", methods=["GET", "POST"])
# @login_required
def form_field_edit(form_id, field_id):

    if request.method == "POST":
        form = FormModel.find_by_id(form_id)
        field = form.find_field_by_id(field_id) if form else None

        if field:
            for prop in request.form:
                if hasattr(field, prop):
                    setattr(field, prop, request.form[prop])

            form.save()
            return redirect(url_for("site.form_edit", _id=form.id))

    return redirect(url_for("site.form_edit", _id=form_id))

