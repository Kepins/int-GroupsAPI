import datetime

import jwt
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
    user4 = User(
        first_name="Janusz",
        last_name="Kowal",
        email="kowal.janek@test.com",
        pass_hash=generate_password_hash("testPaswd14"),
    )
    user4.is_deleted = True
    user4.deletion_date = datetime.datetime.utcnow()

    group1 = Group(
        admin=user1,
        name="group1",
    )
    group2 = Group(
        admin=user1,
        name="group2",
        description="This is group2",
    )
    group3 = Group(
        name="group3",
        description="This is group2",
    )
    group4 = Group(
        name="group4",
        description="This is group2",
        admin=user3,
    )

    app.db.Session.add_all([user1, user2, user3, user4])
    app.db.Session.commit()

    group1.users.append(user1)
    group2.users.append(user1)
    group2.users.append(user2)
    group2.users.append(user3)

    app.db.Session.add_all([group1, group2, group3, group4])
    app.db.Session.commit()

    event1 = Event(
        name="event1",
        description="Descr1",
        group=group2,
        date=datetime.datetime.utcnow(),
    )

    event2 = Event(
        name="event2",
        description="Descr2",
        group=group2,
        date=datetime.datetime.utcnow(),
    )

    event3 = Event(
        name="event3",
        group=group4,
        date=datetime.datetime.utcnow(),
    )

    app.db.Session.add_all([event1, event2, event3])
    app.db.Session.commit()

    yield app


def valid_auth_header(id, secret):
    return "Bearer " + jwt.encode(
        {"id": id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        secret,
        algorithm="HS256",
    )


def expired_auth_header(id, secret):
    return "Bearer " + jwt.encode(
        {"id": id, "exp": datetime.datetime.utcnow() - datetime.timedelta(minutes=2)},
        secret,
        algorithm="HS256",
    )
