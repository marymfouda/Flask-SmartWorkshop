from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace


from api.DataAccessObject.Auth import Auth
from api.api_models import AdminRegister

auth_ns = Namespace(name="Auth", path='/auth', validate=True,
                     description='Admin authentication and authorization')

@auth_ns.route('/register')
class Register(Resource):

    @auth_ns.expect(AdminRegister)
    def post(self):
        dao = Auth(current_app.driver)

        user = dao.register(auth_ns.payload['userName'], auth_ns.payload['password'])

        return user


@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(AdminRegister)
    def post(self):
        dao = Auth(current_app.driver)

        admin = dao.authenticate(auth_ns.payload['userName'], auth_ns.payload['password'])


        if admin is False:
            return "Unauthorized", 401

        return jsonify(admin)
