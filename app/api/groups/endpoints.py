from flask_restx import Resource

from app.api.groups.namespace import api_groups


@api_groups.route("/")
class Groups(Resource):
    def post(self):
        pass

    def get(self):
        pass


@api_groups.route("/<id>")
class GroupsByID(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass
