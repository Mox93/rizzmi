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


from common.db import DB_NAME, PORT, HOST

if "MONGODB_URI" in os.environ:
    app.config['MONGODB_SETTINGS'] = {'db': DB_NAME,
                                      'host': os.environ["MONGOLAB_TEAL"]}
else:
    app.config["MONGODB_DB"] = DB_NAME
    app.config["MONGODB_PORT"] = PORT
    app.config["MONGODB_HOST"] = HOST


from common.db import db

db.init_app(app)

try:
    # TODO should use environment values <DONE?>
    from x.recaptcha import RECAPCHA_SITE_KEY, RECAPCHA_SECRET_KEY

    app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPCHA_SITE_KEY", RECAPCHA_SITE_KEY)
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPCHA_SECRET_KEY", RECAPCHA_SECRET_KEY)
except:
    pass


from api import api_bp
from website import site_bp

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)

