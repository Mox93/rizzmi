from common.db import db, ExtendedDocument
from flask_login import UserMixin
from bson import ObjectId


class DeveloperModel(UserMixin, ExtendedDocument):
    meta = {'collection': 'developers'}

    username = db.StringField(required=True, max_length=25, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, max_length=80)
    session_id = db.ObjectIdField(unique=True, defult=ObjectId)

    def get_id(self):
        return str(self.session_id)

    def clean(self):
        if not self.session_id:
            self.session_id = ObjectId()

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

