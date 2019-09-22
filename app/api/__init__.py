from flask import Blueprint
from flask_restful import Api
from api.resources.field import Field, FieldList
from api.resources.form import Form, FormList
from api.resources.entry import Entry, EntryList
from common.util import URL_MAP


api_bp = Blueprint('api', __name__)

api = Api(api_bp)

URL_MAP.extend(({"resource": Field, "urls": ("/fields/<string:_id>",)},
                {"resource": FieldList, "urls": ("/fields",)},
                {"resource": Form, "urls": ("/forms/<string:_id>",)},
                {"resource": FormList, "urls": ("/forms",)},

                # TODO maybe it's better to use "/entries/<string:entry_id>" instead
                {"resource": Entry, "urls": ("/forms/<string:form_id>/entries/<string:entry_id>",)},
                {"resource": EntryList, "urls": ("/forms/<string:form_id>/entries",)}))

for url_map in URL_MAP:
    api.add_resource(url_map["resource"], *url_map["urls"])


@api_bp.route("/")
def homepage():
    return "<h1> <font color=\"green\"> Welcome to the Rizzmi API! </font> </h1>" \
           "<p>This website is still under construction.</p>"
