import json
from unittest.mock import patch, MagicMock

from tests.conftest import valid_auth_header


def test_invitation_group_not_found(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/99/invite",
        data=json.dumps({"user_id": 3}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "Group Not Found"


def test_invitation_group_not_owned(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/1/invite",
        data=json.dumps({"user_id": 3}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 403
    assert resp.json["message"] == "Forbidden"


def test_invitation_user_not_found(app_with_data):
    resp = app_with_data.test_client().post(
        "/app/groups/1/invite",
        data=json.dumps({"user_id": 99}),
        content_type="application/json",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "User Not Found"


def test_invitation_valid(app_with_data):
    with patch(
        "app.api.groups.endpoints.send_invitation_email", MagicMock()
    ) as mail_mock:
        resp = app_with_data.test_client().post(
            "/app/groups/1/invite",
            data=json.dumps({"user_id": 2}),
            content_type="application/json",
            headers={
                "Authorization": valid_auth_header(
                    1, app_with_data.config["SECRET_KEY_JWT"]
                )
            },
        )

        # Response
        assert resp.status_code == 200
        assert resp.json["message"] == "Success"

        # Email
        mail_mock.assert_called_once()
        assert mail_mock.call_args[0][0] == "adam.malysz@test.com"
