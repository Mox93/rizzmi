from app import jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from graphene import ObjectType, String


class TokenType(ObjectType):
    class Meta:
        name = "Token"
        description = "..."

    access_token = String()
    refresh_token = String()


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {"creation_date": int(user.creation_date.timestamp()),
            "mode": "testing"}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {  # "_id": str(user._id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name}


def create_tokens(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=1), fresh=True)
    refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=30))

    return TokenType(access_token=access_token, refresh_token=refresh_token)


def create_fresh_token(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=1), fresh=True)
    return TokenType(access_token=access_token)


def refresh_access_token(user):
    new_token = create_access_token(identity=user, expires_delta=timedelta(minutes=10), fresh=False)
    return TokenType(access_token=new_token)

