import json

from sqlalchemy import select

from models import Group
from tests.conftest import valid_auth_header


def test_put_all_fields(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/groups/2",
        data=json.dumps({"name": "Group222", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_patch_one(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/groups/2",
        data=json.dumps({"name": "Group222"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_delete(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/groups/2",
        headers={
            "Authorization": valid_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1
