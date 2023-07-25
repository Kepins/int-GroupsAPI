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
