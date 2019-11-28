from common.db import db, ExtendedDocument
from flask_login import UserMixin
from bson import ObjectId


class UserModel(UserMixin, ExtendedDocument):
    """
    The basic common information for all users of the webapp.
    Inherits from UserMixin so it could be used with Flask-Login.
    To add user-roles specific data this document should be inherited.
    ** first/last name and email are case-insensitive
    """

    meta = {'collection': 'users',
            'allow_inheritance': True}

    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True, unique=True, max_length=150)
    phone_number = db.StringField(required=True, min_length=7, max_length=15, unique=True)
    password = db.StringField(required=True, min_length=80, max_length=80)
    session_id = db.ObjectIdField(required=True, unique=True, default=ObjectId)

    def get_id(self):
        return str(self.session_id)

    def clean(self):
        """
        Insures that first/last name and email are lowercase.
        """

        if isinstance(self.first_name, str):
            self.first_name = self.first_name.lower()

        if isinstance(self.last_name, str):
            self.last_name = self.last_name.lower()

        if isinstance(self.email, str):
            self.email = self.email.lower()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.objects(phone_number=phone_number.lower()).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email.lower()).first()


class DeveloperModel(UserModel):
    pass



