from common.db import db, ExtendedDocument
from models.field import EmbeddedFieldModel
from models.collection import Connection, CollectionTemplateModel


class FormTemplateModel(ExtendedDocument):
    """
    A template that contains the properties for creating the form.
    Each form can have one direct connection to a new collection,
    but can be linked to multiple existing collections in the database.
    The main field are:
        - name:                 the name that will show in the form list
        - title:                the title that will show in the top of the form
        - description:          text that is displayed under the title
        - fields:               a list of all the fields in the order they appear in the form
        ======================
        - collections:          a list of references to any existing collection the form should be linked to
        - default_collection:   the default collection which the form will be storing all unlinked fields
        - links:                a list of all the different versions of the form, referenced by id
    """
    meta = {'collection': 'forms'}

    # TODO divide the form visually into sections
    # TODO being able to add more than one (titles + descriptions)

    name = db.StringField(required=True, max_length=50, default="Untitled Form")
    title = db.StringField(required=True, max_length=500, default="Untitled Form")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)

    # form meta data
    collections = db.ListField(db.LazyReferenceField(CollectionTemplateModel, reverse_delete_rule=4))
    default_collection = db.EmbeddedDocumentField(Connection, required=True, default=Connection())
    links = db.ListField(db.ObjectIdField())

    def __init__(self, *args, **kwargs):
        super(FormTemplateModel, self).__init__(*args, **kwargs)
        self.foreign_fields_id = []

    def clean(self):
        """
        Make fields that don't point to any existing collection point to the default collection
        Add fields from collections onto the form
        Trims off 'name' and 'title' to their maximum length
        """

        # TODO checking which field belongs to which form/collection shouldn't be done here
        # TODO the collection of native fields and foreign fields point at two different things

        print(f"***{self.collections}")
        for field in self.fields:
            print(f">>> {field.collection}")

            if not field.collection:
                print("Didn't have a collection")
                field.collection = self.default_collection._id

            elif field.collection == self.default_collection._id:
                print("Had the default collection")
                if field._id in self.foreign_fields_id:
                    self.foreign_fields_id.remove(field._id)

            elif field.collection in self.collections:  # This is looking in the wrong place
                print("Had a foreign collection")
                if field._id not in self.foreign_fields_id:
                    self.foreign_fields_id.append(field._id)

            else:
                print("Had something else")
                field.collection = self.default_collection._id
                if field._id in self.foreign_fields_id:
                    self.foreign_fields_id.remove(field._id)
        
        for collection in self.collections:
            for field in collection.fetch().fields:
                if field._id not in self.foreign_fields_id:
                    self.fields.append(field)
                    self.foreign_fields.append(field._id)

        if isinstance(self.name, str):
            n = FormTemplateModel.name.max_length
            self.name = self.name.strip()[:n] or FormTemplateModel.name.default

        if isinstance(self.title, str):
            n = FormTemplateModel.title.max_length
            self.title = self.title.strip()[:n] or self.name

        if self.name != FormTemplateModel.name.default and self.default_collection.name == Connection.name.default:
            self.default_collection.name = self.name

    def find_field_by_id(self, _id, index=False):
        for i, field in enumerate(self.fields):
            if _id == str(field._id):
                if index:
                    return i, field
                else:
                    return field
        if index:
            return -1, None


class FormMapModel(ExtendedDocument):
    """
    The mapping a all different versions of a from so they can be accessed for filling in.
    Its main fields are:
        - form:     a reference to the FormTemplateModel that will be use to build the form
        - values:   fields that have fixed values  ## probably won't show in the form
    """

    meta = {'collection': 'forms_map'}

    form = db.ReferenceField(FormTemplateModel, reverse_delete_rule=2, required=True)  # , unique_with="values"
    # values = db.EmbeddedDocumentField()  # TODO must put something here

