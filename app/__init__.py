from flask import Flask
from flask_restx import Api

api = Api()


def create_app():
    app = Flask(__name__)

    api.init_app(app)

    from app.rest_api import rest_api_bp
    app.register_blueprint(rest_api_bp)

    return app
