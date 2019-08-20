from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.course import CourseModel
from datetime import datetime, date, timedelta


class Course(Resource):
    parser = reqparse.RequestParser()
    parsing_map = {"name": {"type": str, "required": True, "help": "Enter a name for the course."},
                   "category": {"type": str, "required": True, "help": ""},
                   "trainers": {"type": list, "required": True, "help": "",
                                "location": "json"},
                   "description": {"type": str, "required": True, "help": ""},
                   "target_audience": {"type": str, "required": True, "help": ""},
                   "outcomes": {"type": str, "required": True, "help": ""},
                   "requirements": {"type": str, "required": True, "help": ""},
                   "start_date": {"type": str, "required": True, "help": ""},
                   "end_date": {"type": str, "required": True, "help": ""},
                   "total_lectures": {"type": str, "required": True, "help": ""},
                   "lectures_per_week" : {"type": str, "required": True, "help": ""},
                   "lecture_duration": {"type": str, "required": True, "help": ""},
                   "min_students_per_group": {"type": str, "required": True, "help": ""},
                   "max_students_per_group": {"type": str, "required": True, "help": ""}}

    for name, kwargs in parsing_map.items():
        parser.add_argument(name, **kwargs)

    def get(self, _id):
        course = CourseModel.find_by_id(_id)
        if course:
            return course.json()
        return {"message": "No matching course."}, 404

    def put(self, _id):
        data = self.parser.parse_args()
        course = CourseModel.find_by_id(_id)

        if course:
            course.name = data["name"]
            course.category = data["category"]
            course.trainers = data["trainers"]
            course.description = data["description"]
            course.target_audience = data["target_audience"]
            course.outcomes = data["outcomes"]
            course.requirements = data["requirements"]
            course.start_date = date(*data["start_date"])
            course.end_date = date(*data["end_date"])
            course.total_lectures = data["total_lectures"]
            course.lectures_per_week = data["lectures_per_week"]
            course.lecture_duration = timedelta(*data["lecture_duration"])
            course.min_spg = data["min_students_per_group"]
            course.max_spg = data["max_students_per_group"]
        else:
            valid_data = {key: val for key, val in data.items() if val is not None}
            course = CourseModel(**valid_data)

        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred while saving to the database."}, 500

        return course.json()

    def delete(self, _id):
        course = CourseModel.find_by_id(_id)
        if course:
            try:
                course.delete_from_db()
            except:
                return {"message": "An error occurred while deleting this course."}, 500

            return {'message': 'Course deleted.'}

        return {'message': "The course you're trying to delete doesn't exist."}, 400


class CourseRegister(Course):
        def post(self):
            data = self.parser.parse_args()
            # course = CourseModel.find_by_email(data["email"])
            # if course:
            #     return {'message': "The email {} already exists.".format(data["email"])}, 400

            valid_data = {key: val for key, val in data.items() if val is not None}
            course = CourseModel(**valid_data)

            try:
                course.save_to_db()
            except:
                return {"message": "An error occurred while saving to the database."}, 500

            return course.json(), 201


