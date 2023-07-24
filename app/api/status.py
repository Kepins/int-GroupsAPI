from flask_restx import Resource
from flask_restx import Namespace


api_status = Namespace('api/status', description='Check status of API')


@api_status.route('/')
class Status(Resource):
    def get(self):
        return {'status': 'ok'}
