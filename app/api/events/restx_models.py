from flask_restx import fields

from app.api.events.namespace import api_events
from app.api.groups.restx_models import group_created

event_create = api_events.model(
    "EventCreate",
    {
        "group_id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "date": fields.DateTime,
    },
)

event_created = api_events.model(
    "EventCreated",
    {
        "id": fields.Integer,
        "group": fields.Nested(group_created),
        "name": fields.String,
        "description": fields.String,
        "date": fields.DateTime,
    },
)
