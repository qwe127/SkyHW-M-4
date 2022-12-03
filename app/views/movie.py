from flask import request
from flask_restx import Resource, Namespace

from app.dao.models.movie import MovieSchema
from app.container import movie_service
from app.helpers.decorators import auth_required

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = movie_service.get_all()
        return movies_schema.dump(all_movies), 200

    @auth_required
    def post(self):
        req_json = request.json
        movie_service.create(req_json)

        return "", 201


# filter by genres
@movie_ns.route('/genre_id=<int:gid>')
class MoviesView(Resource):
    def get(self, gid: int):
        movies_filtered = movie_service.get_by_genres(gid)
        return movies_schema.dump(movies_filtered), 200


# filter by directors
@movie_ns.route('/director_id=<did>')
class MoviesView(Resource):
    def get(self, did):
        movies_filtered = movie_service.get_by_directors(did)
        return movies_schema.dump(movies_filtered), 200


# pages
@movie_ns.route('/page=<int:pid>')
class MoviesView(Resource):
    def get(self, pid: int):
        movie_page = movie_service.get_12(pid)
        return movies_schema.dump(movie_page), 200


# status
@movie_ns.route('/status=new')
class MoviesView(Resource):
    def get(self):
        movies_sorted = movie_service.sort_by_year()
        return movies_schema.dump(movies_sorted), 200


# status and pages
@movie_ns.route('/status=new/page=<int:pid>')
class MoviesView(Resource):
    def get(self, pid: int):
        movie_page = movie_service.get_12_new(pid)
        return movies_schema.dump(movie_page), 200


# filter by year
@movie_ns.route('/year=<year>')
class MoviesView(Resource):
    def get(self, year):
        movies_filtered = movie_service.get_by_year(year)
        return movies_schema.dump(movies_filtered), 200


@movie_ns.route('/<mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @auth_required
    def put(self, mid):
        req_json = request.json
        req_json['id'] = mid

        movie_service.update(req_json)

        return "", 204

    @auth_required
    def patch(self, mid):
        req_json = request.json
        req_json['id'] = mid

        movie_service.update_partial(req_json)

        return "", 204

    @auth_required
    def delete(self, mid):
        movie_service.delete(mid)

        return "", 204
