from flask import Blueprint

rest_api_bp = Blueprint('rest_api', __name__)
from app.rest_api import status
