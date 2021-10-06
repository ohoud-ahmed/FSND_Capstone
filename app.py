import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from auth import AuthError, requires_auth
from flask_cors import CORS
import json
import random

from models import setup_db, Movies, Actors


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(404)

        moviesList = [movie.format() for movie in movies]

        return jsonify({
            'movies': moviesList,
            'success': True
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(token):

        try:
            body = request.get_json()
            title = body['title']
            release_date = body['release_date']

            new_movie = Movies(
                title=title,
                release_date=release_date)

            new_movie.insert()

            return jsonify({
                'movies': [new_movie.format()],
                'success': True
            })
        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(token, movie_id):

        body = request.get_json()

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = body.get('title')

            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                'success': True,
                'movies': movie.format()
            })

        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except BaseException:
            abort(422)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actors.query.all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'actors': [actor.format() for actor in actors],
            'success': True
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(token):
        body = request.get_json()

        name = body['name']
        age = body['age']
        gender = body['gender']

        new_actor = Actors(
            name=name,
            age=age,
            gender=gender
        )

        new_actor.insert()

        return jsonify({
            'actors': [new_actor.format()],
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(token, actor_id):

        body = request.get_json()

        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = body.get('name')

            if 'age' in body:
                actor.age = body.get('age')

            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actors': actor.format()
            })

        except BaseException:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):

        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            })

        except BaseException:
            abort(422)

    # Error Part
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'method not allowed'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
