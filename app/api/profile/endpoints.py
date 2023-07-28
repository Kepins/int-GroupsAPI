from flask_restx import Resource

from app.api.profile.namespace import api_profile


@api_profile.route("/")
class Profile(Resource):
    def get(self):
        pass
