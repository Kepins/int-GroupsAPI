from flask_restx import fields

from app.api.users.namespace import api_users

user_names = api_users.model(
    "UserNames",
    {
        "first_name": fields.String,
        "last_name": fields.String,
    },
)

user_create = api_users.inherit(
    "UserCreate",
    user_names,
    {
        "password": fields.String,
        "email": fields.String,
    },
)


user_created = api_users.inherit(
    "UserCreated",
    user_names,
    {
        "id": fields.Integer,
        "email": fields.String,
    },
)

user_patch = api_users.inherit("UserPatch", user_names, {})

user_login = api_users.model(
    "UserLogin",
    {
        "email": fields.String,
        "password": fields.String,
    },
)
