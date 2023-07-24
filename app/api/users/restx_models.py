from flask_restx import fields

from app.api.users.namespace import api_users

user_create = api_users.model('UserCreate', {
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String,
    'email': fields.String,
})


user_created = api_users.model('UserCreated', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
})
