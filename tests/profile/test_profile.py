from tests.conftest import valid_auth_header


def test_profile1(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/profile/",
        headers={
            "Authorization": valid_auth_header(
                2, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json["id"] == 2
    assert resp.json["first_name"] == "Adam"
    assert resp.json["last_name"] == "Małysz"
    assert resp.json["email"] == "adam.malysz@test.com"
    assert len(resp.json["groups"]) == 1
    assert len(resp.json["events"]) == 2


def test_profile2(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/profile/",
        headers={
            "Authorization": valid_auth_header(
                1, app_with_data.config["SECRET_KEY_JWT"]
            )
        },
    )

    assert resp.status_code == 200
    assert resp.json["id"] == 1
    assert resp.json["first_name"] == "Filip"
    assert resp.json["last_name"] == "Nowak"
    assert resp.json["email"] == "FiliNowak@test.com"
    assert len(resp.json["groups"]) == 0
    assert len(resp.json["events"]) == 0
