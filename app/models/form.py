from common.db import db, ExtendedDocument
from common.util import ENDPOINT_MAP
from models.field import EmbeddedFieldModel
# from api.resources.entry import EntryFactory


class FormModel(ExtendedDocument):
    """
    This Model is for storing created forms.
    Each form refers to a collection in the database.
    """
    meta = {'collection': 'forms'}

    # TODO divide the Form into sections

    name = db.StringField(required=True, max_length=50, unique=True)
    title = db.StringField(required=True, max_length=100)
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel, required=True)
    description = db.StringField(max_length=500)

    def clean(self):
        """
        * Ensures that only ...
        """
        # TODO might need to convert from title to name as well
        if self.name:
            self.name = self.name.lower()
            if not self.title:
                self.title = " ".join(self.name.split("_")).title()

    @classmethod
    def find_by_name(cls, name):
        return cls.objects(name=name.lower()).first()


# form = FormModel("registration")
# field = EmbeddedFieldModel(db_field="first_name")
#
# form.fields.append(field)
#
# print(form.fields)
# print(field)
# form.save()

