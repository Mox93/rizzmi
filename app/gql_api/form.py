from graphene import (ObjectType, Interface, Mutation, InputObjectType,
                      String, Int, Boolean, DateTime, ID, List, Field, InputField)
from gql_api.field import EmbeddedFieldType, EmbeddedFieldInput
from models.form import FormTemplateModel


class CommonAttributes(object):
    name = String()
    title = String()
    description = String()
    collections = List(ID)


######################################################################


class CommonFormAttributes(CommonAttributes, Interface):
    _id = ID()
    creation_date = DateTime()
    modified_date = DateTime()

    fields = List(EmbeddedFieldType)
    field = Field(EmbeddedFieldType, _id=ID(required=True))
    default_collection = ID()
    links = List(ID)

    @staticmethod
    def resolve_field(root, info, _id):
        return root.find_field_by_id(_id)


class FormType(ObjectType):
    class Meta:
        name = "Form"
        description = "..."
        interfaces = (CommonFormAttributes,)


######################################################################


class FormInput(CommonAttributes, InputObjectType):
    fields = InputField(List(EmbeddedFieldInput))


class CreateForm(Mutation):
    class Meta:
        name = "NewForm"
        description = "..."

    class Arguments:
        form_data = FormInput(required=True)

    ok = Boolean()
    form = Field(lambda: FormType)

    @staticmethod
    def mutate(root, info, form_data, **kwargs):
        form = FormTemplateModel(**form_data)

        try:
            form.save()
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

        return CreateForm(form=form, ok=ok)


class UpdateForm(Mutation):
    class Meta:
        name = "UpdateForm"
        description = "..."

    class Arguments:
        form_id = ID(required=True)
        form_data = FormInput(required=True)

    ok = Boolean()
    form = Field(lambda: FormType)

    @staticmethod
    def mutate(root, info, form_id, form_data, **kwargs):
        form = FormTemplateModel.find_by_id(form_id)

        try:
            for prop in form_data:
                if hasattr(form, prop) and prop != "fields":
                    setattr(form, prop, form_data[prop])
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

