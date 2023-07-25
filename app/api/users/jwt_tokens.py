import jwt

from datetime import datetime, timedelta

from flask import current_app


def jwt_token(user):
    token_info = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    secret = current_app.config["SECRET_JWT"]

    return jwt.encode(token_info, secret, algorithm="HS256")
