from common.db import db, ExtendedDocument
from flask_login import UserMixin
from bson import ObjectId


class UserModel(UserMixin, ExtendedDocument):
    meta = {'collection': 'users',
            'allow_inheritance': True}

    username = db.StringField(required=True, max_length=25, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, max_length=80)
    session_id = db.ObjectIdField(required=True, unique=True, default=ObjectId)

    def get_id(self):
        return str(self.session_id)

    def clean(self):

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



