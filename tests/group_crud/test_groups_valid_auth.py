import json

from sqlalchemy import select

from models import Group
from tests.conftest import valid_auth_header


def test_post_wrong_fields(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_idd": 3, "name": "group5", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 400
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 5))
    assert group is None


def test_post_all_fields(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_id": 3, "name": "group5", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 201
    assert resp.json["id"] == 5
    assert resp.json["name"] == "group5"
    assert resp.json["description"] == "descr"
    assert resp.json["admin"]["id"] == 3
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 5))
    assert group.name == "group5"
    assert group.description == "descr"
    assert group.admin_id == 3


def test_post_required_fields(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_id": 3, "name": "group5"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 201
    assert resp.json["id"] == 5
    assert resp.json["name"] == "group5"
    assert resp.json["description"] is None
    assert resp.json["admin"]["id"] == 3
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 5))
    assert group.name == "group5"
    assert group.description is None
    assert group.admin_id == 3


def test_post_create_for_deleted_user(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_id": 4, "name": "group5"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "Admin Not Found"


def test_post_create_for_nonexistent_user(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/",
        data=json.dumps({"admin_id": 99, "name": "group5"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "Admin Not Found"


def test_get_exists(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/groups/",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json[1]["id"] == 2
    assert resp.json[1]["name"] == "group2"
    assert resp.json[1]["description"] == "This is group2"
    assert resp.json[1]["admin"]["id"] == 1
    assert len(resp.json) == 4


def test_get_id_not_exist(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/groups/7",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404


def test_get_id_exists(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/groups/2",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert "name" in resp.json


def test_put_all_fields(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/groups/2",
        data=json.dumps({"admin_id": 1, "name": "Group222", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["name"] == "Group222"
    assert resp.json["description"] == "descr"
    assert resp.json["admin"]["id"] == 1

    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "Group222"
    assert group.description == "descr"
    assert group.admin_id == 1


def test_put_required_field(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/groups/2",
        data=json.dumps({"name": "Group222", "admin_id": 2}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["name"] == "Group222"
    assert resp.json["description"] is None
    assert resp.json["admin"]["id"] == 2

    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "Group222"
    assert group.description is None
    assert group.admin_id == 2


def test_patch_all_fields(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/groups/2",
        data=json.dumps({"admin_id": 3, "name": "Group222", "description": "descr"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["name"] == "Group222"
    assert resp.json["description"] == "descr"
    assert resp.json["admin"]["id"] == 3

    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "Group222"
    assert group.description == "descr"
    assert group.admin_id == 3


def test_patch_one_field(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/groups/2",
        data=json.dumps({"name": "Group222"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["name"] == "Group222"
    assert resp.json["description"] == "This is group2"
    assert resp.json["admin"]["id"] == 1

    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "Group222"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_patch_wrong_admin(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/groups/2",
        data=json.dumps({"admin_id": 99, "name": "Group222"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 409
    assert resp.json["message"] == "New Admin Not Found"
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_patch_wrong_field(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/groups/2",
        data=json.dumps({"frst_name": "Jacek", "last_name": "Mały"}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 400
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group.name == "group2"
    assert group.description == "This is group2"
    assert group.admin_id == 1


def test_delete_exists(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/groups/2",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 204
    # db
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 2))
    assert group is None
