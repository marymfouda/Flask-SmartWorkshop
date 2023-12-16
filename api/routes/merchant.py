from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Merchant import Merchant
from api.api_models import MerchantNodeCreation, MerchantRelations

merchants_ns = Namespace(name="Merchants", path= '/merchants', validate=True,
                       description='Merchant information and analysis')

@merchants_ns.route('/', methods=['GET'])
class MerchantAll(Resource):
    
    # @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "name")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Merchant(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@merchants_ns.route('/<string:name>')
class MerchantByName(Resource):

    def get(self, name):
        dao = Merchant(current_app.driver)

        merchant = dao.findByName(name)

        return jsonify(merchant)


@merchants_ns.route('/add')
class MerchantCreate(Resource):

    @merchants_ns.expect(MerchantNodeCreation)
    def post(self):
        dao = Merchant(current_app.driver)

        merchant = dao.addMerchant(merchants_ns.payload['name'], 
                                   merchants_ns.payload['comertial_activity'],
                                   merchants_ns.payload['contact'],
                                   merchants_ns.payload['address'])

        return merchant, 201

@merchants_ns.route('/new')
class MerchantCreate(Resource):

    @merchants_ns.expect(MerchantRelations)
    def post(self):
        dao = Merchant(current_app.driver)

        merchant = dao.newCreateMerchant(merchants_ns.payload['name'], 
                                   merchants_ns.payload['device_id'],
                                   merchants_ns.payload['comertial_activity'],
                                   merchants_ns.payload['contact'],
                                   merchants_ns.payload['address'])

        return merchant, 201

@merchants_ns.route('/contact')
class MerchantCreate(Resource):

    @merchants_ns.expect(MerchantRelations)
    def post(self):
        dao = Merchant(current_app.driver)

        merchant = dao.newContactMerchant(merchants_ns.payload['name'], 
                                   merchants_ns.payload['device_id'],
                                   merchants_ns.payload['comertial_activity'],
                                   merchants_ns.payload['contact'],
                                   merchants_ns.payload['address'])

        return merchant, 201

@merchants_ns.route('/viewgallery')
class MerchantCreate(Resource):

    @merchants_ns.expect(MerchantRelations)
    def post(self):
        dao = Merchant(current_app.driver)

        merchant = dao.newViewedMerchantGallery(merchants_ns.payload['name'], 
                                   merchants_ns.payload['device_id'],
                                   merchants_ns.payload['comertial_activity'],
                                   merchants_ns.payload['contact'],
                                   merchants_ns.payload['address'])

        return merchant, 201


