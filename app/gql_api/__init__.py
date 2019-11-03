from graphene import (Schema, ObjectType, List, Field, ID)
from gql_api.form import FormType, FormOps
from gql_api.field import FieldType, FieldOps, EmbeddedFieldType
from models.form import FormTemplateModel
from models.field import FieldModel


class MutationType(ObjectType):
    field_ops = FieldOps.Field()
    form_ops = FormOps.Field()


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

