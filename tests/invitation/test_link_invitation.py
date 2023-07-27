from sqlalchemy import select

from app.tokens.itsdangerous_tokens import create_invitation_token
from models import User, Group


def test_link_invitation_random_token(app_with_data):
    resp = app_with_data.test_client().get(
        "/app/groups/invitations/random_token",
    )

    assert resp.status_code == 400


def test_link_invitation_user_not_found(app_with_data):
    class User:
        pass

    user = User()
    setattr(user, "id", 99)
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 1))

    with app_with_data.app_context():
        token = create_invitation_token(user, group)
    resp = app_with_data.test_client().get(
        f"/app/groups/invitations/{token}",
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "User Not Found"


def test_link_invitation_group_not_found(app_with_data):
    class Group:
        pass

    group = Group()
    setattr(group, "id", 99)
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 1))

    with app_with_data.app_context():
        token = create_invitation_token(user, group)
    resp = app_with_data.test_client().get(
        f"/app/groups/invitations/{token}",
    )

    assert resp.status_code == 404
    assert resp.json["message"] == "Group Not Found"


def test_link_invitation_user_already_in_group(app_with_data):
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 1))
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 1))

    group.users.append(user)
    app_with_data.db.Session.add(group)
    app_with_data.db.Session.commit()

    with app_with_data.app_context():
        token = create_invitation_token(user, group)
    resp = app_with_data.test_client().get(
        f"/app/groups/invitations/{token}",
    )

    assert resp.status_code == 409
    assert resp.json["message"] == "User Already In Group"


def test_link_invitation_valid(app_with_data):
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 1))
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 1))

    with app_with_data.app_context():
        token = create_invitation_token(user, group)
    resp = app_with_data.test_client().get(
        f"/app/groups/invitations/{token}",
    )

    assert resp.status_code == 200
    assert resp.json["message"] == "Success"
    # db
    user = app_with_data.db.Session.scalar(select(User).where(User.id == 1))
    group = app_with_data.db.Session.scalar(select(Group).where(Group.id == 1))
    assert group in user.groups
