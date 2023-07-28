from flask_restx import fields

from app.api.events.namespace import api_events
from app.api.groups.restx_models import group_created

__event_common_fields = {
    "name": fields.String,
    "description": fields.String,
    "date": fields.DateTime,
}

event_create = api_events.model(
    "EventCreate",
    {
        "group_id": fields.Integer,
    }
    | __event_common_fields,
)

event_created = api_events.model(
    "EventCreated",
    {
        "id": fields.Integer,
        "group": fields.Nested(group_created),
    }
    | __event_common_fields,
)
