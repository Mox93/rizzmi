from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)

Bootstrap(app)

login_manager = LoginManager(app)

app.config["DEBUG"] = True
app.config["TESTING"] = True
# app.config["USE_SESSION_FOR_NEXT"] = True


import os

app.secret_key = os.urandom(24)


from common.db import db, DB_NAME, PORT, HOST

app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = PORT
app.config["MONGODB_HOST"] = HOST

db.init_app(app)


# TODO should use environment values
from x.recaptcha import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY

app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_SITE_KEY
app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_SECRET_KEY


# from api import api_bp
from website import site_bp

# app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)

