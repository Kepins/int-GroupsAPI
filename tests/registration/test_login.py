import datetime
import json

from sqlalchemy import select

from models import User


def test_login_valid(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/users/login",
        data=json.dumps({"email": "FiliNowak@test.com", "password": "testPaswd11"}),
        content_type="application/json",
    )

    assert resp.status_code == 200


def test_login_invalid_password(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/users/login",
        data=json.dumps({"email": "FiliNowak@test.com", "password": "randomstring"}),
        content_type="application/json",
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Invalid Password"


def test_login_invalid_email(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/users/login",
        data=json.dumps({"email": "nonexistent@test.com", "password": "testPaswd11"}),
        content_type="application/json",
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "No Matching User"


def test_login_deleted(app_with_data):
    user = app_with_data.db.Session.scalar(
        select(User).where(User.email == "FiliNowak@test.com")
    )
    user.is_deleted = True
    user.deletion_date = datetime.datetime.utcnow()
    app_with_data.db.Session.add(user)
    app_with_data.db.Session.commit()

    resp = app_with_data.test_client().post(
        "/app/users/login",
        data=json.dumps({"email": "FiliNowak@test.com", "password": "testPaswd11"}),
        content_type="application/json",
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "User Deleted"
