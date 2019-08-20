import uuid
from common.db import db
from datetime import datetime, date, timedelta


class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    category = db.Column(db.Enum)
    trainers = db.Column(db.ARRAY(db.String, zero_indexes=True))
    description = db.Column(db.Text(1500))
    target_audience = db.Column(db.ARRAY(db.String(50), zero_indexes=True))
    outcomes = db.Column(db.Text(1500))
    requirements = db.Column(db.Text(1500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    total_lectures = db.Column(db.Integer)
    lectures_per_week = db.Column(db.Integer)
    lecture_duration = db.Column(db.Interval)
    min_spg = db.Column(db.Integer)  # spg stands for (students per group)
    max_spg = db.Column(db.Integer)

    def __init__(self, name, category, trainers, description, target_audience, outcomes, requirements,
                 start_date, end_date, total_lectures, lectures_per_week, lecture_duration, min_spg,
                 max_spg, _id=None, registration_date=None):

        self.name = name
        self.category = category
        self.trainers = trainers
        self.description = description
        self.target_audience = target_audience
        self.outcomes = outcomes
        self.requirements = requirements
        self.start_date = date(*start_date)
        self.end_date = date(*end_date)
        self.total_lectures = total_lectures
        self.lectures_per_week = lectures_per_week
        self.lecture_duration = timedelta(**lecture_duration)
        self.min_spg = min_spg  # spg stands for (students per group)
        self.max_spg = max_spg
        self.id = _id or uuid.uuid4().hex
        self.registration_date = registration_date or datetime.utcnow()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        sd = self.start_date
        ed = self.end_date
        rd = self.registration_date
        return {"id": self.id,
                "name": self.name,
                "category": self.category,
                "trainers": self.trainers,
                "description": self.description,
                "target_audience": self.target_audience,
                "outcomes": self.outcomes,
                "requirements": self.requirements,
                "start_date": [sd.year, sd.month, sd.day],
                "end_date": [ed.year, ed.month, ed.day],
                "total_lectures": self.total_lectures,
                "lectures_per_week": self.lectures_per_week,
                "lecture_duration": self.lecture_duration,
                "min_students_per_group": self.min_spg,
                "max_students_per_group": self.max_spg,
                "registration_date": [rd.year, rd.month, rd.day, rd.hour, rd.minute, rd.second]}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


