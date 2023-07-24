import json

from sqlalchemy import select

from models import User


def test_get_empty(app):
    resp = app.test_client().get("/app/users/")

    assert resp.status_code == 200
    assert resp.json == []  # empty list


def test_get_exists(app_with_data):
    resp = app_with_data.test_client().get("/app/users/")

    assert resp.status_code == 200
    assert resp.json[1]["id"] == 2
    assert resp.json[1]["email"] == 'adam.malysz@test.com'
    assert resp.json[1]["first_name"] == "Adam"
    assert resp.json[1]["last_name"] == "Małysz"
    assert len(resp.json) == 3


def test_get_id_not_exist(app):
    resp = app.test_client().get("/app/users/2")

    assert resp.status_code == 404


def test_get_id_exists(app_with_data):
    resp = app_with_data.test_client().get("/app/users/2")

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["email"] == 'adam.malysz@test.com'
    assert resp.json["first_name"] == "Adam"
    assert resp.json["last_name"] == "Małysz"


def test_patch_all_fields(app_with_data):
    resp = app_with_data.test_client().patch("/app/users/2",
                                             data=json.dumps({"first_name": "Adaś", "last_name": "Mały"}),
                                             content_type='application/json')

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["email"] == 'adam.malysz@test.com'
    assert resp.json["first_name"] == "Adaś"
    assert resp.json["last_name"] == "Mały"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adaś"
    assert user.last_name == "Mały"


def test_patch_one_field(app_with_data):
    resp = app_with_data.test_client().patch("/app/users/2",
                                             data=json.dumps({"last_name": "Mały"}),
                                             content_type='application/json')

    # response
    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["email"] == 'adam.malysz@test.com'
    assert resp.json["first_name"] == "Adam"
    assert resp.json["last_name"] == "Mały"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Mały"


def test_patch_wrong_field(app_with_data):
    resp = app_with_data.test_client().patch("/app/users/2",
                                             data=json.dumps({"frst_name": "Jacek", "last_name": "Mały"}),
                                             content_type='application/json')

    assert resp.status_code == 400
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))
    assert user.first_name == "Adam"
    assert user.last_name == "Małysz"


def test_delete_not_exists(app_with_data):
    resp = app_with_data.test_client().delete("/app/users/5")

    assert resp.status_code == 204
    assert resp.data == b''


def test_delete_exists(app_with_data):
    resp = app_with_data.test_client().delete("/app/users/2")

    user = app_with_data.db.Session.scalar(select(User).where(User.id == 2))

    assert resp.status_code == 204
    assert resp.data == b''
    assert user.is_deleted
    assert user.deletion_date is not None
