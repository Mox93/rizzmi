from flask import redirect, url_for, render_template
from flask_admin import BaseView, expose
from flask_login import login_required, current_user
from developer import dev_bp


class DevProfileView(BaseView):
    @expose("/", methods=["Get"])
    def index(self):
        return self.render("dev/profile.html")

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("dev.login"))

