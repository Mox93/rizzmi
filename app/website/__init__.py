from flask import Blueprint


site_bp = Blueprint("site", __name__, template_folder="templates", static_folder="static",
                    static_url_path="/website/static")

# from website.views import registration
from website.views import homepage, form, collection, field, entry

