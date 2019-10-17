from bson import ObjectId
from common.db import db, ExtendedDocument
from models.field import EmbeddedFieldModel, ExtendedEmbeddedDocument


class Connection(ExtendedEmbeddedDocument):
    """
    ...
    """
    name = db.StringField(required=True, max_length=50, default="Untitled Connection")
    collection = db.ObjectIdField(required=True, default=ObjectId)


class CollectionModel(ExtendedDocument):
    """
    ...
    """
    meta = {'collection': 'collections'}

    name = db.StringField(required=True, max_length=50, default="Untitled Collection")
    title = db.StringField(required=True, max_length=500, default="Untitled Collection")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)
    db_connection = db.EmbeddedDocumentField(Connection)

    # Embedded Document Version
    _embedded = None

    @classmethod
    def as_embedded(cls, *args, **kwargs):
        if not cls._embedded:
            cls._embedded = type("EmbeddedCollectionModel", (ExtendedEmbeddedDocument,),
                                 {"_id": db.ObjectIdField(unique=True, default=ObjectId, sparse=True),
                                  "title": cls.title,
                                  "description": cls.description,
                                  "fields": cls.fields,
                                  "db_connection": cls.db_connection})
        if args or kwargs:
            return cls._embedded(*args, **kwargs)
        return cls._embedded


EmbeddedCollectionModel = CollectionModel.as_embedded()


class FormModel(ExtendedDocument):
    """
    This Model is for storing form templates.
    Each form can refer to one or more collections in the database.
    """
    meta = {'collection': 'forms'}

    # TODO divide the form visually into sections

    name = db.StringField(required=True, max_length=50, default="Untitled Form")
    title = db.StringField(required=True, max_length=500, default="Untitled Form")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)
    collections = db.ListField(db.ReferenceField(CollectionModel))
    db_connection = db.EmbeddedDocumentField(Connection, required=True, default=Connection())
    links = db.ListField(db.StringField())

    def clean(self):
        """
        * Trims off name to its maximum length
        """

        if isinstance(self.name, str):
            self.name = self.name.strip()[:50] or FormModel.name.default

        if isinstance(self.title, str):
            self.title = self.title.strip()[:500] or self.name

        if self.name != FormModel.name.default and self.db_connection.name == Connection.name.default:
            self.db_connection.name = self.name

    def find_field_by_id(self, _id, index=False):
        for i, field in enumerate(self.fields):
            if _id == str(field._id):
                if index:
                    return i, field
                else:
                    return field
        if index:
            return -1, None

