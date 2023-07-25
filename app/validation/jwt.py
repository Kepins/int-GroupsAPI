import functools

import jwt

from flask import current_app, request
from flask_restx import Namespace

import re


def validate_jwt(api: Namespace):
    def decorator_validate(func):
        @api.response(401, "Unauthorized")
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if auth_header is None:
                api.abort(401, "No Auth-Token Provided")
            if re.compile(
                "^Bearer [a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$"
            ).match(auth_header):
                jwtoken_encoded = auth_header[7:]
            else:
                jwtoken_encoded = ""
            try:
                jwtoken_decoded = jwt.decode(
                    jwtoken_encoded,
                    current_app.config["SECRET_JWT"],
                    algorithms=["HS256"],
                )
            except jwt.ExpiredSignatureError:
                api.abort(401, "Expired Token")
            except jwt.exceptions.InvalidTokenError:
                api.abort(401, "Invalid Token")

            return func(*args, **kwargs, jwtoken_decoded=jwtoken_decoded)

        return wrapper_validate

    return decorator_validate


def validate_jwt_id_matches_id(api: Namespace):
    def decorator_validate(func):
        @api.response(401, "Unauthorized")
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):
            id = kwargs.get("id")
            jwtoken_decoded = kwargs.get("jwtoken_decoded")
            if id != str(jwtoken_decoded["id"]):
                api.abort(401, "Id Not Matching")
            return func(*args, **kwargs)

        return wrapper_validate

    return decorator_validate
