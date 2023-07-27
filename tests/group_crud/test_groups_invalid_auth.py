import json

from sqlalchemy import select

from models import Group
from tests.conftest import valid_auth_header, expired_auth_header


def test_post_user_deleted(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_id": 3, "name": "group5", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                4, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Token Not Matching User"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 5))
    assert group is None


def test_delete_user_deleted(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/groups/2",
        headers={
            "Authorization": valid_auth_header(
                99, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Token Not Matching User"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_delete(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/groups/2",
        headers={
            "Authorization": expired_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 401
    assert resp.json["message"] == "Expired Token"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1
