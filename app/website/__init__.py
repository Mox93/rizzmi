from flask import Blueprint


site_bp = Blueprint("site", __name__, template_folder="templates")

from website.views import homepage
from website.views import developer
# from website.views import registration

