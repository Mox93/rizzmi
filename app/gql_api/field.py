from graphene import (ObjectType, Interface, Mutation, InputObjectType,
                      String, Int, Boolean, DateTime, ID, List, Field, InputField)
from models.field import FieldModel, EmbeddedFieldModel
from models.form import FormTemplateModel


class CommonAttributes(object):
    question = String()
    description = String()
    required = Boolean()
    input_type = String()


class CommonFieldAttributes(CommonAttributes, Interface):
    _id = ID()


######################################################################


class FieldType(ObjectType):
    class Meta:
        name = "Field"
        description = "..."
        interfaces = (CommonFieldAttributes,)

    creation_date = DateTime()
    modified_date = DateTime()

    name = String()


######################################################################


class FieldInput(CommonAttributes, InputObjectType):
    name = String()


class CreateField(Mutation):
    class Meta:
        name = "NewField"
        description = "..."

    class Arguments:
        field_data = FieldInput(required=True)

    ok = Boolean()
    field = Field(lambda: FieldType)

    @staticmethod
    def mutate(root, info, field_data=None, **kwargs):
        field = FieldModel(**field_data)

        try:
            field.save()
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

        return CreateField(field=field, ok=ok)


class UpdateField(Mutation):
    class Meta:
        name = "UpdateField"
        description = "..."

    class Arguments:
        field_id = ID(required=True)
        field_data = FieldInput(required=True)

    ok = Boolean()
    field = Field(lambda: EmbeddedFieldType)

    @staticmethod
    def mutate(root, info, field_id, field_data, **kwargs):
        field = FieldModel.find_by_id(field_id)

        for prop in field_data:
            if hasattr(field, prop):
                setattr(field, prop, field_data[prop])

        try:
            field.save()
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

        return UpdateField(field=field, ok=ok)


######################################################################
######################################################################


class EmbeddedFieldType(ObjectType):
    class Meta:
        name = "EmbeddedField"
        description = "..."
        interfaces = (CommonFieldAttributes,)

    index = Int()
    collection = ID()


######################################################################


class EmbeddedFieldInput(CommonAttributes, InputObjectType):
    index = Int()
    collection = ID()


class AddField(Mutation):
    class Meta:
        name = "AddField"
        description = "..."

    class Arguments:
        form_id = ID(required=True)
        field_data = EmbeddedFieldInput(required=True)

    ok = Boolean()
    field = Field(lambda: EmbeddedFieldType)

    @staticmethod
    def mutate(root, info, form_id, field_data=None, **kwargs):
        form = FormTemplateModel.find_by_id(form_id)
        field = EmbeddedFieldModel(**field_data)

        try:
            form.fields.insert(field.index, field)
            form.save()
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

        return AddField(field=field, ok=ok)


class EditField(Mutation):
    class Meta:
        name = "EditField"
        description = "..."

    class Arguments:
        form_id = ID(required=True)
        field_id = ID(required=True)
        field_data = EmbeddedFieldInput(required=True)

    ok = Boolean()
    field = Field(lambda: EmbeddedFieldType)

    @staticmethod
    def mutate(root, info, form_id, field_id, field_data, **kwargs):
        form = FormTemplateModel.find_by_id(form_id)

        try:
            field = form.find_field_by_id(field_id)
            for prop in field_data:
                if hasattr(field, prop):
                    setattr(field, prop, field_data[prop])

            form.save()
            ok = True
        except Exception as e:
            print(str(e))
            ok = False

        return EditField(field=field, ok=ok)


######################################################################
######################################################################


class DeleteField(Mutation):
    class Meta:
        name = "DeleteField"
        description = "..."

    class Arguments:
        form_id = ID()
        field_id = ID(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, field_id, form_id=None, **kwargs):
        if form_id:
            form = FormTemplateModel.find_by_id(form_id)

            try:
                field = form.find_field_by_id(field_id)
                form.fields.remove(field)
                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        else:
            field = FieldModel.find_by_id(field_id)
            try:
                field.delete()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        return DeleteField(ok=ok)

