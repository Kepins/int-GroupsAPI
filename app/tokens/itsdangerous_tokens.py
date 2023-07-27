from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature
from sqlalchemy import select

from app import db
from models import User


def create_activation_token(user):
    s = URLSafeSerializer(current_app.config["SECRET_KEY_ITSDANGEROUS"])

    token = s.dumps({"id": user.id}, salt="activate")
    return token


def user_id_from_activation_token(token):
    s = URLSafeSerializer(current_app.config["SECRET_KEY_ITSDANGEROUS"])

    try:
        dic = s.loads(token, salt="activate")
    except BadSignature as bs:
        return None

    return dic["id"]


def user_from_activation_token(token):
    return db.Session.scalar(
        select(User).where(User.id == user_id_from_activation_token(token))
    )


def create_invitation_token(user, group):
    s = URLSafeSerializer(current_app.config["SECRET_KEY_ITSDANGEROUS"])

    token = s.dumps({"user_id": user.id, "group_id": group.id}, salt="invite")
    return token


def ids_from_invitation_token(token):
    s = URLSafeSerializer(current_app.config["SECRET_KEY_ITSDANGEROUS"])

    try:
        dic = s.loads(token, salt="invite")
    except BadSignature as bs:
        return None

    return dic
