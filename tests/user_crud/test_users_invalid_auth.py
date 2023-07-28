import json

from sqlalchemy import select

from models import User
from tests.conftest import valid_auth_header, expired_auth_header


def test_get_no_auth(app):
    resp = app.test_client().get(
        "/app/users/",
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "No Auth-Token Provided"


def test_patch_no_auth(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/users/2",
        data=json.dumps({"last_name": "Mały"}),
        content_type="application/json",
    )

    # response
    assert resp.status_code == 401
    assert resp.json["message"] == "No Auth-Token Provided"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_patch_random_auth(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/users/2",
        data=json.dumps({"last_name": "Mały"}),
        content_type="application/json",
        headers={"Authorization": "mdksa.sdaka.asdaf"},
    )

    # response
    assert resp.status_code == 401
    assert resp.json["message"] == "Invalid Token"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_get_expired(app):
    resp = app.test_client().get(
        "/app/users/",
        headers={"Authorization": expired_auth_header(1, app.config["SECRET_KEY_JWT"])},
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Expired Token"


def test_patch_expired(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/users/2",
        data=json.dumps({"first_name": "Adaś", "last_name": "Mały"}),
        content_type="application/json",
        headers={
            "Authorization": expired_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 401
    assert resp.json["message"] == "Expired Token"

    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_delete_expired(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/users/2",
        headers={
            "Authorization": expired_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))

    assert resp.status_code == 401
    assert resp.json["message"] == "Expired Token"
    assert not user.is_deleted
    assert user.deletion_date is None


def test_patch_different_id(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/users/2",
        data=json.dumps({"last_name": "Mały"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_delete_different_id(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/users/5",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"


def test_patch_expired_different_id(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/users/2",
        data=json.dumps({"last_name": "Mały"}),
        content_type="application/json",
        headers={
            "Authorization": expired_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 401
    assert resp.json["message"] == "Expired Token"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_get_user_deleted(app):
    resp = app.test_client().get(
        "/app/users/",
        headers={"Authorization": valid_auth_header(4, app.config["SECRET_KEY_JWT"])},
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Token Not Matching User"
