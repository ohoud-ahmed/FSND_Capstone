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
    def get_movies():
       moviesList = Movies.query.all()
       movies = {}
       for movie in moviesList:
           movies[movie.id] = movie.type

       return jsonify({
          'success': True,
          'movies': movies,
        })

    @app.route('/movies-detail')
    @requires_auth('get:movies-detail')
    def movies_detail(token):
      movies = Movies.query.all()

      return jsonify({
        'movies': [movie.long() for movie in movies],
        'success': True
      })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(token):
       body = request.get_json()

       title = body['title']
       date=json.dumps(body['date'])

  
       new_movie = Movies(
            title=title,
            date=date)

       new_movie.insert()

       return jsonify({
            'movies': [new_movie.long()],
            'success': True
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies') 
    def update_movies(token, movie_id):

       body = request.get_json()

       try:
           movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
           if movie is None:
               abort(404)
   
           if 'title' in body:
               movie.title = int(body.get('title'))
   
           movie.update()
   
           return jsonify({
               'success': True,
               'movies': movie.long()
           })

       except:
           abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id, token):
       try:
           movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
   
           if movie is None:
               abort(404)
   
           movie.delete()
   
           return jsonify({
               'success': True,
               'delete': movie_id
           })
   
       except:
           abort(422)

    
    
    @app.route('/actors')
    def get_actors():
       actorsList = Actors.query.all()
       actors = {}
       for actor in actorsList:
           actors[actor.id] = actor.type

       return jsonify({
          'success': True,
          'actors': actors,
        })

    @app.route('/actors-detail')
    @requires_auth('get:actors-detail')
    def actors_detail(token):
      actors = Actors.query.all()

      return jsonify({
        'actors': [actor.long() for actor in actors],
        'success': True
      })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(token):
       body = request.get_json()

       name = body['name']
       age=json.dumps(body['age'])
       gender=json.dumps(body['gender'])

  
       new_actor = Actors(
            name=name,
            age=age,
            gender=gender
            )


       new_actor.insert()

       return jsonify({
            'actors': [new_actor.long()],
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
               actor.name = int(body.get('name'))
   
           actor.update()
   
           return jsonify({
               'success': True,
               'actors': actor.long()
           })

       except:
           abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
       try:
           actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
   
           if actor is None:
               abort(404)
   
           actor.delete()
   
           return jsonify({
               'success': True,
               'delete': actor_id
           })
   
       except:
           abort(422)
   
    return app



app = create_app()

if __name__ == '__main__':
    app.run()