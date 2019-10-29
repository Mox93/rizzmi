from bson import ObjectId
from common.util import INPUT_TYPES
from common.db import (db, ExtendedDocument, ExtendedEmbeddedDocument,
                       DTYPES, ACCEPT_MAX_LEN, ACCEPT_MIN_LEN, ACCEPT_MIN_VAL, ACCEPT_MAX_VAL)


class FieldModel(ExtendedDocument):
    """
    The main building block used in creating Forms.
    Its purpose is to store created fields for future reuse.
    The main fields are:
        - name:
        - question:     what will appear in forms
        - data_type:    the value type that will be stored in the database
        - input_type:   the method of inputting the value in forms
        - required:     a boolean
        - unique:       a boolean
        - unique_with:  a list of fields that when combined must be unique
        - primary_key:  will make the field required and unique  ## shouldn't be used for now
        - choices:      a list of values that the field-value must be one of
        - description:  some explanation on why or how to fill-in the field
        ===============
        - max_length:   only used if the field data type allows it
        - min_length:   only used if the field data type allows it
        - max_value:    only used if the field data type allows it
        - min_value:    only used if the field data type allows it
   """

    meta = {'collection': 'fields'}

    # TODO implement tags

    name = db.StringField(required=True, max_length=50, default="untitled_field")
    question = db.StringField(max_length=500)
    data_type = db.StringField(required=True, choices=DTYPES.keys(), default="dynamic")
    input_type = db.StringField(choices=INPUT_TYPES, default=INPUT_TYPES[0])
    required = db.BooleanField()
    unique = db.BooleanField()
    unique_with = db.DynamicField()
    primary_key = db.BooleanField()
    choices = db.DynamicField()
    description = db.StringField()

    # Data-type dependent attributes
    max_length = db.IntField()
    min_length = db.IntField()

    min_value = db.DynamicField()
    max_value = db.DynamicField()

    # Embedded Document Version
    _embedded = None

    def clean(self):
        """
        Ensures that only data types which accept max/min_length/value have them and
        that min is always less than max.
        Converts 'name' to lowercase with '_' instead of spaces and trims it to its maximum length.
        Trims 'question' to its maximum length.
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
            n = FieldModel.name.max_length
            self.name = "_".join(self.name.lower().split(" "))[:n] or FieldModel.name.default

        if isinstance(self.question, str):
            n = FieldModel.question.max_length
            self.question = self.question[:n]

    def __repr__(self):
        return f"<Field name: {self.name} question: {self.question}>"

    @classmethod
    def as_embedded(cls, *args, **kwargs):
        """
        In order to use fields inside of forms we need to convert them into embedded documents.
        This is done to separate them from the original field so they don't mutate each other.
        ** some attributes are added to store information about the collection and form they belong to.
        ** passing nothing to this function will return the EmbeddedFieldModel class,
        ** while passing args and/or kwargs will return an EmbeddedFieldModel instance.
        :param args:
        :param kwargs:
        :return EmbeddedFieldModel:
        """
        if not cls._embedded:

            cls._embedded = type("EmbeddedFieldModel", (ExtendedEmbeddedDocument,),
                                 {"index": db.IntField(required=True, default=-1),
                                  "question": cls.question,
                                  "data_type": cls.data_type,
                                  "input_type": cls.input_type,
                                  "required": cls.required,
                                  "unique": cls.unique,
                                  "unique_with": cls.unique_with,
                                  "primary_key": cls.primary_key,
                                  "choices": cls.choices,
                                  "description": cls.description,
                                  "max_length": cls.max_length,
                                  "min_length": cls.min_length,
                                  "min_value": cls.min_value,
                                  "max_value": cls.max_value,
                                  "collection": db.ObjectIdField(),
                                  "__repr__": lambda self: f"<Field question: {self.question}>"})

        if args or kwargs:
            return cls._embedded(*args, **kwargs)

        return cls._embedded


EmbeddedFieldModel = FieldModel.as_embedded()

