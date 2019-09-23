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

app.config["SECRET_KEY"] = os.urandom(24)

app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]

app.config["MONGODB_DB"] = os.environ["DB_NAME"]
app.config["MONGODB_HOST"] = os.environ["MONGOLAB_MAROON_URI"]
app.config['MONGODB_CONNECT'] = False


from common.db import db

db.init_app(app)


from api import api_bp
from website import site_bp

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)

