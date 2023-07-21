from flask import Blueprint
from flask_restx import Api

from .status import status_api as status_api
from .register import user_register_api as user_register_api

api_bp = Blueprint('api_bp', __name__)

api = Api(
    api_bp,
    title='API',
    version='0.1',
)

api.add_namespace(status_api)
api.add_namespace(user_register_api)
