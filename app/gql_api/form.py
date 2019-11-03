from graphene import (ObjectType, Interface, Mutation, InputObjectType,
                      String, Int, Boolean, DateTime, ID, List, Field, InputField)
from gql_api.field import EmbeddedFieldType, EmbeddedFieldInput, AddField, EditField, RemoveField
from models.form import FormTemplateModel
from models.field import EmbeddedFieldModel


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


class CreateForm(InputObjectType):
    form_data = InputField(FormInput, required=True)


class UpdateForm(InputObjectType):
    form_id = ID(required=True)
    form_data = InputField(FormInput, required=True)


class DeleteForm(InputObjectType):
    form_id = ID(required=True)


class FormOps(Mutation):
    class Meta:
        name = "FormOps"
        description = "..."

    class Arguments:
        create = CreateForm()
        update = UpdateForm()
        delete = DeleteForm()

        add_field = AddField()
        edit_field = EditField()
        remove_field = RemoveField()

    ops = List(String)
    ok = Boolean()
    form = Field(lambda: FormType)

    @staticmethod
    def mutate(root, info, create=None, update=None, delete=None,
               add_field=None, edit_field=None, remove_field=None, **kwargs):
        ops = []
        ok = False
        form = None

        if create:
            ops.append("create")

            form = FormTemplateModel(**create.form_data)

            try:
                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if update:
            ops.append("update")

            form = FormTemplateModel.find_by_id(update.form_id)

            try:
                for atr in update.form_data:
                    if hasattr(form, atr) and atr != "fields":
                        setattr(form, atr, update.form_data[atr])
                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if add_field:
            ops.append("add_field")

            form = FormTemplateModel.find_by_id(add_field.form_id)
            field = EmbeddedFieldModel(**add_field.field_data)

            try:
                form.fields.insert(field.index, field)
                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if edit_field:
            ops.append("edit_field")

            form = FormTemplateModel.find_by_id(edit_field.form_id)

            try:
                field = form.find_field_by_id(edit_field.field_id)
                index = edit_field.field_data.get("index", field.index)
                if index != field.index:
                    form.fields.remove(field)
                    form.fields.insert(index, field)

                for atr in edit_field.field_data:
                    if hasattr(field, atr):
                        setattr(field, atr, edit_field.field_data[atr])

                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if remove_field:
            ops.append("remove_field")

            form = FormTemplateModel.find_by_id(remove_field.form_id)

            try:
                field = form.find_field_by_id(remove_field.field_id)
                form.fields.remove(field)
                form.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

        if delete:
            ops.append("delete")

            form = FormTemplateModel.find_by_id(delete.form_id)

            try:
                form.delete()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

            return FormOps(ok=ok, ops=ops)

        return FormOps(ok=ok, form=form, ops=ops)

