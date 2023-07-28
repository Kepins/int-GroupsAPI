from flask_restx import fields

from app.api.events.restx_models import event_created
from app.api.groups.restx_models import group_created
from app.api.profile.namespace import api_profile
from app.api.users.restx_models import user_created

profile_get = api_profile.inherit(
    "ProfileGet",
    user_created,
    {
        "groups": fields.List(fields.Nested(group_created)),
        "events": fields.List(fields.Nested(event_created)),
    },
)
