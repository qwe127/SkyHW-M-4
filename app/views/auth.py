from flask import request
from flask_restx import Namespace, Resource

from app.container import auth_service, user_service

auth_ns = Namespace("auth")


# makes a users
@auth_ns.route('/register')
class AuthsView(Resource):
    def post(self):
        req_json = request.json
        user_service.create(req_json)

        return "user created", 201


# keys
@auth_ns.route('/login')
class AuthsView(Resource):
    def post(self):
        data = request.json

        email = data.get("email", None)
        password = data.get("password", None)
        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
