from marshmallow import Schema, fields, validate


class GroupCreatePutSchema(Schema):
    admin_id = fields.Integer(required=True, validate=validate.Range(min=1))
    name = fields.Str(required=True, validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))


class GroupPatchSchema(Schema):
    admin_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.Str(validate=validate.Length(1))
    description = fields.Str(validate=validate.Length(1))


class GroupInviteSchema(Schema):
    user_id = fields.Integer(required=True, validate=validate.Range(min=1))
