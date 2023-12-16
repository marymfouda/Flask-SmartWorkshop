from flask import current_app
from flask_restx import Resource, Namespace

from api.DataAccessObject.Securit5Shutters import Securit5Shutters
from api.api_models import SecuritService

securit_ns = Namespace(name="Securit", path= '/services/securit', validate=True,
                       description='Securit 5 Shutter information and analysis')



@securit_ns.route('/new')
class Securit5ShuttersCreateService(Resource):

    @securit_ns.expect(SecuritService)
    def post(self):
        dao = Securit5Shutters(current_app.driver)

        service = dao.newService(securit_ns.payload['device_id'], 
                                  securit_ns.payload['height'],
                                  securit_ns.payload['width'],
                                  securit_ns.payload['piece_count'])
        if service.get('message'):
            return service, 404

        return service, 201


