from flask import current_app
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import fields as rfields
from itsdangerous import URLSafeSerializer
from itsdangerous import BadSignature
from marshmallow import Schema
from marshmallow import validates
from marshmallow import fields
from marshmallow import validate
from marshmallow import ValidationError
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app import db
from app.email.verification import send_verification_email
from app.validation import validate_schema
from models import User

user_register_api = Namespace('app/users', description='Register user')


def create_token(user):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"])

    token = s.dumps({"id": user.id}, salt="activate")
    return token


def user_id_from_token(token):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"])

    try:
        dic = s.loads(token, salt="activate")
    except BadSignature as bs:
        return None

    return dic['id']


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


user_create = user_register_api.model('UserCreate', {
    'first_name': rfields.String,
    'last_name': rfields.String,
    'password': rfields.String,
    'email': rfields.String,
})


user_created = user_register_api.model('UserCreated', {
    'id': rfields.Integer,
    'first_name': rfields.String,
    'last_name': rfields.String,
    'email': rfields.String,
})


@user_register_api.route('/')
class Register(Resource):
    @user_register_api.expect(user_create)
    @user_register_api.marshal_with(user_created, code=201)
    @user_register_api.response(409, 'Already Exists')
    @validate_schema(user_register_api, UserCreateSchema)
    def post(self):
        session = db.Session()

        user_schema = UserCreateSchema().load(user_register_api.payload)

        # Query to check if user already exists
        user = session.scalar(select(User).where(User.email == user_schema['email']))

        if user:
            user_register_api.abort(409, "Already Exists")

        user = User(first_name=user_schema['first_name'],
                    last_name=user_schema['last_name'],
                    is_activated=False,
                    pass_hash=generate_password_hash(user_schema['password']),
                    email=user_schema['email'],
                    )

        session.add(user)
        session.commit()

        verification_url = f'http://127.0.0.1:5000/app/user/activate/{create_token(user)}'
        send_verification_email(user.email, verification_url)

        return user, 201


@user_register_api.route('/activate/<token>/')
class Activate(Resource):
    @user_register_api.response(200, 'Success')
    @user_register_api.response(400, "Invalid Token")
    def get(self, token):
        user_id = user_id_from_token(token)
        if not user_id:
            user_register_api.abort(400, "Invalid Token")

        session = db.Session()

        user = session.scalar(select(User).where(User.id == user_id))

        user.is_activated = True

        session.add(user)
        session.commit()

        return {'message': 'Success'}, 200
