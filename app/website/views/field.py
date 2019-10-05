from flask import render_template
from website import site_bp


@site_bp.route("/fields")
def field():
    return render_template("list.html", title="Fields")

