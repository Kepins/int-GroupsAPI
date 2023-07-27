from flask import url_for
from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.groups.marshmellow_schemas import (
    GroupCreatePutSchema,
    GroupPatchSchema,
    GroupInviteSchema,
)
from app.api.groups.namespace import api_groups
from app.api.groups.restx_models import group_create, group_created, group_invite
from app.email import EmailServiceError, send_invitation_email
from app.tokens.itsdangerous_tokens import (
    create_invitation_token,
    ids_from_invitation_token,
)
from app.validation import validate_schema, validate_jwt
from app.validation.existance import check_user_exists
from models import User, Group


@api_groups.route("/")
class Groups(Resource):
    @api_groups.expect(group_create)
    @api_groups.response(201, "Success", group_created)
    @api_groups.response(409, "Admin Not Found")
    @validate_schema(api_groups, GroupCreatePutSchema)
    @validate_jwt(api_groups)
    def post(self, validated_schema, jwtoken_decoded):
        if not check_user_exists(validated_schema["admin_id"]):
            return {"message": "Admin Not Found"}, 409

        group = Group(
            **validated_schema
        )

        db.Session.add(group)
        db.Session.commit()

        return api_groups.marshal(group, group_created), 201

    @api_groups.response(200, "Success", [group_created])
    @validate_jwt(api_groups)
    def get(self, jwtoken_decoded):
        groups = db.Session.scalars(select(Group))

        return [api_groups.marshal(group, group_created) for group in groups]


@api_groups.route("/<id>")
class GroupsByID(Resource):
    @api_groups.response(200, "Success", group_created)
    @api_groups.response(404, "Not found")
    @validate_jwt(api_groups)
    def get(self, id, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return {"message": "Not Found"}, 404
        return api_groups.marshal(group, group_created)

    @api_groups.expect(group_create)
    @api_groups.response(200, "Success", group_created)
    @api_groups.response(403, "Forbidden")
    @api_groups.response(404, "Not found")
    @api_groups.response(409, "Conflict")
    @validate_schema(api_groups, GroupCreatePutSchema)
    @validate_jwt(api_groups)
    def put(self, id, validated_schema, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return {"message": "Not Found"}, 404

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        if not check_user_exists(validated_schema["admin_id"]):
            return {"message": "New Admin Not Found"}, 409

        # iterate over every field (even NOT required)
        for key in GroupCreatePutSchema().fields.keys():
            value = validated_schema.get(key)
            setattr(group, key, value)

        db.Session.add(group)
        db.Session.commit()

        return api_groups.marshal(group, group_created)

    @api_groups.expect(group_create)
    @api_groups.response(200, "Success", group_created)
    @api_groups.response(403, "Forbidden")
    @api_groups.response(404, "Not found")
    @validate_schema(api_groups, GroupPatchSchema)
    @validate_jwt(api_groups)
    def patch(self, id, validated_schema, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return {"message": "Not Found"}, 404

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        if "admin_id" in validated_schema and not check_user_exists(
            validated_schema["admin_id"]
        ):
            return {"message": "New Admin Not Found"}, 409

        for key, value in validated_schema.items():
            setattr(group, key, value)

        db.Session.add(group)
        db.Session.commit()

        return api_groups.marshal(group, group_created)

    @api_groups.response(204, "No Content")
    @api_groups.response(403, "Forbidden")
    @api_groups.response(404, "Not Found")
    @validate_jwt(api_groups)
    def delete(self, id, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return None, 404

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        db.Session.delete(group)
        db.Session.commit()

        return None, 204


@api_groups.route("/<group_id>/invite")
class GroupsByIDInvite(Resource):
    @api_groups.expect(group_invite)
    @api_groups.response(200, "Success")
    @api_groups.response(404, "Not Found")
    @validate_schema(api_groups, GroupInviteSchema)
    @validate_jwt(api_groups)
    def post(self, group_id, validated_schema, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == group_id))
        if not group:
            return {"message": "Group Not Found"}, 404

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        if not check_user_exists(validated_schema["user_id"]):
            return {"message": "User Not Found"}, 404
        user = db.Session.scalar(
            select(User).where(User.id == validated_schema["user_id"])
        )

        invitation_link = url_for(
            "api_bp.app/groups_groups_invitations",
            _external=True,
            token=create_invitation_token(user, group),
        )

        try:
            send_invitation_email(user.email, invitation_link)
        except EmailServiceError(Exception):
            return {"message": "Email Service Down"}, 503, {"retry-after": "300"}

        return {"message": "Success"}, 200


@api_groups.route("/invitations/<token>")
class GroupsInvitations(Resource):
    def get(self, token):
        ids = ids_from_invitation_token(token)
        print(ids)
