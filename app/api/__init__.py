from flask import Blueprint
from flask_restx import Api

from .events import api_events
from .groups import api_groups
from .profile import api_profile
from .status import api_status
from .users import api_users

api_bp = Blueprint("api_bp", __name__)

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}

api = Api(
    api_bp,
    title="GroupAPP",
    version="1.0",
    authorizations=authorizations,
    security="apikey",
)

api.add_namespace(api_status)
api.add_namespace(api_users)
api.add_namespace(api_groups)
api.add_namespace(api_events)
api.add_namespace(api_profile)
