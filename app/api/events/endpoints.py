from flask_restx import Resource
from sqlalchemy import select

from app import db
from app.api.events.marshmellow_schemas import EventCreatePutSchema, EventPatchSchema
from app.api.events.namespace import api_events
from app.api.events.restx_models import event_create, event_created
from app.validation import validate_schema, validate_jwt, validate_kwargs_are_int
from models import Group, Event


@api_events.route("/")
class Events(Resource):
    @api_events.expect(event_create)
    @api_events.response(201, "Created", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Group Not Found")
    @validate_schema(api_events, EventCreatePutSchema)
    @validate_jwt(api_events)
    def post(self, validated_schema, jwtoken_decoded):
        group = db.Session.scalar(
            select(Group).where(Group.id == validated_schema["group_id"])
        )
        if not group:
            return {"message": "Group Not Found"}, 404
        if group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Group Does Not Belong To Requester"}, 403

        event = Event(**validated_schema)

        db.Session.add(event)
        db.Session.commit()

        return api_events.marshal(event, event_created), 201

    @api_events.response(200, "Success", [event_created])
    @validate_jwt(api_events)
    def get(self, jwtoken_decoded):
        events = db.Session.scalars(
            select(Event).join(Group).where(Group.admin_id == jwtoken_decoded["id"])
        )

        return [api_events.marshal(event, event_created) for event in events], 200


@api_events.route("/<id>")
class EventsByID(Resource):
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not Found")
    @validate_kwargs_are_int(api_events, "id")
    @validate_jwt(api_events)
    def get(self, id, jwtoken_decoded):
        event = db.Session.scalar(select(Event).where(Event.id == id))
        if not event:
            return {"message": "Not Found"}, 404

        if event.group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        return api_events.marshal(event, event_created), 200

    @api_events.expect(event_create)
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not found")
    @validate_schema(api_events, EventCreatePutSchema)
    @validate_kwargs_are_int(api_events, "id")
    @validate_jwt(api_events)
    def put(self, id, validated_schema, jwtoken_decoded):
        event = db.Session.scalar(select(Event).where(Event.id == id))
        if not event:
            return {"message": "Not Found"}, 404

        if event.group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        new_group = db.Session.scalar(
            select(Group).where(Group.id == validated_schema["group_id"])
        )
        if not new_group:
            return {"message": "New Group Not Found"}, 404
        if new_group.admin_id != jwtoken_decoded["id"]:
            return {"message": "New Group Does Not Belong To Requester"}, 403

        # iterate over every field (even NOT required)
        for key in EventCreatePutSchema().fields.keys():
            value = validated_schema.get(key)
            setattr(event, key, value)

        db.Session.add(event)
        db.Session.commit()

        return api_events.marshal(event, event_created), 200

    @api_events.expect(event_create)
    @api_events.response(200, "Success", event_created)
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not found")
    @validate_schema(api_events, EventPatchSchema)
    @validate_kwargs_are_int(api_events, "id")
    @validate_jwt(api_events)
    def patch(self, id, validated_schema, jwtoken_decoded):
        event = db.Session.scalar(select(Event).where(Event.id == id))
        if not event:
            return {"message": "Not Found"}, 404

        if event.group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        if "group_id" in validated_schema:
            new_group = db.Session.scalar(
                select(Group).where(Group.id == validated_schema["group_id"])
            )
            if not new_group:
                return {"message": "New Group Not Found"}, 404
            if new_group.admin_id != jwtoken_decoded["id"]:
                return {"message": "New Group Does Not Belong To Requester"}, 403

        for key, value in validated_schema.items():
            setattr(event, key, value)

        db.Session.add(event)
        db.Session.commit()

        return api_events.marshal(event, event_created), 200

    @api_events.response(204, "No Content")
    @api_events.response(403, "Forbidden")
    @api_events.response(404, "Not Found")
    @validate_kwargs_are_int(api_events, "id")
    @validate_jwt(api_events)
    def delete(self, id, jwtoken_decoded):
        event = db.Session.scalar(select(Event).where(Event.id == id))
        if not event:
            return {"message": "Not Found"}, 404

        if event.group.admin_id != jwtoken_decoded["id"]:
            return {"message": "Forbidden"}, 403

        db.Session.delete(event)
        db.Session.commit()

        return None, 204
