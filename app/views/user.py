from flask import request
from flask_restx import Resource, Namespace

from app.dao.models.user import UserSchema
from app.container import user_service
from app.helpers.decorators import auth_required

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        return users_schema.dump(all_users), 200


@user_ns.route('/username=<username>')
class UserView(Resource):
    def get(self, username):
        user = user_service.get_by_username(username)
        return user_schema.dump(user), 200


# gets user data
@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        user = user_service.get_one(uid)
        return user_schema.dump(user), 200

    # changes name, surname, favorite_genre
    @auth_required
    def patch(self, uid):
        req_json = request.json
        req_json['id'] = uid

        user_service.update_partial(req_json)

        return "", 204

    @auth_required
    def delete(self, uid):
        user_service.delete(uid)

        return "", 204


# password change
@user_ns.route('/<int:uid>/password')
class UserView(Resource):
    @auth_required
    def put(self, uid):
        req_json = request.json
        req_json['id'] = uid
        user_service.update_password(req_json)

        return "", 204
