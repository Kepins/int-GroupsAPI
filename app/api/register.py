import os

from dotenv import load_dotenv
from flask_restx import Resource
from flask_restx import Namespace
from itsdangerous import URLSafeSerializer
from itsdangerous import BadSignature
from marshmallow import Schema
from marshmallow import validates
from marshmallow import fields
from marshmallow import validate
from marshmallow import ValidationError
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.db import Session
from app.email.verification import send_verification_email
from app.validation import validate_schema
from models import User

user_register_api = Namespace('app/user', description='Register user')


def create_token(user):
    load_dotenv()
    s = URLSafeSerializer(os.environ.get("SECRET_KEY"))

    token = s.dumps({"id": user.id}, salt="activate")
    return token


def user_id_from_token(token):
    load_dotenv()
    s = URLSafeSerializer(os.environ.get("SECRET_KEY"))

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


@user_register_api.route('/')
class Register(Resource):
    @validate_schema(user_register_api, UserCreateSchema)
    def post(self):
        session = Session()

        user_schema = UserCreateSchema().load(user_register_api.payload)

        # Query to check if user already exists
        user = session.execute(select(User)
                               .where(User.email == user_schema['email'])
                               ).first()

        if user:
            return {'error': 'already_exists'}, 403

        user = User(first_name=user_schema['first_name'],
                    last_name=user_schema['last_name'],
                    is_activated=False,
                    pass_hash=generate_password_hash(user_schema['password']),
                    email=user_schema['email'],
                    )

        session.add(user)
        session.commit()
        Session.remove()

        verification_url = f'http://127.0.0.1:5000/app/user/activate/{create_token(user)}'
        send_verification_email(user.email, verification_url)

        return {'id': user.id}, 201
