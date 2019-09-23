from bson import ObjectId
from common.db import (db, ExtendedDocument, DTYPES, ACCEPT_MAX_LEN,
                       ACCEPT_MIN_LEN, ACCEPT_MIN_VAL, ACCEPT_MAX_VAL)


class FieldModel(ExtendedDocument):
    """
    This Model is the main building block used to create Forms.
    Its purpose is to store created fields for future reuse.
   """
    meta = {'collection': 'fields'}

    # TODO implement tags

    name = db.StringField(required=True, max_length=50, unique=True)
    displayed_text = db.StringField(max_length=250)
    data_type = db.StringField(required=True, choices=DTYPES.keys(), default="dynamic")
    required = db.BooleanField()
    unique = db.BooleanField()
    unique_with = db.DynamicField()
    primary_key = db.BooleanField()
    choices = db.DynamicField()
    help_text = db.StringField(max_length=250)

    # Data-type dependent attributes
    max_length = db.IntField()
    min_length = db.IntField()

    min_value = db.DynamicField()
    max_value = db.DynamicField()

    # Embedded Document Version
    _embedded = None

    def clean(self):
        """
        * Ensures that only data types which accept max/min_length/value have them and
        that min is always less than max.
        * Converts 'name' to lowercase.
        * Assignees a titled version of 'name' to displayed_text if nothing is assigned to it.
        """
        if self.data_type not in ACCEPT_MAX_LEN and self.max_length is not None:
            msg = f"The data_type '{self.data_type}' can't have a maximum length!"
            raise db.ValidationError(msg)

        if self.data_type not in ACCEPT_MIN_LEN and self.min_length is not None:
            msg = f"The data_type '{self.data_type}' can't have a minimum length!"
            raise db.ValidationError(msg)

        if self.data_type not in ACCEPT_MIN_VAL and self.min_value is not None:
            msg = f"The data_type '{self.data_type}' can't have a minimum value!"
            raise db.ValidationError(msg)

        if self.data_type not in ACCEPT_MAX_VAL and self.max_value is not None:
            msg = f"The data_type '{self.data_type}' can't have a maximum value!"
            raise db.ValidationError(msg)

        if self.max_length is not None and self.min_length is not None and self.max_length < self.min_length:
            msg = "max_length can't be less than min_length!"
            raise db.ValidationError(msg)

        if self.max_value is not None and self.min_value is not None and self.max_value < self.min_value:
            msg = "max_value can't be less than min_value!"
            raise db.ValidationError(msg)

        if isinstance(self.name, str):
            self.name = self.name.lower()
            if self.displayed_text is None:
                self.displayed_text = " ".join(self.name.split("_")).title()

    @classmethod
    def find_by_name(cls, name):
        return cls.objects(name=name.lower()).first()

    @classmethod
    def as_embedded(cls, *args, **kwargs):
        if not cls._embedded:

            cls._embedded = type("EmbeddedFieldModel", (db.EmbeddedDocument,),
                                 {"_id": db.ObjectIdField(default=ObjectId),
                                  "name": db.StringField(required=True, max_length=50),  # cls.name,
                                  "displayed_text": cls.displayed_text,
                                  "data_type": cls.data_type,
                                  "required": cls.required,
                                  "unique": cls.unique,
                                  "unique_with": cls.unique_with,
                                  "primary_key": cls.primary_key,
                                  "choices": cls.choices,
                                  "help_text": cls.help_text,
                                  "max_length": cls.max_length,
                                  "min_length": cls.min_length,
                                  "min_value": cls.min_value,
                                  "max_value": cls.max_value,
                                  "clean": cls.clean,
                                  "find_by_id": cls.find_by_id,
                                  "find_by_name": cls.find_by_name,
                                  "json": cls.json})
        if args or kwargs:
            return cls._embedded(*args, **kwargs)
        return cls._embedded


EmbeddedFieldModel = FieldModel.as_embedded()
