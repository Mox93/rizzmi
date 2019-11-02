from graphene import (Schema, ObjectType, List, Field, ID)
from gql_api.form import FormType, CreateForm
from gql_api.field import (FieldType, EmbeddedFieldType,
                           CreateField, AddField,
                           UpdateField, EditField,
                           DeleteField)
from models.form import FormTemplateModel
from models.field import FieldModel


class MutationType(ObjectType):
    new_field = CreateField.Field()
    add_field = AddField.Field()
    update_field = UpdateField.Field()
    edit_field = EditField.Field()
    delete_field = DeleteField.Field()

    new_form = CreateForm.Field()


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    form_list = List(FormType)
    form = Field(FormType, _id=ID(required=True))

    field_list = List(FieldType)
    field = Field(FieldType, _id=ID(required=True))

    @staticmethod
    def resolve_form_list(root, info):
        return FormTemplateModel.find_all()

    @staticmethod
    def resolve_form(root, info, _id):
        return FormTemplateModel.find_by_id(_id)

    @staticmethod
    def resolve_field_list(root, info):
        return FieldModel.find_all()

    @staticmethod
    def resolve_field(root, info, _id):
        return FieldModel.find_by_id(_id)


schema = Schema(query=QueryType, mutation=MutationType,
                types=[EmbeddedFieldType, FieldType, FormType])

