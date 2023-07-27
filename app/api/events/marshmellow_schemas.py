from marshmallow import Schema, fields, validate


class EventCreatePutSchema(Schema):
    group_id = fields.Integer(required=True, validate=validate.Range(min=1))
    name = fields.Str(required=True, validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))
    date = fields.DateTime(required=True)


class EventPatchSchema(Schema):
    group_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.Str(validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))
    date = fields.DateTime()
