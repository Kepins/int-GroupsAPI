from flask import Flask

from app.config import Config

config = Config()


def create_app():
    app = Flask(__name__)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app
