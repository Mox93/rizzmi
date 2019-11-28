from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_mongoengine import MongoEngineSessionInterface
from flask_jwt_extended import JWTManager
from models.user import DeveloperModel


app = Flask(__name__)

CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = "dev.login"


@login_manager.user_loader
def load_user(user_id):
    user = DeveloperModel.find_one_by("session_id", user_id)
    return user


app.config["DEBUG"] = True
app.config["TESTING"] = True


import os
import secrets

app.config["SECRET_KEY"] = secrets.token_urlsafe(24)
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(24)

jwt = JWTManager(app)


app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]

app.config["MONGODB_DB"] = os.environ["DB_NAME"]
app.config["MONGODB_HOST"] = os.environ["MONGOLAB_MAROON_URI"]
app.config['MONGODB_CONNECT'] = False

from common.db import db

db.init_app(app)
app.session_interface = MongoEngineSessionInterface(db)

# from api import api_bp
from website import site_bp
from developer import dev_bp

# app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)
app.register_blueprint(dev_bp, url_prefix="/dev")


from flask_graphql import GraphQLView
from gql_api import schema
from gql_api.auth import add_claims_to_access_token, user_identity_lookup

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

