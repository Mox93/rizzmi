from flask_restful import Resource, reqparse  # , request
from models.entry import EntryModel
from models.form import FormModel
from common.util import ENDPOINT_MAP, PY_DTYPES, mash, boolean

'''
class EntryFactory(object):
    """
    This Model is for creating different resources.
    Each resource should handel its respective FormEntry.
    """

    def __new__(cls, form):
        parser = reqparse.RequestParser(bundle_errors=True)
        for field in form.fields:
            # print(field.json())
            # TODO values aren't always correct or available, need to check <DONE?>
            props = {"type": PY_DTYPES[field.data_type],
                     "required": field.required,
                     "choices": field.choices,
                     "location": "json",
                     "help": field.help_text}
            valid_props = {key: val for key, val in props if val is not None}
            parser.add_argument(field.db_field, **valid_props)

        FormEntry = EntryModel(form)

        # TODO give the CRUD functions more flexibility
        # TODO need a second get for the entry list
        # TODO post needs to be in the entry list

        def get(self, _id):
            entry = FormEntry.find_by_id(_id)
            if entry:
                return entry.json(), 200
            return {"message": f"An entry with the id '{_id}' does not exist in the collection {form.name}."}, 404

        def post(self, _id):
            data = self.parser.parse_args()
            entry = FormEntry.find_by_id(_id)
            if entry:
                return {"message": f"An entry with the id '{_id}' already exists in the collection {form.name}."}, 400
            valid_data = {key: val for key, val in data.items() if val is not None}
            entry = FormEntry(**valid_data)
            try:
                entry.save()
            except Exception as e:
                return {"message": str(e)}, 500
            return entry.json(), 201

        def put(self, _id):
            data = self.parser.parse_args()
            entry = FormEntry.find_by_id(_id)
            valid_data = {key: val for key, val in data.items() if val is not None}
            if entry:
                for key, val in valid_data.items():
                    setattr(entry, key, val)
            else:
                entry = FormEntry(**valid_data)
            try:
                entry.save()
            except Exception as e:
                return {"message": str(e)}, 500
            return form.json(), 200

        def delete(self, _id):
            entry = FormEntry.find_by_id(_id)
            if not form:
                return {"message": f"An entry with the id '{_id}' does not exist in the collection {form.name}."}, 400
            try:
                entry.delete()
            except Exception as e:
                return {"message": str(e)}, 500
            return {"message": f"The entry '{_id}' has been deleted successfully."}, 200

        attrs = {"parser": parser.copy(),
                 "get": get,
                 "post": post,
                 "put": put,
                 "delete": delete}
        class_name = "".join(form.name.title().split("_"))
        # TODO do we need this to be a instance of resource?
        entry_resource = type(f"{class_name}Entry", (Resource,), attrs)

        # urls = (f"/{form.name}/<string:_id>",)
        # URL_MAP.append({"resource": entry_res, "urls": urls})
        # api.add_resource(entry_resource, *urls)

        return entry_resource
'''


class Entry(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    def get(self, entry_id, form_id=None):
        form = FormModel.find_by_id(form_id)

        if not form:
            return {"message": f"Form does not exist."}, 404

        FormEntry = EntryModel(form)
        entry = FormEntry.find_by_id(entry_id)

        if entry:
            return entry.json(), 200

        return {"message": f"Entry does not exist."}, 404

    def put(self, entry_id, form_id=None):
        form = FormModel.find_by_id(form_id)

        if not form:
            return {"message": f"Form does not exist."}, 404

        parser = mash(form, Entry.parser.copy())
        data = parser.parse_args()
        valid_data = {key: val for key, val in data.items() if val is not None}

        FormEntry = EntryModel(form)
        entry = FormEntry.find_by_id(entry_id)

        if entry:
            code = 200
            for key, val in valid_data.items():
                setattr(entry, key, val)
        else:
            code = 201
            entry = FormEntry(**valid_data)

        try:
            entry.save()
        except Exception as e:
            return {"message": str(e)}, 500

        return form.json(), code

    def defete(self, entry_id, form_id=None):
        form = FormModel.find_by_id(form_id)

        if not form:
            return {"message": f"Form does not exist."}, 404

        FormEntry = EntryModel(form)
        entry = FormEntry.find_by_id(entry_id)

        if not form:
            return {"message": f"Entry does not exist."}, 400

        try:
            entry.delete()
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry has been deleted successfully."}, 200


class EntryList(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    def get(self, form_id):
        form = FormModel.find_by_id(form_id)

        if not form:
            return {"message": f"Form does not exist."}, 404

        FormEntry = EntryModel(form)

        entries = FormEntry.find_all()

        if entries:
            return {"entries": [entry.json() for entry in entries]}, 200

        return {"message": f"No entries were found."}, 404

    def post(self, form_id):
        form = FormModel.find_by_id(form_id)

        if not form:
            return {"message": f"Form does not exist."}, 404

        parser = mash(form, EntryList.parser.copy())
        data = parser.parse_args()

        FormEntry = EntryModel(form)

        # TODO should check for unique fields
        entry = None  # FormEntry.find_by_id(entry_id)

        if entry:
            return {"message": f"An entry with the ??? '{None}' already exists."}, 400

        valid_data = {key: val for key, val in data.items() if val is not None}
        entry = FormEntry(**valid_data)

        try:
            entry.save()
        except Exception as e:
            return {"message": str(e)}, 500

        return entry.json(), 201


# fn = EmbeddedFieldModel(db_field="first_name", data_type="str", required=True)
# ln = EmbeddedFieldModel(db_field="last_name", data_type="str", required=True)
# email = EmbeddedFieldModel(db_field="email", data_type="str", required=True, unique=True)
#
# reg = FormModel("registration")
# reg.fields.extend((fn, ln, email))
# RegEntryRes = EntryFactory(reg)
#
# print(URL_MAP)


