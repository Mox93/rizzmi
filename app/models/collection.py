from common.db import db, ExtendedDocument, ExtendedEmbeddedDocument


class Connection(ExtendedEmbeddedDocument):
    """
    A holder for information about the database collection
    Its main fields are:
        - name:                 the displayed name in the webapp
        - dynamic_document:     whether the collection should accept dynamic document or not
    ** the collection name in the database is the Connection's _id
    """

    name = db.StringField(required=True, max_length=50, default="Untitled Collection")
    dynamic_document = db.BooleanField(required=True, default=True)


class CollectionTemplateModel(ExtendedDocument):
    """
    A template containing the fields of documents that are saved in the correlating collection.
    Its main fields are:
        - name:             the name that will show in the collection list
        - title:            the title that will show in the top of the collection
        - description:      text that is displayed under the title
        - fields:           a list of all the fields in the order they show in the collection table
        - db_connection:    information about the actual database collection  ## if exists
    """

    meta = {'collection': 'collection_templates'}

    name = db.StringField(required=True, max_length=50, default="Untitled Collection")
    title = db.StringField(required=True, max_length=500, default="Untitled Collection")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(ExtendedEmbeddedDocument)
    db_connection = db.EmbeddedDocumentField(Connection)

