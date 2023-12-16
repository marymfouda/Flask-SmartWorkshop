from flask import current_app
from flask_restx import Resource, Namespace

from api.DataAccessObject.FoldingSecurit import FoldingSecurit
from api.api_models import FoldingSecuritService

folding_ns = Namespace(name="Folding Securit", path= '/services/foldingsecurit', validate=True,
                       description='Folding Securit information and analysis')



@folding_ns.route('/new')
class FoldingSecuritCreateService(Resource):

    @folding_ns.expect(FoldingSecuritService)
    def post(self):
        dao = FoldingSecurit(current_app.driver)

        service = dao.newService(folding_ns.payload['device_id'], 
                                  folding_ns.payload['height'],
                                  folding_ns.payload['width'],
                                  folding_ns.payload['sink'],
                                  folding_ns.payload['piece_count'])
        if service.get('message'):
            return service, 404

        return service, 201


