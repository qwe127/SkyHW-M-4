from flask import request
from flask_restx import Resource, Namespace

from app.dao.models.genre import GenreSchema
from app.container import genre_service
from app.helpers.decorators import auth_required
genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = genre_service.get_all()
        return genres_schema.dump(all_genres), 200

    @auth_required
    def post(self):
        req_json = request.json
        genre_service.create(req_json)

        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200

    @auth_required
    def put(self, gid):
        req_json = request.json
        req_json['id'] = gid

        genre_service.update(req_json)

        return "", 204

    @auth_required
    def patch(self, gid):
        req_json = request.json
        req_json['id'] = gid

        genre_service.update_partial(req_json)

        return "", 204

    @auth_required
    def delete(self, gid):
        genre_service.delete(gid)

        return "", 204
