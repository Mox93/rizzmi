from flask import render_template
from website import site_bp


@site_bp.route("/collections")
def collection():
    return render_template("list.html", title="Collections")

