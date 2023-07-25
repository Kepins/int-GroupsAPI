from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature


def create_token(user):
    s = URLSafeSerializer(current_app.config["SECRET_DAN"])

    token = s.dumps({"id": user.id}, salt="activate")
    return token


def user_id_from_token(token):
    s = URLSafeSerializer(current_app.config["SECRET_DAN"])

    try:
        dic = s.loads(token, salt="activate")
    except BadSignature as bs:
        return None

    return dic["id"]
