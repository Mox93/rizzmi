from common.db import ExtendedDocument, DTYPES


class EntryModel(object):
    """
    This Model takes a FormModel and creates an Entry Document class.
    """

    _instances = {}

    def __new__(cls, form):
        _id = str(form.id)

        if EntryModel._instances.get(_id, None):
            return EntryModel._instances[_id]

        attrs = {"meta": {'collection': form.name}}

        for field in form.fields:
            name = field.name
            field_init = DTYPES.get(field.data_type, DTYPES["dynamic"])
            props = field.json(exclude=["name", "data_type"])
            attrs[name] = field_init(**props)

        # TODO create (find_by, clean, ...) methods
        class_name = "".join(form.name.title().split("_"))
        EntryModel._instances[_id] = type(f"{class_name}EntryModel", (ExtendedDocument, ), attrs)
        return EntryModel._instances[_id]

