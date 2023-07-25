from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.groups.marshmellow_schemas import GroupCreateSchema
from app.api.groups.namespace import api_groups
from app.api.groups.restx_models import group_create, group_created
from app.validation import validate_schema
from models import User, Group


@api_groups.route("/")
class Groups(Resource):
    @api_groups.expect(group_create)
    @api_groups.response(201, "Success", group_created)
    @api_groups.response(409, "Admin Not Found")
    @validate_schema(api_groups, GroupCreateSchema)
    def post(self, validated_schema):
        admin = db.Session.scalar(select(User).where(User.id == validated_schema["admin_id"]))

        if not admin or admin.is_deleted:
            api_groups.abort(409, "Admin Not Found")

        group = Group(
            name=validated_schema["name"],
            description=validated_schema.get("description"),
            admin=admin
        )

        db.Session.add(group)
        db.Session.commit()

        return api_groups.marshal(group, group_created), 201

    def get(self):
        pass


@api_groups.route("/<id>")
class GroupsByID(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass
