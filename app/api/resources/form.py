from flask_restful import Resource, reqparse
from common.util import boolean
from models.form import FormModel
from models.field import EmbeddedFieldModel


class Form(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument("name", type=str, required=True, help="Form name missing.")
    parser.add_argument("title", type=str)
    parser.add_argument("fields", type=list, location="json", required=True, help="Fields missing.")
    parser.add_argument("description", type=str)

    def get(self, _id):
        form = FormModel.find_by_id(_id)

        if form:
            return form.json(), 200

        return {"message": "Form unavailable."}, 404

    def put(self, _id):
        form = FormModel.find_by_id(_id)

        if not form:
            return {"message": "Form unavailable."}, 404
            # data = Form.parser.parse_args()
            # valid_data = {key: val for key, val in data.items() if val is not None}
            # form = FormModel(**valid_data)

        parser = Form.parser.copy()
        parser.replace_argument("name", type=str)
        parser.replace_argument("fields", type=list, location="json")
        data = parser.parse_args()

        # TODO do we really need to not have duplicated names?
        # for now we do, because they are used in creating entry classes.
        if data.name:
            other_form = FormModel.find_by_name(data.name)
            if other_form and form.id != other_form.id:
                return {"message": {f"{data.name}": "This name already exists."}}

        valid_data = {key: val for key, val in data.items() if val is not None}

        # TODO the fields are not being updated
        if valid_data.get("fields", None):
            # fields = [EmbeddedFieldModel(**field) for field in valid_data["fields"]]
            fields = valid_data["fields"]

            print(f"fields = {form.fields}")
            print(f"new_field = {fields}")

            for field in fields:
                current_field = EmbeddedFieldModel.find_by_id(field["_id"])
                print(current_field)
                if current_field:
                    for key, val in field.items():
                        setattr(current_field, key, val)
                else:
                    current_field = EmbeddedFieldModel(**field)

            del valid_data["fields"]

        for key, val in valid_data.items():
            setattr(form, key, val)

        try:
            form.save()
            # form.integrate()
        except Exception as e:
            return {"message": str(e)}, 500

        return form.json(), 200

    def delete(self, _id):
        form = FormModel.find_by_id(_id)

        if not form:
            return {"message": f"Form unavailable."}, 400

        try:
            form.delete()
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"The form '{_id}' has been deleted successfully."}, 200


class FormList(Resource):
    parser = reqparse.RequestParser()

    # TODO add more filters
    parser.add_argument("has_description", type=boolean, location="args")

    def get(self):
        data = FormList.parser.parse_args()

        # TODO filters should happen at the db query level
        forms = FormModel.find_all()

        if forms:
            return {"forms": [form.json() for form in forms]}, 200

        return {"message": "No forms were found."}, 404

    def post(self):

        # TODO everything passed through the field list gets taken and that shouldn't happen!
        data = Form.parser.parse_args()

        # TODO do we really need to not have duplicated names?
        # for now we do, because they are used in creating entry classes.
        form = FormModel.find_by_name(data.name)

        if form:
            return {"message": f"A form with the name '{data.name}' already exists."}, 400

        valid_data = {key: val for key, val in data.items() if val is not None}
        form = FormModel(**valid_data)

        try:
            form.save()
        except Exception as e:
            return {"message": str(e)}, 500

        return form.json(), 201


# TODO create resource for handling fields inside the form
