from flask import Flask

from app.db import AlchemyDatabase
from app.config import Config

db = AlchemyDatabase()


def create_app(env=".env"):
    app = Flask(__name__)

    config = Config(env)
    app.config.from_object(config)

    db.init_app(app)

    from app.api import api_bp

    app.register_blueprint(api_bp)

    @app.after_request
    def after_request_func(response):
        db.Session.remove()
        return response

    return app
