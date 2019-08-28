import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# from common.security import authenticate, identity
from common.db import DB_NAME, PORT, HOST
from resources.field import Field
# from resources.trainer import Trainer, TrainerRegister
# from resources.employee import Employee, EmployeeRegister
# from resources.customer import Customer, CustomerRegister
# from resources.course import Course, CourseRegister

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = PORT
app.config["MONGODB_HOST"] = HOST

app.secret_key = os.urandom(24)
api = Api(app)

# jwt = JWT(app, authenticate, identity)

# url_map = {"/trainer/<string:_id>": Trainer,
#            "/trainer/register": TrainerRegister,
#            "/employee/<string:_id>": Employee,
#            "/employee/register": EmployeeRegister,
#            "/customer/<string:_id>": Customer,
#            "/customer/register": CustomerRegister,}
           # "/course/<string:_id>": Course,
           # "/course/register": CourseRegister}

URL_MAP = {("/field/<string:name>",): Field}

for urls, resource in URL_MAP.items():
    api.add_resource(resource, *urls)


if __name__ == '__main__':
    from common.db import db
    db.init_app(app)

    app.run(port=5000)
