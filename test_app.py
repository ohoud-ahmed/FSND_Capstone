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

        self.casting_assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1OGMwMzIwNjcyMWUwMDY5MDhkMjU4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzM0NTc2MTMsImV4cCI6MTYzMzU0NDAxMywiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Oe_sXgW7zMshH9yWe7I7Rhw6kJla6_embZHV3k0u9-N_GkOLbqUuOqseMt6wwWtWJYbBACh7nQGB6xqfJaeQufDrGmAkRIH_nkhMw8DExQEMWXu0TYyXhms-j0E-Rf8gUOynXGDGSqKg-s1CZ4pf23-8kDSvLhG2a6eyyRFbei3NRVLHeQIQjL4BsH-5r_dL7KsmMnTiEVnc1G01Trimt_IV6g77gFRnOhZXqu6d2oPxxRUFmRF_V73dPwoBHs970bE5krW0e-QtsEmfTkYxQiBBLY08sX_ag0RhIlI2Gw5ur_6kRctRoA8gaiW4xCxfD3WfW2PXKertWfFGItlGNw'
        }

        self.casting_director_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1Y2FiMmQwMmIzZGQwMDcxYzUyYjY0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzM0NjMyMzEsImV4cCI6MTYzMzU0OTYzMSwiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.OgxAiUSrxdRic2iUY-JTc7a2BlnLkUp-nwBWAwXg-aeub15zp6Z8BdWtdMoTvhdcsW_6uTDAVLh3kgoLDzCxUIM6RslGn9U0CMxHyR3l4G41IL6y75ac6B-minjD_8Omzsa6WlJYdhZhDSwl5Uf_9nmuFTFKi7Z1WOFGH-jY_hwsm0RTh8artxLI37YVgoU4O3TjLYf1ARhb4Yk1fJvsRG18gWwpR4-zI_iuAUz8puvZw2ZON5QMMCs_XNlIZotV19Ur_HoyGkQlnfWgUlUOogLPhyG7cMg3Jlhy3G7UqFPrVQEPC2mIAw1UWdlgs5b1GUN2xP4QLYsPgibPFFCDiQ'
        }

        self.executive_producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9xejZ4UzJERE9Wd3lzdXJDMDBacCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZzI4b3hqdi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1OGMxYTljNjllYjIwMDcwNGE2ZDI3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzM0NTc4NjMsImV4cCI6MTYzMzU0NDI2MywiYXpwIjoiSWhIMXg0Z2hSMVZSRGVDMWt3TExjaW15TTNNd0xnRmQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.VS9l0XUye8ZIVJJp4Pu5dcJccLC2niH7cHHKlHCw9N4iLGFc1u8GL6jQlHNRhXJYaRS-Jd52NMP7CLUHUzSlSExP4RKVUyM9FnEsdwcmRbIEtRzO6jaiIQDgaO6ZjCB-x4QE2bZxA-TqS5BAp8byeW6JwX6rAmLVoUgicd6HIMDv6xJ4I0-21c76Y9O6JfA5YpZbMWJz51nl40r9_-J-w3CzUlGR6og5Rj1RVxgwWx456rz-d82RQhnTeaaXT8sHuE4HuaiaNbY63mO7Th-l2klONL6J8ppiLjwLHj40YL07ecIusGuol_5liCC0t-4_z6N9r7_IJfYL6eawSXx07w'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# Test Get movies

    def test_get_movies(self):  # Test for success
        res = self.client().get('/movies',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_movies(self):  # Test for error
        res = self.client().get('/movies/',
                                headers=self.executive_producer_header)
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
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_movies(self):  # Test for error
        new_test_movie = {
            "release_date": "2020/2/2"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Test delete movie

    def test_delete_movies(self):  # Test for success

        res = self.client().delete('/movies/2',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(movie, None)

    def test_404_delete_movies(self):  # Test for error

        res = self.client().delete('/movies/200',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch movie

    def test_patch_movies(self):  # Test for success

        res = self.client().patch('/movies/1',
                                  json={'title': "updated test movie title"},
                                  headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_movies(self):  # Test for error

        res = self.client().delete('/movies/200',
                                   json={'title': "updated movie title"},
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test Get actors

    def test_get_actors(self):  # Test for success
        res = self.client().get('/actors',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_actors(self):  # Test for error
        res = self.client().get('/actors/',
                                headers=self.executive_producer_header)
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
        res = self.client().post('/actors', json=new_test_actor,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Test delete actor

    def test_delete_actors(self):  # Test for success

        res = self.client().delete('/actors/2',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertEqual(actor, None)

    def test_404_delete_actors(self):  # Test for error

        res = self.client().delete('/actors/200',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test patch actor API

    def test_patch_actors(self):  # Test for success

        res = self.client().patch('/actors/1', json={'age': "33"},
                                  headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_actors(self):  # Test for error

        res = self.client().delete('/actors/200',
                                   json={'name': "updated actor name"},
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test casting assistant role

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
            "release_date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie,
                                 headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

# Test RBAC for executive producer role

    # Test for authorized access
    def test_get_actors_executive_producer_role(self):
        new_test_movie = {
            "title": "movie test name",
            "release_date": "2000-12-12"
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
            "release_date": "2000-12-12"
        }
        res = self.client().post('/movies', json=new_test_movie)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
