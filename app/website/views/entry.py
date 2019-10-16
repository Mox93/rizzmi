from flask import redirect, url_for, request, render_template, abort
from models.entry import EntryModel
from website import site_bp


@site_bp.route("/forms/<string:_id>/entry", methods=["GET", "POST"])
def form_entry(_id):
    entry = EntryModel.find_by_id(_id)

    if entry:
        return render_template("form_entry.html", form=entry.form)

    abort(404)



