from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from developer import dev_bp
from flask_admin import AdminIndexView


class DevHomeView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("dev.login"))


@dev_bp.route("/", methods=["Get"])
@login_required
def homepage():
    pass
    # TODO this gets found by url_for in the login but the url leads to somewhere else, needs to be fixed it
    # return render_template("dev/homepage.html")

