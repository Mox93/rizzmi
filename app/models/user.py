from common.db import db, ExtendedDocument
from flask_login import UserMixin
from bson import ObjectId


class UserModel(UserMixin, ExtendedDocument):
    """
    The basic common information for all users of the webapp.
    Inherits from UserMixin so it could be used with Flask-Login.
    To add user-roles specific data this document should be inherited.
    ** username and email are case-insensitive
    """

    meta = {'collection': 'users',
            'allow_inheritance': True}

    username = db.StringField(required=True, max_length=50, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, max_length=80)
    session_id = db.ObjectIdField(required=True, unique=True, default=ObjectId)

    def get_id(self):
        return str(self.session_id)

    def clean(self):
        """
        Insures that username and email are lowercase.
        """

        if isinstance(self.username, str):
            self.username = self.username.lower()

        if isinstance(self.email, str):
            self.email = self.email.lower()

    @classmethod
    def find_by_username(cls, username):
        return cls.objects(username=username.lower()).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email.lower()).first()


class DeveloperModel(UserModel):
    pass



