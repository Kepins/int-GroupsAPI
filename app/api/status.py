from flask_restx import Resource
from flask_restx import Namespace


status_api = Namespace('api/status', description='Check status of API')


@status_api.route('/')
class Status(Resource):
    def get(self):
        return {'status': 'ok'}
