from marshmallow import Schema, fields, validate


class GroupCreatePutSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))


class GroupPatchSchema(Schema):
    name = fields.Str(validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))


class GroupInviteSchema(Schema):
    user_id = fields.Integer(required=True, validate=validate.Range(min=1))
