from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.customer import CustomerModel
from datetime import date


class Customer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name", type=str, required=True, help="Enter a first name.")
    parser.add_argument("middle_name", type=str, required=False)
    parser.add_argument("last_name", type=str, required=True, help="Enter a surname.")
    parser.add_argument("gender", type=str, required=True, help="Enter a gender.")
    parser.add_argument("email", type=str, required=True, help="Enter a email.")
    parser.add_argument("phone_No_1", type=str, required=True, help="Enter a phone number.")
    parser.add_argument("phone_No_2", type=str, required=False)
    parser.add_argument("phone_No_3", type=str, required=False)
    parser.add_argument("address", type=str, required=True, help="Enter an address.")
    parser.add_argument("date_of_birth", type=list, required=True, help="Enter a date of birth.", location="json")
    parser.add_argument("social_status", type=str, required=True, help="Enter a social status.")
    parser.add_argument("national_id", type=str, required=True, help="Enter a national ID.")
    parser.add_argument("has_smartphone", type=bool, required=False)
    parser.add_argument("has_computer", type=bool, required=False)
    parser.add_argument("has_internet", type=bool, required=False)

    def get(self, _id):
        user = CustomerModel.find_by_id(_id)
        if user:
            return user.json()
        return {"message": "No matching account."}, 404

    def put(self, _id):
        data = self.parser.parse_args()
        user = CustomerModel.find_by_id(_id)

        if user:
            user.first_name = data["first_name"]  # if data["first_name"] else user.first_name
            user.middle_name = data["middle_name"]
            user.last_name = data["last_name"]
            user.date_of_birth = date(*data["date_of_birth"])
            user.gender = data["gender"]
            user.email = data["email"]
            user.phone_No_1 = data["phone_No_1"]
            user.phone_No_2 = data["phone_No_2"]
            user.phone_No_3 = data["phone_No_3"]
            user.address = data["address"]
            user.social_status = data["social_status"]
            user.national_id = data["national_id"]
            user.has_smartphone = data["has_smartphone"]
            user.has_computer = data["has_computer"]
            user.has_internet = data["has_internet"]
        else:
            valid_data = {key: val for key, val in data.items() if val is not None}
            user = CustomerModel(**valid_data)

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while saving to the database."}, 500

        return user.json()

    def delete(self, _id):
        user = CustomerModel.find_by_id(_id)
        if user:
            try:
                user.delete_from_db()
            except:
                return {"message": "An error occurred while deleting this user."}, 500

            return {'message': 'User deleted.'}

        return {'message': "The user you're trying to delete doesn't exist."}, 400


class CustomerRegister(Customer):
    def post(self):
        data = self.parser.parse_args()
        user = CustomerModel.find_by_email(data["email"])
        if user:
            return {'message': "The email {} already exists.".format(data["email"])}, 400

        valid_data = {key: val for key, val in data.items() if val is not None}
        user = CustomerModel(**valid_data)

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while saving to the database."}, 500

        return user.json(), 201
