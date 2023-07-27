from flask_restx import Resource

from app.api.events.marshmellow_schemas import EventCreatePutSchema, EventPatchSchema
from app.api.events.namespace import api_events
from app.api.events.restx_models import event_create, event_created
from app.validation import validate_schema, validate_jwt


@api_events.route("/")
class Events(Resource):
    @api_events.expect(event_create)
    @api_events.response(201, "Created", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(409, "Group Not Found")
    @validate_schema(api_events, EventCreatePutSchema)
    @validate_jwt(api_events)
    def post(self, validated_schema, jwtoken_decoded):
        pass

    @api_events.response(200, "Success", [event_created])
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not Found")
    @validate_jwt(api_events)
    def get(self, jwtoken_decoded):
        pass


@api_events.route("/<id>")
class EventsByID(Resource):
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not Found")
    @validate_jwt(api_events)
    def get(self, id, jwtoken_decoded):
        pass

    @api_events.expect(event_create)
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not found")
    @api_events.response(409, "Conflict")
    @validate_schema(api_events, EventCreatePutSchema)
    @validate_jwt(api_events)
    def put(self, id, validated_schema, jwtoken_decoded):
        pass

    @api_events.expect(event_create)
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not found")
    @api_events.response(409, "Conflict")
    @validate_schema(api_events, EventPatchSchema)
    @validate_jwt(api_events)
    def patch(self, id, validated_schema, jwtoken_decoded):
        pass

    @api_events.response(204, "No Content")
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not Found")
    @validate_jwt(api_events)
    def delete(self, id, jwtoken_decoded):
        pass
