import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_path = os.environ['DATABASE_URL']
        if database_path.startswith("postgres://"):
            database_path = database_path.replace(
                "postgres://", "postgresql://", 1)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# Test Get movies


    def test_get_movies(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().get('/movies',
                                headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_movies(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().get('/movies/',
                                headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test post new movie

    def test_post_movies(self):  # Test for success
        new_test_movie = {
            "title": "movie name",
            "release_date": "2100-12-12"
        }
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_movies(self):  # Test for error
        new_test_movie = {
            "release_date": "2020/2/2"
        }
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Test delete movie

    def test_delete_movies(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().delete('/movies/2',
                                   headers=headers)
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(movie, None)

    def test_404_delete_movies(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().delete('/movies/200',
                                   headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch movie

    def test_patch_movies(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().patch('/movies/1',
                                  json={'title': "updated test movie title"},
                                  headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_movies(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().delete('/movies/200',
                                   json={'title': "updated movie title"},
                                   headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test Get actors

    def test_get_actors(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().get('/actors',
                                headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_actors(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().get('/actors/',
                                headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test post new actor

    def test_post_actors(self):  # Test for success
        new_test_actor = {
            "name": "Juliae",
            "age": 54,
            "gender": "Female"
        }
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Test delete actor

    def test_delete_actors(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().delete('/actors/2',
                                   headers=headers)
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(actor, None)

    def test_404_delete_actors(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().delete('/actors/200',
                                   headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch actor API

    def test_patch_actors(self):  # Test for success
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}

        res = self.client().patch('/actors/1', json={'age': "33"},
                                  headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_actors(self):  # Test for error
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}

        res = self.client().delete('/actors/200',
                                   json={'name': "updated actor name"},
                                   headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test casting assistant role

    # Test for authorized access
    def test_get_actors_casting_assistant_role(self):
        CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR', None)
        headers = {'Authorization': 'Bearer{}'.format(CASTING_DIRECTOR)}
        res = self.client().get('/actors',
                                headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # Test for unauthorized access
    def test_401_get_actors_casting_assistant_role(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

# Test RBAC for casting director role

    # Test for authorized access
    def test_get_actors_casting_director_role(self):
        new_test_actor = {
            "name": "actor name test role ",
            "age": 20,
            "gender": "Female"
        }
        CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR', None)
        headers = {'Authorization': 'Bearer{}'.format(CASTING_DIRECTOR)}
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for unauthorized access
    def test_401_get_actors_casting_director_role(self):
        new_test_movie = {
            "title": "movie test name",
            "release_date": "2000-12-12"
        }
        CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR', None)
        headers = {'Authorization': 'Bearer{}'.format(CASTING_DIRECTOR)}
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=headers)

        self.assertEqual(res.status_code, 401)

# Test RBAC for executive producer role

    # Test for authorized access
    def test_get_actors_executive_producer_role(self):
        new_test_movie = {
            "title": "movie test name",
            "release_date": "2000-12-12"
        }
        EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER', None)
        headers = {'Authorization': 'Bearer{}'.format(EXECUTIVE_PRODUCER)}
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for unauthorized access
    def test_401_get_actors_executive_producer_role(self):
        new_test_movie = {
            "title": "movie test name",
            "release_date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
