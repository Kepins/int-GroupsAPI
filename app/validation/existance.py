from sqlalchemy import exists, and_, not_

from app import db
from models import User


def check_user_exists(id):
    return db.Session.query(
        exists(User).where(and_(User.id == id, not_(User.is_deleted)))
    ).scalar()
