from flask_restful import Resource, reqparse
from models.field import FieldModel
from common.db import DTYPES


class Field(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument("name", type=str, required=True, help="Field name missing.")
    parser.add_argument("displayed_text", type=str)
    parser.add_argument("data_type", type=str, choices=DTYPES.keys(), required=True, help="Field type missing.")
    parser.add_argument("required", type=bool)
    parser.add_argument("unique", type=bool)
    parser.add_argument("unique_with", type=list, location="json")
    # parser.add_argument("primary_key", type=bool)
    parser.add_argument("choices", type=list, location="json")
    parser.add_argument("help_text", type=str)
    parser.add_argument("max_length", type=int)
    parser.add_argument("min_length", type=int)
    parser.add_argument("min_value", type=float)
    parser.add_argument("max_value", type=float)

    def get(self, _id):
        field = FieldModel.find_by_id(_id)
        if field:
            return field.json(), 200
        return {"message": f"Field unavailable."}, 404

    def put(self, _id):
        data = Field.parser.parse_args()
        field = FieldModel.find_by_id(_id)
        valid_data = {key: val for key, val in data.items() if val is not None}
        if field:
            for key, val in valid_data.items():
                setattr(field, key, val)
        else:
            field = FieldModel(**valid_data)
        try:
            field.save()
        except Exception as e:
            return {"message": str(e)}, 500
        return field.json(), 200

    def delete(self, _id):
        field = FieldModel.find_by_id(_id)
        if not field:
            return {"message": f"Field unavailable."}, 400
        try:
            field.delete()
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"The field '{_id}' has been deleted successfully."}, 200


class FieldList(Resource):
    parser = reqparse.RequestParser()

    # TODO add more filters
    parser.add_argument("data_type", type=str, location="args")

    def get(self):
        data = FieldList.parser.parse_args()
        # TODO filters should happen at the db query level
        fields = FieldModel.find_all()
        if fields:
            return {field.name: field.json(exclude=["name"]) for field in fields}, 200
        return {"message": f"No fields were found."}, 404

    def post(self):
        data = Field.parser.parse_args()
        field = FieldModel.find_by_name(data.name)
        if field:
            return {"message": f"A field with the name '{data.name}' already exists."}, 400
        valid_data = {key: val for key, val in data.items() if val is not None}
        field = FieldModel(**valid_data)
        try:
            field.save()
        except Exception as e:
            return {"message": str(e)}, 500
        return field.json(), 201
