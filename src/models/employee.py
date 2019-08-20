import uuid
from common.db import db
from datetime import datetime, date


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone_No_1 = db.Column(db.String(25))
    phone_No_2 = db.Column(db.String(25))
    phone_No_3 = db.Column(db.String(25))
    registration_date = db.Column(db.DateTime)

    def __init__(self, first_name, middle_name, last_name, email, phone_No_1,
                 phone_No_2="", phone_No_3="", registration_date=None, _id=None):
        self.first_name = first_name.lower()
        self.middle_name = middle_name.lower()
        self.last_name = last_name.lower()
        self.email = email
        self.phone_No_1, self.phone_No_2, self.phone_No_3 = phone_No_1, phone_No_2, phone_No_3
        self.registration_date = registration_date or datetime.utcnow()
        self.id = _id or uuid.uuid4().hex

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        rd = self.registration_date
        return {"id": self.id,
                "first_name": self.first_name,
                "middle_name": self.middle_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_No_1": self.phone_No_1,
                "phone_No_2": self.phone_No_2,
                "phone_No_3": self.phone_No_3,
                "registration_date": [rd.year, rd.month, rd.day, rd.hour, rd.minute, rd.second]}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
