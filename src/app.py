import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from common.security import authenticate, identity
from resources.trainer import Trainer, TrainerRegister
from resources.employee import Employee, EmployeeRegister
from resources.customer import Customer, CustomerRegister
# from resources.course import Course, CourseRegister

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../data/data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24)
api = Api(app)

jwt = JWT(app, authenticate, identity)

url_map = {"/trainer/<string:_id>": Trainer,
           "/trainer/register": TrainerRegister,
           "/employee/<string:_id>": Employee,
           "/employee/register": EmployeeRegister,
           "/customer/<string:_id>": Customer,
           "/customer/register": CustomerRegister,}
           # "/course/<string:_id>": Course,
           # "/course/register": CourseRegister}

for url, resource in url_map.items():
    api.add_resource(resource, url)

if __name__ == '__main__':
    from common.db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
