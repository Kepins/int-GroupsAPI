from app import api
from flask_restx import Resource


@api.route('/api/status')
class Status(Resource):
    def get(self):
        return {'status': 'ok'}
