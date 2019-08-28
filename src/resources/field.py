from flask_restful import Resource, reqparse
from models.field import FieldModel


class Field(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("db_field", type=str)
    parser.add_argument("displayed_text", type=str)
    parser.add_argument("data_type", type=str, required=True, help="Field type missing!")
    parser.add_argument("required", type=bool)
    parser.add_argument("unique", type=bool)
    parser.add_argument("unique_with", type=list, location="json")
    parser.add_argument("primary_key", type=bool)
    parser.add_argument("choices", type=list, location="json")
    parser.add_argument("help_text", type=str)
    parser.add_argument("max_length", type=int)
    parser.add_argument("min_length", type=int)
    parser.add_argument("min_value", type=float)
    parser.add_argument("max_value", type=float)

    def get(self, name):
        field = FieldModel.find_by_name(name)
        if field:
            return field.json(), 200
        return {"message": f"A field with the name '{name}' does not exist."}, 404

    def post(self, name):
        data = Field.parser.parse_args()
        field = FieldModel.find_by_name(name)
        if field:
            return {"message": f"A field with the name '{name}' already exists."}, 400
        valid_data = {key: val for key, val in data.items() if val is not None}
        valid_data["db_field"] = valid_data.get("db_field", name)
        field = FieldModel(**valid_data)
        try:
            field.save()
        except Exception as e:
            return {"message": str(e)}, 500
        return field.json(), 201

    def put(self, name):
        data = Field.parser.parse_args()
        field = FieldModel.find_by_name(name)
        valid_data = {key: val for key, val in data.items() if val is not None}
        if field:
            for key, val in valid_data.items():
                setattr(field, key, val)
        else:
            valid_data["db_field"] = valid_data.get("db_field", name)
            field = FieldModel(**valid_data)
        try:
            field.save()
        except Exception as e:
            return {"message": str(e)}, 500
        return field.json(), 200

    def delete(self, name):
        field = FieldModel.find_by_name(name)
        if not field:
            return {"message": f"A field with the name '{name}' does not exist."}, 400
        try:
            field.delete()
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"The field '{name}' has been deleted successfully."}, 200

