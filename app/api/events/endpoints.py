from flask_restx import Resource

from app.api.events.namespace import api_events


@api_events.route("/")
class Events(Resource):
    def post(self):
        pass

    def get(self):
        pass


@api_events.route("/<id>")
class EventsByID(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass
