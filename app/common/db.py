from bson import ObjectId
from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class ExtendedDocument(db.Document):
    """
    The base for all documents in the project
    Contains the following additional features:
        - _id:              an ObjectId
        - creation_date:    the time the document was created  ## UTC
        - modified_date:    the last time the document was modified  ## UTC
        - json:             returns a dict-like representation of the document
        - find_by_id:       a basic search by id
        - find_one_by:      returns the firs document which has the given field-name with the required value
        - find_many_by:     returns all documents which has the given field-name with the required value
        - find_all:         returns all documents
    """

    meta = {"abstract": True}

    _id = db.ObjectIdField(required=True, default=ObjectId)
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.utcnow()
        self.modified_date = datetime.utcnow()
        return super(ExtendedDocument, self).save(*args, **kwargs)

    def json(self, exclude=tuple()):
        result = self.to_mongo()

        pass_on = []

        for key in exclude:
            if key in result:
                del result[key]
            else:
                pass_on.append(key)

        for key in result:
            if isinstance(result[key], ObjectId):
                result[key] = str(result[key])
            elif isinstance(self[key], db.EmbeddedDocument):
                result[key] = self[key].json(exclude=pass_on)
            elif isinstance(self[key], list):
                for i, item in enumerate(self[key]):
                    if isinstance(result[key][i], ObjectId):
                        result[key][i] = str(result[key][i])
                    elif isinstance(item, db.EmbeddedDocument):
                        result[key][i] = item.json(exclude=pass_on)

        return result

    @classmethod
    def find_by_id(cls, _id):
        try:
            return cls.objects(_id=_id).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_one_by(cls, field_name, value):
        try:
            return cls.objects(**{field_name: value}).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_many_by(cls, field_name, value, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects(**{field_name: value}).order_by(*sort_keys))
            return list(cls.objects(**{field_name: value}))
        except Exception as e:
            print(str(e))
            return []

    @classmethod
    def find_all(cls, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects().order_by(*sort_keys))
            return list(cls.objects())
        except Exception as e:
            print(str(e))
            return []


class ExtendedDynamicDocument(db.DynamicDocument, ExtendedDocument):
    """
    The base for all dynamic documents in the project
    Contains the following additional features:
        - creation_date:    the time the document was created  ## UTC
        - modified_date:    the last time the document was modified  ## UTC
        - json:             returns a dict-like representation of the document
        - find_by_id:       a basic search by id
        - find_one_by:      returns the firs document which has the given field-name with the required value
        - find_many_by:     returns all documents which has the given field-name with the required value
        - find_all:         returns all documents
    """

    pass


class ExtendedEmbeddedDocument(db.EmbeddedDocument):
    """
    The base for all embedded documents in the project
    Contains the following additional features:
        - _id:              an ObjectId
        - json:             returns a dict-like representation of the document
        - find_by_id:       a basic search by id
        - find_one_by:      returns the firs document which has the given field-name with the required value
        - find_many_by:     returns all documents which has the given field-name with the required value
        - find_all:         returns all documents
    """

    meta = {"abstract": True}

    _id = db.ObjectIdField(required=True, default=ObjectId)

    def json(self, exclude=tuple()):
        result = self.to_mongo()

        pass_on = []

        for key in exclude:
            if key in result:
                del result[key]
            else:
                pass_on.append(key)

        for key in result:
            if isinstance(result[key], ObjectId):
                result[key] = str(result[key])
            elif isinstance(self[key], db.EmbeddedDocument):
                result[key] = self[key].json(exclude=pass_on)
            elif isinstance(self[key], list):
                for i, item in enumerate(self[key]):
                    if isinstance(result[key][i], ObjectId):
                        result[key][i] = str(result[key][i])
                    elif isinstance(item, db.EmbeddedDocument):
                        result[key][i] = item.json(exclude=pass_on)

        return result

    @classmethod
    def find_by_id(cls, _id):
        try:
            return cls.objects(_id=_id).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_one_by(cls, field_name, value):
        try:
            return cls.objects(**{field_name: value}).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_many_by(cls, field_name, value, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects(**{field_name: value}).order_by(*sort_keys))
            return list(cls.objects(**{field_name: value}))
        except Exception as e:
            print(str(e))
            return []

    @classmethod
    def find_all(cls, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects().order_by(*sort_keys))
            return list(cls.objects())
        except Exception as e:
            print(str(e))
            return []


# DB Configuration Values

DB_NAME = "rizzmi"
PORT = 27017
HOST = "localhost"


# Metadata Defaults

DTYPES = {"bool": db.BooleanField,
          "datetime": db.DateTimeField,
          "dict": db.DictField,
          "dynamic": db.DynamicField,
          "email": db.EmailField,
          "float": db.FloatField,
          "int": db.IntField,
          "list": db.ListField,
          "str": db.StringField}

ACCEPT_MAX_LEN = ["str", "list", "email"]
ACCEPT_MIN_LEN = ["str", "email"]
ACCEPT_MIN_VAL = ["int", "float"]
ACCEPT_MAX_VAL = ["int", "float"]

