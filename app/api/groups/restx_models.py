from flask_restx import fields

from app.api.groups.namespace import api_groups
from app.api.users.restx_models import user_created

group_create = api_groups.model(
    "GroupCreate",
    {
        "admin_id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
    },
)

group_created = api_groups.model(
    "GroupCreated",
    {
        "id": fields.Integer,
        "admin": fields.Nested(user_created),
        "name": fields.String,
        "description": fields.String,
    },
)

group_invite = api_groups.model("GroupInvite", {"user_id": fields.Integer})
