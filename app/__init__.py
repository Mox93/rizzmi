from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mongoengine import MongoEngineSessionInterface
from flask_wtf.csrf import CSRFProtect
from models.user import DeveloperModel


app = Flask(__name__)

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "dev.login"

# csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id):
    user = DeveloperModel.find_one_by("session_id", user_id)
    return user


app.config["DEBUG"] = True
app.config["TESTING"] = True


import secrets

app.config["SECRET_KEY"] = secrets.token_urlsafe(24)
# app.config["SERVER_NAME"] = "127.0.0.1:5000"
# app.config["APPLICATION_ROOT"] = "/"


from common.db import db, DB_NAME, PORT, HOST

app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = PORT
app.config["MONGODB_HOST"] = HOST

db.init_app(app)

app.session_interface = MongoEngineSessionInterface(db)

# TODO should use environment values
from x.recaptcha import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY

app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_SITE_KEY
app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_SECRET_KEY


# from api import api_bp
from website import site_bp
from developer import dev_bp

# app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)
app.register_blueprint(dev_bp, url_prefix="/dev")


from flask_graphql import GraphQLView
from gql_api import schema

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))