from common.db import db, ExtendedDocument, ExtendedEmbeddedDocument, DTYPES
from models.form import FormModel


class EntryModel(ExtendedDocument):
    """
    This Model stores a reference to a form and any pre filled fields
    """

    meta = {'collection': 'entries'}

    form = db.ReferenceField(FormModel, reverse_delete_rule=2, required=True)  # , unique_with="values"
    # values = db.EmbeddedDocumentField()  # TODO must put something here


class FormEntry(object):
    """
    This Model takes a FormModel and creates a form out of it with fields mapped to the appropriate collection.
    """

    _instances = {}

    # Embedded Document Version
    _embedded = None

    def __new__(cls, form):
        _id = str(form.id)

        if cls._instances.get(_id, None):
            return cls._instances[_id]

        attrs = {"meta": {'collection': form.name}}

        for field in form.fields:
            name = field.name
            field_init = DTYPES.get(field.data_type, DTYPES["dynamic"])
            props = field.json(exclude=["name", "data_type"])
            attrs[name] = field_init(**props)

        # TODO create (clean, ...) methods
        class_name = "".join(form.name.title().split("_"))
        cls._instances[_id] = type(f"{class_name}FormEntry", (ExtendedDocument, ), attrs)
        return cls._instances[_id]

