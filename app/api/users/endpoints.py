import datetime

from flask import url_for
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

from models import User
from app import db
from app.api.users.itsdangerous_tokens import user_id_from_token, create_token
from app.api.users.marshmellow_schemas import (
    UserCreateSchema,
    UserPatchSchema,
    UserLoginSchema,
)
from app.api.users.namespace import api_users
from app.api.users.restx_models import user_create, user_created, user_patch, user_login
from app.email import send_verification_email, EmailServiceError
from app.validation import validate_schema, validate_jwt
from app.api.users.jwt_tokens import jwt_token


@api_users.route("/")
class Users(Resource):
    @api_users.expect(user_create)
    @api_users.response(201, "Success", user_created)
    @api_users.response(409, "Already Exists")
    @api_users.response(503, "Email Service Down")
    @validate_schema(api_users, UserCreateSchema)
    def post(self):
        user_schema = UserCreateSchema().load(api_users.payload)

        # Query to check if user already exists
        user = db.Session.scalar(select(User).where(User.email == user_schema["email"]))

        if user:
            api_users.abort(409, "Already Exists")

        user = User(
            first_name=user_schema["first_name"],
            last_name=user_schema["last_name"],
            is_activated=False,
            pass_hash=generate_password_hash(user_schema["password"]),
            email=user_schema["email"],
        )

        db.Session.add(user)
        db.Session.commit()
        verification_url = url_for(
            "api_bp.app/users_users_activate", _external=True, token=create_token(user)
        )
        try:
            send_verification_email(user.email, verification_url)
        except EmailServiceError as e:
            db.Session.delete(user)
            db.Session.commit()
            return {"message": "Email Service Down"}, 503, {"retry-after": "300"}

        return api_users.marshal(user, user_created), 201

    @api_users.response(200, "Success", [user_created])
    @validate_jwt(api_users)
    def get(self, jwtoken_decoded):
        users = db.Session().scalars(select(User)).all()

        return [api_users.marshal(user, user_created) for user in users]


@api_users.route("/activate/<token>/")
class UsersActivate(Resource):
    @api_users.response(200, "Success")
    @api_users.response(400, "Invalid Token")
    def get(self, token):
        user_id = user_id_from_token(token)
        if not user_id:
            api_users.abort(400, "Invalid Token")

        user = db.Session.scalar(select(User).where(User.id == user_id))

        user.is_activated = True

        db.Session.add(user)
        db.Session.commit()

        return {"message": "Success"}, 200


@api_users.route("/<id>")
class UsersByID(Resource):
    @api_users.response(200, "Success", user_created)
    @api_users.response(404, "Not Found")
    @validate_jwt(api_users)
    def get(self, id, jwtoken_decoded):
        user = db.Session.scalar(select(User).where(User.id == id))
        if not user:
            return {"message": "Not Found"}, 404
        return api_users.marshal(user, user_created)

    @api_users.expect(user_patch)
    @api_users.response(200, "Success", user_created)
    @api_users.response(404, "Not Found")
    @validate_schema(api_users, UserPatchSchema)
    @validate_jwt(api_users)
    def patch(self, id, jwtoken_decoded):
        user_patch_schema = UserPatchSchema().load(api_users.payload)

        user = db.Session.scalar(select(User).where(User.id == id))
        if not user:
            return {"message": "Not Found"}, 404

        for key, value in user_patch_schema.items():
            setattr(user, key, value)

        db.Session.add(user)
        db.Session.commit()

        return api_users.marshal(user, user_created), 200

    @api_users.response(204, "No Content")
    @validate_jwt(api_users)
    def delete(self, id, jwtoken_decoded):
        user = db.Session.scalar(select(User).where(User.id == id))
        if not user or user.is_deleted:
            return None, 204

        user.is_deleted = True
        user.deletion_date = datetime.datetime.utcnow()
        db.Session.add(user)
        db.Session.commit()

        return None, 204


@api_users.route("/login")
class Login(Resource):
    @api_users.expect(user_login)
    @api_users.response(200, "Success")
    @api_users.response(401, "Unauthorized")
    @validate_schema(api_users, UserLoginSchema)
    def post(self):
        user_login_schema = UserLoginSchema().load(api_users.payload)

        user_db = db.Session.scalar(
            select(User).where(User.email == user_login_schema["email"])
        )

        if not user_db:
            return {"message": "No Matching User"}, 401
        if user_db.is_deleted:
            return {"message": "User Deleted"}, 401
        if not check_password_hash(user_db.pass_hash, user_login_schema["password"]):
            return {"message": "Invalid Password"}, 401

        return jwt_token(user_db), 200
