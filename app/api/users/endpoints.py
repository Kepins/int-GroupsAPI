from flask import url_for
from flask_restx import Resource
from werkzeug.security import generate_password_hash
from sqlalchemy import select

from models import User
from app import db
from app.api.users.tokens import user_id_from_token, create_token
from app.api.users.marshmellow_schemas import UserCreateSchema, UserPatchSchema
from app.api.users.namespace import api_users
from app.api.users.restx_models import user_create, user_created, user_patch
from app.email import send_verification_email, EmailServiceError
from app.validation import validate_schema


@api_users.route('/')
class Register(Resource):
    @api_users.expect(user_create)
    @api_users.response(201, "Success", user_created)
    @api_users.response(409, 'Already Exists')
    @api_users.response(503, 'Email Service Down')
    @validate_schema(api_users, UserCreateSchema)
    def post(self):
        user_schema = UserCreateSchema().load(api_users.payload)

        # Query to check if user already exists
        user = db.Session.scalar(select(User).where(User.email == user_schema['email']))

        if user:
            api_users.abort(409, "Already Exists")

        user = User(first_name=user_schema['first_name'],
                    last_name=user_schema['last_name'],
                    is_activated=False,
                    pass_hash=generate_password_hash(user_schema['password']),
                    email=user_schema['email'],
                    )

        db.Session.add(user)
        db.Session.commit()
        verification_url = url_for("api_bp.app/users_activate", _external=True, token=create_token(user))
        try:
            send_verification_email(user.email, verification_url)
        except EmailServiceError as e:
            db.Session.delete(user)
            db.Session.commit()
            return {"message": "Email Service Down"}, 503, {"retry-after": "300"}

        return api_users.marshal(user, user_created), 201

    @api_users.response(200, "Success",  [user_created])
    def get(self):
        users = db.Session().scalars(select(User)).all()

        return [api_users.marshal(user, user_created) for user in users]
    
    
@api_users.route('/activate/<token>/')
class Activate(Resource):
    @api_users.response(200, 'Success')
    @api_users.response(400, "Invalid Token")
    def get(self, token):
        user_id = user_id_from_token(token)
        if not user_id:
            api_users.abort(400, "Invalid Token")

        user = db.Session.scalar(select(User).where(User.id == user_id))

        user.is_activated = True

        db.Session.add(user)
        db.Session.commit()

        return {'message': 'Success'}, 200


@api_users.route('/<id>')
class Id(Resource):

    @api_users.response(200, "Success", user_created)
    @api_users.response(404, "Not found")
    def get(self, id):
        user = db.Session.scalar(select(User).where(User.id == id))
        if not user:
            return {'message': 'Not found'}, 404
        return api_users.marshal(user, user_created)

    @api_users.expect(user_patch)
    @api_users.response(200, "Success", user_created)
    @api_users.response(404, "Not found")
    @validate_schema(api_users, UserPatchSchema)
    def patch(self, id):
        user_patch_schema = UserPatchSchema().load(api_users.payload)

        user = db.Session.scalar(select(User).where(User.id == id))
        if not user:
            return {'message': 'Not found'}, 404

        for key, value in user_patch_schema.items():
            setattr(user, key, value)

        db.Session.add(user)
        db.Session.commit()

        return api_users.marshal(user, user_created), 200
