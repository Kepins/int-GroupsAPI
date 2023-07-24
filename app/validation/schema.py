import functools

from flask_restx import Namespace
from marshmallow import Schema, ValidationError


def validate_schema(api: Namespace, schema: type[Schema]):
    def decorator_validate(func):
        @api.response(400, "Validation Error")
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):
            payload = api.payload
            try:
                schema().load(payload)
            except ValidationError as err:
                api.abort(400, err.messages)
            return func(*args, **kwargs)

        return wrapper_validate

    return decorator_validate
