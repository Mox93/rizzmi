from flask_mongoengine import MongoEngine

db = MongoEngine()


# DB Configuration Values

DB_NAME = "rizzmi"
PORT = 27017
HOST = "localhost"


# Metadata Defaults

DTYPES = {"bool": db.BooleanField,
          "datetime": db.DateTimeField,
          "dict": db.DictField,
          "dynamic": db.DynamicField,
          "float": db.FloatField,
          "int": db.IntField,
          "list": db.ListField,
          "str": db.StringField}

ACCEPT_MAX_LEN = ["str", "list"]
ACCEPT_MIN_LEN = ["str"]
ACCEPT_MIN_VAL = ["int", "float"]
ACCEPT_MAX_VAL = ["int", "float"]


# Helper Functions



