from flask_restx import Resource
from flask_restx import Namespace
from marshmallow import Schema
from marshmallow import validates
from marshmallow import fields
from marshmallow import validate
from marshmallow import ValidationError

from app.validation import validate_schema


user_register_api = Namespace('app/user', description='Register user')


class UserCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(1))
    last_name = fields.Str(required=True, validate=validate.Length(1))
    password = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email())

    @validates("password")
    def validate_password(self, passwd: str):
        if len(passwd) < 8:
            raise ValidationError("Shorter than minimum length 8.")
        if not any(ch.islower() for ch in passwd):
            raise ValidationError("Must contain at least one lowercase letter.")
        if not any(ch.isupper() for ch in passwd):
            raise ValidationError("Must contain at least one uppercase letter.")
        if not any(ch.isdigit() for ch in passwd):
            raise ValidationError("Must contain at least one digit.")


@user_register_api.route('/')
class Register(Resource):
    @validate_schema(user_register_api, UserCreateSchema)
    def post(self):
        user_schema = UserCreateSchema().load(user_register_api.payload)
        return {'status': 'ok'}, 201
