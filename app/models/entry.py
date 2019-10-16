from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired
from common.db import db, ExtendedDocument, ExtendedEmbeddedDocument, DTYPES
from models.form import FormModel


class EntryModel(ExtendedDocument):
    """
    This Model stores a reference to a form and any pre filled fields
    """
    meta = {'collection': 'entries'}

    _form = db.ReferenceField(FormModel, reverse_delete_rule=2, required=True, unique_with="values")
    values = db.EmbeddedDocumentField()  # TODO must put something here

    @property
    def form(self):
        # TODO convert the FormModel to a form <using wtforms>
        return self._form

    @form.setter
    def form(self, value):
        self._form = value


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

