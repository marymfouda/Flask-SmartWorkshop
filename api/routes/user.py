from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.User import User
from api.api_models import UserNodeCreation

users_ns = Namespace(name="Users", path= '/users', validate=True,
                       description='User information and analysis')

@users_ns.route('/', methods=['GET'])
class UserAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "device_id")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = User(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@users_ns.route('/<string:id>')
class UserById(Resource):

    def get(self, id):
        dao = User(current_app.driver)

        person = dao.findById(id)

        return jsonify(person)


@users_ns.route('/add')
class UserCreate(Resource):

    @users_ns.expect(UserNodeCreation)
    def post(self):
        dao = User(current_app.driver)

        user = dao.addUser(users_ns.payload['device_id'], users_ns.payload['type'])

        return user, 201


