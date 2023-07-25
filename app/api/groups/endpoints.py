from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.groups.marshmellow_schemas import GroupCreateSchema
from app.api.groups.namespace import api_groups
from app.api.groups.restx_models import group_create, group_created
from app.validation import validate_schema
from models import User


@api_groups.route("/")
class Groups(Resource):
    @api_groups.expect(group_create)
    @api_groups.response(201, "Success", group_created)
    @api_groups.response(409, "Admin Not Found")
    @validate_schema(api_groups, GroupCreateSchema)
    def post(self, validated_schema):
        pass

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
