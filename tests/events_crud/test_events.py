import datetime
import json

from sqlalchemy import select

from models import Event
from tests.conftest import valid_auth_header

date_str = "2023-07-27T14:01:16.497000"
date_datetime = datetime.datetime(2023, 7, 27, 14, 1, 16, 497000)


def test_post_created(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/events/",
        data=json.dumps(
            {
                "group_id": 2,
                "name": "event3",
                "description": "event3descr",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 201
    assert resp.json["group"]["id"] == 2
    assert resp.json["group"]["admin"]["id"] == 1
    assert resp.json["name"] == "event3"
    assert resp.json["description"] == "event3descr"
    assert resp.json["date"] == date_str
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 4))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event3"
    assert event_db.description == "event3descr"
    assert event_db.date == date_datetime


def test_post_created_not_all_fields(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/events/",
        data=json.dumps({"group_id": 2, "name": "event3", "date": date_str}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 201
    assert resp.json["group"]["id"] == 2
    assert resp.json["group"]["admin"]["id"] == 1
    assert resp.json["name"] == "event3"
    assert resp.json["description"] is None
    assert resp.json["date"] == date_str
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 4))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event3"
    assert event_db.description is None
    assert event_db.date == date_datetime


def test_post_group_not_found(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/events/",
        data=json.dumps({"group_id": 99, "name": "event3", "date": date_str}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "Group Not Found"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 4))
    assert not event_db


def test_post_forbidden(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/events/",
        data=json.dumps({"group_id": 4, "name": "event3", "date": date_str}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Group Does Not Belong To Requester"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 4))
    assert not event_db


def test_get_all(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/events/",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )
    assert resp.status_code == 200
    assert len(resp.json) == 2


def test_put_not_all_fields(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/events/1",
        data=json.dumps({"group_id": 1, "name": "event11", "date": date_str}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json["group"]["id"] == 1
    assert resp.json["group"]["admin"]["id"] == 1
    assert resp.json["name"] == "event11"
    assert resp.json["description"] is None
    assert resp.json["date"] == date_str
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 1
    assert event_db.group.admin.id == 1
    assert event_db.name == "event11"
    assert event_db.description is None
    assert event_db.date == date_datetime


def test_put_all_fields(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 1,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json["group"]["id"] == 1
    assert resp.json["group"]["admin"]["id"] == 1
    assert resp.json["name"] == "event11"
    assert resp.json["description"] == "event1descr"
    assert resp.json["date"] == date_str
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 1
    assert event_db.group.admin.id == 1
    assert event_db.name == "event11"
    assert event_db.description == "event1descr"
    assert event_db.date == date_datetime


def test_put_forbidden(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 2,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_put_new_group_not_exists(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 99,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "New Group Not Found"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_put_new_group_not_owned(app_with_data):
    resp = app_with_data.test_client().put(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 4,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "New Group Does Not Belong To Requester"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_patch_not_all_fields(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/events/2",
        data=json.dumps({"group_id": 1, "name": "event11", "date": date_str}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json["group"]["id"] == 1
    assert resp.json["group"]["admin"]["id"] == 1
    assert resp.json["name"] == "event11"
    assert resp.json["description"] == "Descr2"
    assert resp.json["date"] == date_str
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 2))
    assert event_db.group.id == 1
    assert event_db.group.admin.id == 1
    assert event_db.name == "event11"
    assert event_db.description == "Descr2"
    assert event_db.date == date_datetime


def test_patch_forbidden(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 2,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_patch_new_group_not_exists(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 99,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "New Group Not Found"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_patch_new_group_not_owned(app_with_data):
    resp = app_with_data.test_client().patch(
        "/app/events/1",
        data=json.dumps(
            {
                "group_id": 4,
                "description": "event1descr",
                "name": "event11",
                "date": date_str,
            }
        ),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "New Group Does Not Belong To Requester"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_delete(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/events/1",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )
    assert resp.status_code == 204
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db is None


def test_delete_forbidden(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/events/1",
        headers={
            "Authorization": valid_auth_header(
                3, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db.group.id == 2
    assert event_db.group.admin.id == 1
    assert event_db.name == "event1"
    assert event_db.description == "Descr1"
    assert event_db.date != date_datetime


def test_delete_not_users(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/events/3",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )
    assert resp.status_code == 403
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 1))
    assert event_db is not None


def test_delete_not_existent(app_with_data):
    resp = app_with_data.test_client().delete(
        "/app/events/99",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )
    assert resp.status_code == 404
    # db
    event_db = app_with_data.db.Session.scalar(select(Event).where(Event.id == 99))
    assert event_db is None
