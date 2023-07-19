import functools

from flask_restx import Namespace
from marshmallow import Schema
from marshmallow import ValidationError


def validate_schema(api: Namespace, schema: type[Schema]):
    def decorator_validate(func):
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):
            payload = api.payload
            try:
                schema().load(payload)
            except ValidationError as err:
                return err.messages, 400
            return func(*args, **kwargs)
        return wrapper_validate
    return decorator_validate
