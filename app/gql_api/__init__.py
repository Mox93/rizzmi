from graphene import (Schema, ObjectType, List, Field, ID, String, Int)
from gql_api.auth import TokenType, create_tokens, refresh_access_token, create_fresh_token
from gql_api.form import FormType, FormOps
from gql_api.field import FieldType, FieldOps, EmbeddedFieldType
from gql_api.user import UserType, Signup, CreateUser, UpdateUser, DeleteUser, ChangePassword
from models.form import FormTemplateModel
from models.field import FieldModel
from models.user import UserModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."

    signup = Signup.Field()

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    change_password = ChangePassword.Field()
    delete_user = DeleteUser.Field()

    field_ops = FieldOps.Field()
    form_ops = FormOps.Field()


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    login = Field(TokenType, email=String(required=True), password=String(required=True))
    refresh = Field(TokenType, password=String(required=True))
    authenticate = Field(TokenType)

    user_list = List(UserType)
    user = Field(UserType, _id=ID(required=True))

    form_list = List(FormType)
    form = Field(FormType, _id=ID(required=True))

    field_list = List(FieldType)
    field = Field(FieldType, _id=ID(required=True))

    @staticmethod
    def resolve_login(root, info, email, password):
        if email and password:
            user = UserModel.find_by_email(email)
            if user and check_password_hash(user.password, password):
                return create_tokens(user)
            raise Exception("email or password were in correct")

    @staticmethod
    @jwt_refresh_token_required
    def resolve_refresh(root, info):
        current_user = UserModel.find_by_email(get_jwt_identity().email)
        if current_user:
            return refresh_access_token(current_user)

    @staticmethod
    @jwt_required
    def resolve_authenticate(root, info, password):
        current_user = UserModel.find_by_email(get_jwt_identity().email)
        if current_user and check_password_hash(user.password, password):
            return create_fresh_token(current_user)
        raise Exception("password was in correct")

    @staticmethod
    # @jwt_required
    def resolve_user_list(root, info):
        return UserModel.find_all()

    @staticmethod
    def resolve_user(root, info, _id):
        return UserModel.find_by_id(_id)

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

