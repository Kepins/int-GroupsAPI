from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.groups.marshmellow_schemas import GroupCreatePutSchema, GroupPatchSchema
from app.api.groups.namespace import api_groups
from app.api.groups.restx_models import group_create, group_created
from app.validation import validate_schema, validate_jwt
from models import User, Group


@api_groups.route("/")
class Groups(Resource):
    @api_groups.expect(group_create)
    @api_groups.response(201, "Success", group_created)
    @api_groups.response(409, "Admin Not Found")
    @validate_schema(api_groups, GroupCreatePutSchema)
    @validate_jwt(api_groups)
    def post(self, validated_schema, jwtoken_decoded):
        admin = db.Session.scalar(
            select(User).where(User.id == validated_schema["admin_id"])
        )

        if not admin or admin.is_deleted:
            api_groups.abort(409, "Admin Not Found")

        group = Group(
            name=validated_schema["name"],
            description=validated_schema.get("description"),
            admin=admin,
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
    @validate_schema(api_groups, GroupCreatePutSchema)
    @validate_jwt(api_groups)
    def put(self, id, validated_schema, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return {"message": "Not Found"}, 404

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message:": "Forbidden"}, 403

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
            return {"message:": "Forbidden"}, 403

        for key, value in validated_schema.items():
            setattr(group, key, value)

        db.Session.add(group)
        db.Session.commit()

        return api_groups.marshal(group, group_created)

    @api_groups.response(204, "No Content")
    @api_groups.response(403, "Forbidden")
    @validate_jwt(api_groups)
    def delete(self, id, jwtoken_decoded):
        group = db.Session.scalar(select(Group).where(Group.id == id))
        if not group:
            return None, 204

        if group.admin_id != jwtoken_decoded["id"]:
            return {"message:": "Forbidden"}, 403

        db.Session.delete(group)
        db.Session.commit()

        return None, 204
