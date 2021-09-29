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
        self.database_name = "cinema"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:123123', 'localhost:5432', self.database_name)
        # database_path = os.environ['DATABASE_URL']
        # if database_path.startswith("postgres://"):
        #     database_path = database_path.replace(
        #         "postgres://", "postgresql://", 1)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1NGI3YzlmZTM5YmIwMDY5MWUyMTEwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzI5NDIwMjgsImV4cCI6MTYzMzAyODQyOCwiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.F2RQTmjobG-CHTqdYTb0nXJlow2G1Y06_94XvaTkZtNkbCBBfWORz6hjvZTrioMvLWHwGHfgmEhyq2kMEEDsiLdbAwwyMbu02grH87Thj_CZ8Y6u62u5qfgCX-AxxGzgA2sBvm7fbxUuWaWVZ8tdQfNMHPS5PKnknzmcCP2lvnHjR72wd20vd0XPZMVOdrD3F_lLFo3wA23ry7qOeh26lIhGjP3zmAkBaeFruzaNtzA7neQPY5a8XDOpsi3RUrTag9tHbJ0ZabUC9PJjuoIfCRV3j5EmaV8hN3cMPSCqpWyYOIWiKqr86VW2JH0off-sWggtzjZPzRU_PxtpBgfN6A'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1NGQ1YjUzM2Y2OTIwMDcwNDJjMWUwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzI5NDk2ODgsImV4cCI6MTYzMzAzNjA4OCwiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.QjYJsnvOLrd8YyWqVmJHnUI_bMXy9rLra_QNUjixTBgQziuhLlf_smVpbD2_qFZPFUL7iJWbZ_bUFhQZHPStabxwnoyJgVZ0vv_wXV3dpPtMf6A8O6V04rDTWc-b-iWr_rsvq9-iv-0QGQZpAeNvzsf__Uf2Aw8kWuXwF52e6gImpoCRGgo4mQ6Uod_sP2eqIAE2UzV-taUHCROGxwC_gGeRJrp7BqNW9du6SpXupepc-zlTxNpv-ovVAT_uU_Z6NDhZKGk2JZ5i7hYJf1BFTuWo5P9je2QG56osuqSXTFS7SA9GixuNUmnqdPphNVtkyqHZZ7EPdMIe8pPm5MJZ2w'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1NGQ2ZmUwMmIzZGQwMDcxYzJhZGM2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzI5NTAwMTcsImV4cCI6MTYzMzAzNjQxNywiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.wLmsCviRwV5NkXyW-Ex_5oZxo6Xt35Wif_ig3iYpzw7iDtHLqfCLXryjGt3c2tObcfMUA-XIMYDr5Eu--lcFVLGKjLxO6DU02rONOrcJ1u3HdLqXGMo86FeZ_a_gC9MLHK8KePqDRR8hEjoXDnGxwwX8lHjuufesxD7zvia4TgZvYx9SFkJR_0y4IDwSTSC-Tk-d0PpJK2EZoV844H64mnmevW6_fW48bPMMSj-TCwF0-tZRQ1KIwJJAuNBcru4bjL67NZy1iQNRpygxEanejitqHG7gVHMqNsjNMEHjpVk-uP50-1qHQ5FzvP8lKAlM2EGy7LXG835ZxxDF4WU4UQ'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# Test Get actors API

    def test_get_actors(self):  # Test for success behavior
        res = self.client().get('/actors',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_404_get_actors(self):  # Test for error behavior
        res = self.client().get('/actors/',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test Get movies API

    def test_get_movies(self):  # Test for success behavior
        res = self.client().get('/movies',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_movies(self):  # Test for error behavior
        res = self.client().get('/movies/',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test post new actor API

    def test_post_actors(self):  # Test for success behavior
        new_test_actor = {
            "name": "actor test name",
            "age": 0,
            "gender": "Female"
        }
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_422_post_actors(self):  # Test for error behavior
        new_test_actor = {
            "name": "actor test name",
            "age": "five",
            "gender": "Female"
        }
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Test post new movie API

    def test_post_movies(self):  # Test for success behavior
        new_test_movie = {
            "title": "movie test name",
            "release_date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_movies(self):  # Test for error behavior
        new_test_movie = {
            "title": "movie test name",
            "release_date": "date"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Test delet actor API

    def test_delete_actors(self):  # Test for success behavior

        res = self.client().delete('/actors/2',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(actor, None)

    def test_404_delete_actors(self):  # Test for error behavior

        res = self.client().delete('/actors/200',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test delet movie API

    def test_delete_movies(self):  # Test for success behavior

        res = self.client().delete('/movies/2',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(movie, None)

    def test_404_delete_movies(self):  # Test for error behavior

        res = self.client().delete('/movies/200',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch actor API

    def test_patch_actors(self):  # Test for success behavior

        res = self.client().patch('/actors/1', json={'age': "33"},
                                  headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_actors(self):  # Test for error behavior

        res = self.client().delete('/actors/200',
                                   json={'name': "updated actor name"},
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch movie API

    def test_patch_movies(self):  # Test for success behavior

        res = self.client().patch('/movies/1',
                                  json={'title': "updated test movie title"},
                                  headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_404_patch_movies(self):  # Test for error behavior

        res = self.client().delete('/movies/200',
                                   json={'title': "updated movie title"},
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test RBAC for casting assistant role

    # Test for authorized access
    def test_get_actors_casting_assistant_role(self):
        res = self.client().get('/actors',
                                headers=self.casting_assistant_header)
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
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=self.casting_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for unauthorized access
    def test_401_get_actors_casting_director_role(self):
        new_test_movie = {
            "title": "movie test name",
            "date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

# Test RBAC for executive producer role

    # Test for authorized access
    def test_get_actors_executive_producer_role(self):
        new_test_movie = {
            "title": "movie test name",
            "date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for unauthorized access
    def test_401_get_actors_executive_producer_role(self):
        new_test_movie = {
            "title": "movie test name",
            "date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
