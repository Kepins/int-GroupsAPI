import json
from unittest.mock import patch, MagicMock

from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from models import User


def test_registration_not_valid_not_json(app, client):
    resp = client.post("/app/users/",
                       data={"first_name": "Jacek", "last_name": "Placek",
                             "email": "jacek@test.com", "password": "testPaswd1"},
                       )
    assert resp.status_code == 415  # UNSUPPORTED MEDIA TYPE


def test_registration_not_valid_field_missing(app, client):
    resp = client.post("/app/users/",
                       data=json.dumps({"first_name": "Jacek", "email": "jacek@test.com", "password": "testPaswd1"}),
                       content_type='application/json')

    assert resp.text == '{"message": "{\'last_name\': [\'Missing data for required field.\']}"}\n'
    assert resp.status_code == 400  # INVALID REQUEST


def test_registration_already_exists(app, client):
    user = User(first_name="Filip", last_name="Nowak",
                email="FiliNowak@test.com", pass_hash=generate_password_hash("testPaswd1"))
    app.db.Session.add(user)
    app.db.Session.commit()
    resp = client.post("/app/users/",
                       data=json.dumps({"first_name": "Flipek", "last_name": "Nowak",
                                        "email": "FiliNowak@test.com", "password": "testPaswd2"}),
                       content_type='application/json')

    assert resp.status_code == 409
    assert resp.json["message"] == "Already Exists"


def test_register_email_service_down(app, client):
    app.config["SMTP_SERVER"] = ""
    app.config["SMTP_PORT"] = 0

    resp = client.post("/app/users/",
                       data=json.dumps({"first_name": "Flipek", "last_name": "Nowak",
                                        "email": "FiliNowak@test.com", "password": "testPaswd2"}),
                       content_type='application/json')

    assert resp.status_code == 503
    assert app.db.Session.scalar(select(User).where(User.email == "FiliNowak@test.com")) is None
    assert resp.headers["retry-after"] == "300"


def test_registration_valid(app, client):
    with patch("app.api.register.send_verification_email", MagicMock()) as mail_mock:
        resp = client.post("/app/users/",
                           data=json.dumps({"first_name": "Jacek", "last_name": "Placek",
                                 "email": "jacek@test.com", "password": "testPaswd1"}),
                           content_type='application/json')

        db_user = app.db.Session.scalar(select(User).where(User.email == "jacek@test.com"))
        app.db.Session.remove()

        # Response
        assert resp.status_code == 201
        assert resp.json["id"] == 1
        assert resp.json["first_name"] == "Jacek"
        assert resp.json["last_name"] == "Placek"
        assert resp.json["email"] == "jacek@test.com"
        # Database
        assert db_user is not None
        assert db_user.first_name == "Jacek"
        assert db_user.last_name == "Placek"
        assert check_password_hash(db_user.pass_hash, "testPaswd1")
        assert not db_user.is_activated
        # Email
        mail_mock.assert_called_once()
        assert mail_mock.call_args[0][0] == "jacek@test.com"

        # Request to activation URL

        url_activate = mail_mock.call_args[0][1]
        resp_activate = client.get(url_activate)

        db_user = app.db.Session.scalar(select(User).where(User.email == "jacek@test.com"))
        app.db.Session.remove()

        assert resp_activate.status_code == 200
        assert db_user.is_activated


def test_activate_invalid_token(app, client):
    token = "not_valid_token"
    resp = client.get(f"app/users/activate/{token}/")

    assert resp.status_code == 400
