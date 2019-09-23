from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)

Bootstrap(app)

login_manager = LoginManager(app)

app.config["DEBUG"] = True
app.config["TESTING"] = True
# app.config["USE_SESSION_FOR_NEXT"] = True

print("app line 15")
import os

app.secret_key = os.urandom(24)


from common.db import DB_NAME, PORT, HOST

if "MONGOLAB_TEAL_URI" in os.environ:
    app.config['MONGODB_SETTINGS'] = {'db': DB_NAME,
                                      'host': os.environ["MONGOLAB_TEAL_URI"]}
else:
    app.config["MONGODB_DB"] = DB_NAME
    app.config["MONGODB_PORT"] = PORT
    app.config["MONGODB_HOST"] = HOST
print("app line 30")

from common.db import db

db.init_app(app)

try:
    # TODO should use environment values <DONE?>
    from x.recaptcha import RECAPCHA_SITE_KEY, RECAPCHA_SECRET_KEY

    app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPCHA_SITE_KEY", RECAPCHA_SITE_KEY)
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPCHA_SECRET_KEY", RECAPCHA_SECRET_KEY)
except:
    pass

print("app line 45")
from api import api_bp
from website import site_bp

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(site_bp)

print("app line 52")