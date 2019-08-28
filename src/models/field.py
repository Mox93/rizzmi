from common.db import db, DTYPES, ACCEPT_MAX_LEN, ACCEPT_MIN_LEN, ACCEPT_MIN_VAL, ACCEPT_MAX_VAL


class FieldModel(db.Document):
    """
    This Model is the main building block used to create Forms.
    Its purpose is to store created fields for future reuse.

   """
    meta = {'collection': 'fields'}

    # TODO implement tags

    db_field = db.StringField(required=True, max_length=50, unique=True)
    displayed_text = db.StringField(max_length=250)
    data_type = db.StringField(required=True, choices=DTYPES.keys(), default="dynamic")
    required = db.BooleanField()
    unique = db.BooleanField()
    unique_with = db.DynamicField()
    primary_key = db.BooleanField()
    choices = db.DynamicField()
    help_text = db.StringField(max_length=250)

    # Data type dependent attributes
    max_length = db.IntField()
    min_length = db.IntField()

    min_value = db.DynamicField()
    max_value = db.DynamicField()

    def __init__(self, *args, **kwargs):
        super(FieldModel, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Ensures that only data types which accept max/min_length/value have them and
        that min is always less than max
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

        self.db_field = self.db_field.lower()

        if self.displayed_text is None:
            self.displayed_text = " ".join(self.db_field.split("_")).title()

    @classmethod
    def find_by_name(cls, name):
        return cls.objects(db_field=name.lower()).first()

    def json(self):
        result = dict(self.to_mongo())
        del result["_id"]
        return result



