from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class ExtendedDocument(db.Document):
    meta = {"abstract": True}

    _creation_date = db.DateTimeField()
    _modified_date = db.DateTimeField(default=datetime.now)

    @property
    def creation_date(self, raw=False):
        if raw:
            return self._creation_date

        if self._creation_date.day == datetime.now().day:
            return self._creation_date.strftime("%I:%M %p")

        return self._creation_date.strftime("%b %d, %Y")

    @creation_date.setter
    def creation_date(self, value):
        self._creation_date = value

    @property
    def modified_date(self, raw=False):
        if raw:
            return self._modified_date

        if self._modified_date.day == datetime.now().day:
            return self._modified_date.strftime("%I:%M %p")

        return self._modified_date.strftime("%b %d, %Y")

    @modified_date.setter
    def modified_date(self, value):
        self._modified_date = value

    def save(self, *args, **kwargs):
        if not self._creation_date:
            self._creation_date = datetime.now()
        self._modified_date = datetime.now()
        return super(ExtendedDocument, self).save(*args, **kwargs)

    def json(self, exclude=tuple()):
        result = self.to_mongo()

        for key in exclude:
            if key in result:
                del result[key]

        if result.get("_id", None):
            result["_id"] = str(result["_id"])

        if result.get("id", None):
            result["_id"] = str(result["id"])
            del result["id"]

        for key in result:
            try:
                if isinstance(self[key], db.EmbeddedDocument):
                    result[key]["_id"] = str(result[key].get("_id", "")) or None
                elif isinstance(self[key], list):
                    for item in result[key]:
                        item["_id"] = str(item.get("_id", "")) or None
            except KeyError as e:
                # pass
                print(self, e)

        return result

    @classmethod
    def find_by_id(cls, _id):
        try:
            return cls.objects(id=_id).first()
        except:
            return

    @classmethod
    def find_one_by(cls, name, value):
        try:
            return cls.objects(**{name: value}).first()
        except:
            return

    @classmethod
    def find_many_by(cls, name, value, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return cls.objects(**{name: value}).order_by(*sort_keys)
            return cls.objects(**{name: value})
        except:
            return []

    @classmethod
    def find_all(cls, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return cls.objects().order_by(*sort_keys)
            return cls.objects()
        except:
            return []


class ExtendedEmbeddedDocument(db.EmbeddedDocument):
    meta = {"abstract": True}

    def json(self, exclude=tuple()):
        result = self.to_mongo()

        for key in exclude:
            if key in result:
                del result[key]

        if result.get("_id", None):
            result["_id"] = str(result["_id"])

        if result.get("id", None):
            result["_id"] = str(result["id"])
            del result["id"]

        for key in result:
            try:
                if isinstance(self[key], db.EmbeddedDocument):
                    result[key]["_id"] = str(result[key].get("_id", "")) or None
                elif isinstance(self[key], list):
                    for item in result[key]:
                        item["_id"] = str(item.get("_id", "")) or None
            except KeyError as e:
                # pass
                print(self, e)

        return result

    def delete_by_id(self, value):
        self.objects.update(__raw__={"$pull": {"_id": value}})

    @classmethod
    def find_by_id(cls, _id):
        try:
            return cls.objects(id=_id).first()
        except:
            return

    @classmethod
    def find_by(cls, field_name, value):
        try:
            return cls.objects(**{field_name: value}).first()
        except:
            return

    @classmethod
    def find_all(cls):
        try:
            return cls.objects()
        except:
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


if __name__ == "__main__":
    print("Hello Mongo!")

