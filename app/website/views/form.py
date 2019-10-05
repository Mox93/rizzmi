from flask import render_template, request, redirect, url_for, abort
from website import site_bp
from models.form import FormModel


# @site_bp.route("/forms/new", methods=["GET", "POST"])
# def form_create():
#     return render_template("edit.html", title="Forms")


@site_bp.route("/forms/<string:_id>", methods=["GET", "POST"])
def form_edit(_id):

    if request.method == "POST":
        form = FormModel.find_by_id(_id)

        for field in request.form:
            setattr(form, field, request.form[field])

        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    if _id == "new":
        form = FormModel()

        # TODO instead of saving just create an id for the from
        form.save()
        return redirect(url_for("site.form_edit", _id=form.id))

    form = FormModel.find_by_id(_id)

    if form:
        return render_template("edit.html", element=form)

    abort(404)


@site_bp.route("/forms", methods=["GET", "POST"])
def form_list():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormModel.find_by_id(_id)
        new_name = request.form.get("new_name")

        if form and new_name:
            form.name = new_name
            form.save()

    forms = FormModel.find_all()
    return render_template("list.html", elements=forms, title="Forms")


@site_bp.route("/forms/delete", methods=["GET", "POST"])
def form_delete():

    if request.method == "POST":
        _id = request.form.get("_id")
        form = FormModel.find_by_id(_id)

        if form:
            form.delete()

    return redirect(url_for("site.form_list"))

