import pytest

from dotenv import dotenv_values
from sqlalchemy import delete, text

from app import create_app
from app.db import AlchemyDatabase
from models import User
from models import Group
from models import Event


@pytest.fixture
def db():
    env_test = dotenv_values(".env.test")

    class TestApp():
        config = {}
    app = TestApp()
    app.config = {
        "POSTGRES_USER": env_test["POSTGRESQL_USER"],
        "POSTGRES_PASSWD": env_test["POSTGRESQL_PASSWD"],
        "POSTGRES_HOSTNAME": env_test["POSTGRESQL_HOSTNAME"],
        "POSTGRES_DB_NAME": env_test["POSTGRESQL_DB_NAME"],
    }
    db = AlchemyDatabase()
    db.init_app(app)

    db.Session.execute(delete(Event))
    db.Session.execute(delete(Group))
    db.Session.execute(delete(User))
    db.Session.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1"))
    db.Session.execute(text("ALTER SEQUENCE group_id_seq RESTART WITH 1"))
    db.Session.execute(text("ALTER SEQUENCE event_id_seq RESTART WITH 1"))
    db.Session.commit()

    yield db

    db.Session.execute(delete(User))
    db.Session.execute(delete(Group))
    db.Session.execute(delete(Event))
    db.Session.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1"))
    db.Session.execute(text("ALTER SEQUENCE group_id_seq RESTART WITH 1"))
    db.Session.execute(text("ALTER SEQUENCE event_id_seq RESTART WITH 1"))
    db.Session.commit()

    db.Session.remove()


@pytest.fixture
def app(db):
    app = create_app(".env.test")
    app.db = db
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

