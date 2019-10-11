from bson import ObjectId
from datetime import datetime
from common.db import db, ExtendedDocument
from models.field import EmbeddedFieldModel, ExtendedEmbeddedDocument


class Connection(ExtendedEmbeddedDocument):
    """
    ...
    """
    collection = db.StringField(max_length=50)

    def __repr__(self):
        return self.collection


class SectionModel(ExtendedDocument):
    """
    ...
    """
    meta = {'collection': 'sections'}

    name = db.StringField(required=True, max_length=50, default="Untitled Section")
    title = db.StringField(required=True, max_length=500, default="Untitled Section")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)
    db_connection = db.EmbeddedDocumentField(Connection)

    # Embedded Document Version
    _embedded = None

    @classmethod
    def as_embedded(cls, *args, **kwargs):
        if not cls._embedded:
            cls._embedded = type("EmbeddedSectionModel", (ExtendedEmbeddedDocument,),
                                 {"_id": db.ObjectIdField(unique=True, default=ObjectId, sparse=True),
                                  "title": cls.title,
                                  "description": cls.description,
                                  "fields": cls.fields,
                                  "db_connection": cls.db_connection})
        if args or kwargs:
            return cls._embedded(*args, **kwargs)
        return cls._embedded


class FormModel(ExtendedDocument):
    """
    This Model is for storing created forms.
    Each form refers to a collection in the database.
    """
    meta = {'collection': 'forms'}

    # TODO divide the Form into sections

    name = db.StringField(required=True, max_length=50, default="Untitled Form")
    title = db.StringField(required=True, max_length=500, default="Untitled Form")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)
    sections = db.EmbeddedDocumentListField(SectionModel.as_embedded())
    db_connection = db.EmbeddedDocumentField(Connection)

    def clean(self):
        """
        * Trims off name to its maximum length
        """

        if isinstance(self.name, str):
            self.name = self.name.strip()[:50] or "Untitled Form"

        if isinstance(self.title, str):
            self.title = self.title.strip()[:500] or self.name

    def find_field_by_id(self, _id, index=False):
        for i, field in enumerate(self.fields):
            if _id == str(field._id):
                if index:
                    return i, field
                else:
                    return field
        if index:
            return -1, None

