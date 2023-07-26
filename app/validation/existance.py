from sqlalchemy import select

from app import db
from models import User


def check_user_exists(id):
    user = db.Session.scalar(select(User).where(User.id == id))
    if not user or user.is_deleted:
        return False
    return True
