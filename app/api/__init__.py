from flask import Blueprint
from flask_restx import Api

from .status import api_status as api_status
from .users import api_users as api_users

api_bp = Blueprint("api_bp", __name__)

api = Api(
    api_bp,
    title="API",
    version="0.1",
)

api.add_namespace(api_status)
api.add_namespace(api_users)
