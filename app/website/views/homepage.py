from flask import render_template
from website import site_bp


@site_bp.route("/")
def homepage():
    return render_template("homepage.html")

