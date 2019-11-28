from models.user import UserModel
from gql_api.auth import TokenType, create_tokens
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from graphene import (ObjectType, Interface, Mutation, InputObjectType,
                      String, Int, Boolean, DateTime, ID, List, Field, InputField)


class CommonAttributes(object):
    first_name = String()
    last_name = String()
    email = String()
    phone_number = String()


######################################################################


class UserInterface(CommonAttributes, Interface):
    _id = ID()
    creation_date = DateTime()
    modified_date = DateTime()


class UserType(ObjectType):
    class Meta:
        name = "User"
        description = "..."
        interfaces = (UserInterface,)


######################################################################


class StrictUserInput(InputObjectType):
    first_name = String(required=True)
    last_name = String(required=True)
    email = String(required=True)
    phone_number = String(required=True)
    password = String(required=True)


class CreateUser(Mutation):
    class Meta:
        name = "CreateUser"
        description = "..."

    class Arguments:
        user_data = StrictUserInput(required=True)

    ok = Boolean()
    user = Field(lambda: UserType)
    auth = Field(lambda: TokenType)

    @staticmethod
    @jwt_required
    def mutate(root, info, user_data):
        email_exists = UserModel.find_by_email(user_data.email)
        phone_number_exists = UserModel.find_by_phone_number(user_data.phone_number)

        if email_exists or phone_number_exists:
            return CreateUser(ok=False, user=user_data)

        user = UserModel(**user_data)

        try:
            user.password = generate_password_hash(user_data.password, method="sha256")
            user.save()
            return CreateUser(ok=True, user=user, auth=create_tokens(user))
        except Exception as e:
            print(str(e))
            return CreateUser(ok=False, user=user_data)

# ================================================================== #


class UserInput(CommonAttributes, InputObjectType):
    pass


class UpdateUser(Mutation):
    class Meta:
        name = "UpdateUser"
        description = "..."

    class Arguments:
        user_data = UserInput(required=True)

    ok = Boolean()
    user = Field(lambda: UserType)

    @staticmethod
    @jwt_required
    def mutate(root, info, user_data):
        user = UserModel.find_by_email(get_jwt_identity().email)

        if not user:
            return UpdateUser(ok=False, user=user_data)

        try:
            for atr, val in user_data.items():
                if atr == "password":
                    user.password = generate_password_hash(val, method="sha256")
                elif hasattr(user, atr):
                    setattr(user, atr, val)
            user.save()
            return UpdateUser(ok=True, user=user)
        except Exception as e:
            print(str(e))
            return UpdateUser(ok=False, user=user_data)


class ChangePassword(Mutation):
    class Meta:
        name = "CreatePassword"
        description = "..."

    class Argunebts:
        password = String(required=True)

    ok = Boolean()
    auth = Field(lambda: TokenType)

    @staticmethod
    @fresh_jwt_required
    def mutate(root, info, password):
        user = UserModel.find_by_email(get_jwt_identity().email)

        if not user:
            return ChangePassword(ok=False)

        try:
            user.password = generate_password_hash(password, method="sha256")
            user.save()
            return ChangePassword(ok=True, auth=create_tokens(user))
        except Exception as e:
            print(str(e))
            return ChangePassword(ok=False)


class DeleteUser(Mutation):
    class Meta:
        name = "DeleteUser"
        description = "..."

    class Arguments:
        pass

    ok = Boolean()

    @staticmethod
    @fresh_jwt_required
    def mutate(root, info):
        user = UserModel.find_by_email(get_jwt_identity().email)

        if not user:
            return UpdateUser(ok=False)
        try:
            user.delete()
            return UpdateUser(ok=True)
        except Exception as e:
            print(str(e))
            return UpdateUser(ok=False)


######################################################################


class Signup(Mutation):
    class Meta:
        name = "Signup"
        description = "..."

    class Arguments:
        user_data = StrictUserInput(required=True)

    ok = Boolean()
    user = Field(lambda: UserType)
    auth = Field(lambda: TokenType)

    @staticmethod
    def mutate(root, info, user_data=None):
        if user_data:
            email_exists = UserModel.find_by_email(user_data.email)
            phone_number_exists = UserModel.find_by_phone_number(user_data.phone_number)

            if email_exists or phone_number_exists:
                return Signup(ok=False, user=user_data)

            user = UserModel(**user_data)

            try:
                user.password = generate_password_hash(user_data.password, method="sha256")
                user.save()
                ok = True
            except Exception as e:
                print(str(e))
                ok = False

            return Signup(ok=ok, user=user, auth=create_tokens(user))

        return Signup(ok=False, user=user_data)

