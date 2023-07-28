from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.profile.namespace import api_profile
from app.api.profile.restx_models import profile_get
from app.api.users.restx_models import user_created
from app.validation import validate_jwt
from models import User, Group, user_group, Event


@api_profile.route("/")
class Profile(Resource):
    @api_profile.response(200, "Success", profile_get)
    @validate_jwt(api_profile)
    def get(self, jwtoken_decoded):
        id_user = jwtoken_decoded["id"]

        user = db.Session.scalar(select(User).where(User.id == id_user))
        groups = db.Session.scalars(
            select(Group).join(user_group).join(User).where(User.id == id_user)
        ).all()
        events = db.Session.scalars(
            select(Event)
            .join(Group)
            .join(user_group)
            .join(User)
            .where(User.id == id_user)
        ).all()

        return (
            api_profile.marshal(
                {
                    "groups": groups,
                    "events": events,
                    **api_profile.marshal(user, user_created),
                },
                profile_get,
            ),
            200,
        )
