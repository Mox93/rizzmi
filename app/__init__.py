from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from models.developer import DeveloperModel


app = Flask(__name__)

Bootstrap(app)

login_manager = LoginManager(app)

login_manager.login_view = "dev.login"


@login_manager.user_loader
def load_user(user_id):
    user = DeveloperModel.find_one_by("session_id", user_id)
    return user


app.config["DEBUG"] = True
app.config["TESTING"] = True


import os

app.config["SECRET_KEY"] = os.urandom(24)
# app.config["SERVER_NAME"] = "127.0.0.1:5000"
# app.config["APPLICATION_ROOT"] = "/"


app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]

app.config["MONGODB_DB"] = os.environ["DB_NAME"]
app.config["MONGODB_HOST"] = os.environ["MONGOLAB_MAROON_URI"]
app.config['MONGODB_CONNECT'] = False


from common.db import db

db.init_app(app)


from api import api_bp
from website import site_bp
from developer import dev_bp

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)
app.register_blueprint(dev_bp, url_prefix="/dev")

