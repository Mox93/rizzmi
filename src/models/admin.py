import uuid
from common.db import db


class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.String, primary_key=True)
    phone_No = db.Column(db.String(25))
    password = db.Column(db.String(50))

    def __init__(self, phone_no, password, _id=None):
        self.phone_No = phone_no
        self.password = password
        self.id = _id or uuid.uuid4().hex

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_phone_no(cls, phone_no):
        return cls.query.filter_by(username=phone_no).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
