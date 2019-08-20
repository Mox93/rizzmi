from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.trainer import TrainerModel


class Trainer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name", type=str, required=True, help="Enter a first name.")
    parser.add_argument("middle_name", type=str, required=False)
    parser.add_argument("last_name", type=str, required=True, help="Enter a surname.")
    parser.add_argument("email", type=str, required=True, help="Enter a email.")
    parser.add_argument("phone_No_1", type=str, required=True, help="Enter a phone number.")
    parser.add_argument("phone_No_2", type=str, required=False)
    parser.add_argument("phone_No_3", type=str, required=False)

    def get(self, _id):
        user = TrainerModel.find_by_id(_id)
        if user:
            return user.json()
        return {"message": "No matching account."}, 404

    def put(self, _id):
        data = self.parser.parse_args()
        user = TrainerModel.find_by_id(_id)

        if user:
            user.first_name = data["first_name"]  # if data["first_name"] else user.first_name
            user.middle_name = data["middle_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.phone_No_1 = data["phone_No_1"]
            user.phone_No_2 = data["phone_No_2"]
            user.phone_No_3 = data["phone_No_3"]
        else:
            valid_data = {key: val for key, val in data.items() if val is not None}
            user = TrainerModel(**valid_data)

        user.save_to_db()
        return user.json()

    def delete(self, _id):
        user = TrainerModel.find_by_id(_id)
        if user:
            try:
                user.delete_from_db()
            except:
                return {"message": "An error occurred while deleting this user."}, 500

            return {'message': 'User deleted.'}

        return {'message': "The user you're trying to delete doesn't exist."}, 400


class TrainerRegister(Trainer):
    def post(self):
        data = self.parser.parse_args()

        if TrainerModel.find_by_email(data["email"]):
            return {'message': "The email {} already exists.".format(data["email"])}, 400

        valid_data = {key: val for key, val in data.items() if val is not None}
        user = TrainerModel(**valid_data)

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while registering this user."}, 500

        return user.json(), 201
