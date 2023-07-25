import pytest

from dotenv import dotenv_values
from werkzeug.security import generate_password_hash

from app import create_app
from app.db import AlchemyDatabase
from models import User, Group, Event, Base


@pytest.fixture
def db():
    env_test = dotenv_values(".env.test")

    class TestApp:
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

    Base.metadata.create_all(db.engine)

    yield db

    db.Session.remove()
    Base.metadata.drop_all(db.engine)


@pytest.fixture
def app(db):
    app = create_app(".env.test")
    app.db = db
    yield app


@pytest.fixture
def app_with_data(app):
    user1 = User(
        first_name="Filip",
        last_name="Nowak",
        email="FiliNowak@test.com",
        pass_hash=generate_password_hash("testPaswd11"),
    )
    user2 = User(
        first_name="Adam",
        last_name="Małysz",
        email="adam.malysz@test.com",
        pass_hash=generate_password_hash("testPaswd12"),
    )
    user3 = User(
        first_name="Julian",
        last_name="Nowak",
        email="julian.nowak@test.com",
        pass_hash=generate_password_hash("testPaswd13"),
    )

    app.db.Session.add_all([user1, user2, user3])
    app.db.Session.commit()

    yield app