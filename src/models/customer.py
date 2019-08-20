import uuid
from common.db import db
from datetime import datetime, date


class CustomerModel(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone_No_1 = db.Column(db.String(25))
    phone_No_2 = db.Column(db.String(25))
    phone_No_3 = db.Column(db.String(25))
    address = db.Column(db.String(250))
    date_of_birth = db.Column(db.Date)
    social_status = db.Column(db.String(25))
    national_id = db.Column(db.String(25))
    has_smartphone = db.Column(db.Boolean)
    has_computer = db.Column(db.Boolean)
    has_internet = db.Column(db.Boolean)
    registration_date = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, gender, date_of_birth, address, email, social_status,
                 national_id, phone_No_1, has_smartphone=False, has_computer=False, has_internet=False,
                 phone_No_2="", phone_No_3="", middle_name="", registration_date=None, _id=None):

        self.first_name = first_name.lower()
        self.middle_name = middle_name.lower()
        self.last_name = last_name.lower()
        self.gender = gender
        self.email = email
        self.phone_No_1, self.phone_No_2, self.phone_No_3 = phone_No_1, phone_No_2, phone_No_3
        self.address = address
        self.date_of_birth = date(*date_of_birth)
        self.social_status = social_status
        self.national_id = national_id
        self.has_smartphone = has_smartphone
        self.has_computer = has_computer
        self.has_internet = has_internet
        self.registration_date = registration_date or datetime.utcnow()
        self.id = _id or uuid.uuid4().hex
        # print(self.__dict__)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        d = self.date_of_birth
        rd = self.registration_date
        return {"id": self.id,
                "first_name": self.first_name,
                "middle_name": self.middle_name,
                "last_name": self.last_name,
                "gender": self.gender,
                "social_status": self.social_status,
                "national_id": self.national_id,
                "email": self.email,
                "phone_No_1": self.phone_No_1,
                "phone_No_2": self.phone_No_2,
                "phone_No_3": self.phone_No_3,
                "address": self.address,
                "date_of_birth": [d.year, d.month, d.day],
                "has_smartphone": self.has_smartphone,
                "has_computer": self.has_computer,
                "has_internet": self.has_internet,
                "registration_date": [rd.year, rd.month, rd.day, rd.hour, rd.minute, rd.second]}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
