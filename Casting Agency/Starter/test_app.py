import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from models import setup_db, Movie, Actor, db


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgresql://postgres@localhost:5432/agency"
        setup_db(self.app, self.database_path)

        self.assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilo4SjVNRm9QTE5QblZEM3pBYTYySSJ9.eyJpc3MiOiJodHRwczovL2ZveDcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODNkNWYzYWQzNDU5MGJlMWRhMGVlMyIsImF1ZCI6Imh0dHBzOi8vYXBpLmNvbSIsImlhdCI6MTU4NTg5MTkwNCwiZXhwIjoxNTg1ODk5MTA0LCJhenAiOiJLTWhGNmZKYTEyTFloMzRvVW5aMU50RDdRMXg2cFJQdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.dfSp3nyneAoPtSMWORsXL15IkWAmm_ZW5SNZ5kxXULd012qCRXmwFI6qtXWrjGd_MFR_8mYZpJHeKmbGiLY47zhaXnrgDpoVBgZm-9KKhDCZACrCvnN8PaFi6cnYZQH6J0HR8AmPUAxMplgYUnbUxxaf4tYwCXPYupH_Bqn9J1-BGb5CheSoqOeL6ben2CIINeZVutqT5guMqL9snxDoJHKXbfN-6J49rg5rlMGRzRvnHlboTSDvEd1EUu6OYSF9jH83hZc7De44N0GJ7MXdhfeagwNXl_RaMJH0-6UnQnBwfIkN7M9f1RZzgZX3UPChKqMEXTIRqC9BV-NAsuwZrQ'
        }

        self.director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilo4SjVNRm9QTE5QblZEM3pBYTYySSJ9.eyJpc3MiOiJodHRwczovL2ZveDcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODRmODRlYWI4OGQ0MGJlOGEyZGE5ZCIsImF1ZCI6Imh0dHBzOi8vYXBpLmNvbSIsImlhdCI6MTU4NTg5MTg0MywiZXhwIjoxNTg1ODk5MDQzLCJhenAiOiJLTWhGNmZKYTEyTFloMzRvVW5aMU50RDdRMXg2cFJQdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.B3T75SpIUFr0L22So3Ymo0LSgoKzFBfRR30JjJwUOqNrYAAkTCkpRZD9x5qmuiZfic0FWuhS60zvzEtPd0iDwHAHbBku2o5KHoiQcyjuhxNXHuMB3vn-artm8_tIemIyY0o-GCxM_lKMoKyOD77tuJS33gwyycsaBwDP_esAX3DjJ9aOw0WF4IeEpF3CDy5xJMXEGeP_TkoYGwRzJrLFGn48huwJjlhMbaP-vr3qrajLiQDA6UU28vAfizMXEfL-2sSrlE41h4Di1aHs_PgJomfyud5rDMNAdoAUSSdoQhmpmuOEVRh_htsxTYBZjHat8FKv3IpcMIwtOYxpgTDuJw'
        }

        self.producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilo4SjVNRm9QTE5QblZEM3pBYTYySSJ9.eyJpc3MiOiJodHRwczovL2ZveDcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODRmODhjNmIyNjlhMGJkYzBjMTU2NCIsImF1ZCI6Imh0dHBzOi8vYXBpLmNvbSIsImlhdCI6MTU4NTg5MTc2OSwiZXhwIjoxNTg1ODk4OTY5LCJhenAiOiJLTWhGNmZKYTEyTFloMzRvVW5aMU50RDdRMXg2cFJQdyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.Jkh7BguKxhpduc2sJBHYocyhqciuN2tCXYi-uFs5MthCXuFZ8g4BODT_pocgnDrTnNiFJLVc478opZFULbTST9s3V4ELDud5jw4xb6aunQC6oKbv6GPpLtPBpcY6YDEKN69tpY_X3Mhb4k8lgIkECT8g8PwdOXrEDTRDQ3bhLWOqWfqdGH2nSdN34KF10Rdq0B6Re_pAw1jUNvRR-ppPQ1FT-ebZM4aSRT3OU41rFeUzBK3I0d9PAo6B8bXrPFybLatvBrjO7FfdX0LkHNn3ifUWDVn-52OcxZpVnFCK0WcAh3zHSaMLoJ-LIkxd38e2wgKU2VFBlZ_3W709eSZDRQ'
        }

        self.movie = {
            'title': 'Knives Out ',
            'release_date': '2019'
        }

        self.new_movie = {
            'title': 'Space',
            'release_date': '2020'
        }

        self.actor = {
            'name': 'Daniel Craig',
            'age': '52',
            'gender': 'Male'
        }

        self.new_actor = {
            'name': 'Chris Evans',
            'age': '38',
            'gender': 'Male'
        }

        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            self.db.create_all()

        self.client().post('/movies', json=self.movie, headers=self.producer_header)
        self.client().post('/actors', json=self.actor, headers=self.producer_header)

    def tearDown(self):
        self.db.drop_all()
        pass

    def test_get_actors_public(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_director(self):
        res = self.client().get('/actors', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_producer(self):
        res = self.client().get('/actors', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_movies_public(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_director(self):
        res = self.client().get('/movies', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_producer(self):
        res = self.client().get('/movies', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_post_actors_public(self):
        res = self.client().post('/actors', json=self.new_actor)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_assistant(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_director(self):
        original_count = len(Actor.query.all())

        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_actors_producer(self):
        original_count = len(Actor.query.all())

        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_movies_public(self):
        res = self.client().post('/movies', json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_assistant(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_director(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.director_header)

        self.assertEqual(res.status_code, 201)

    def test_post_movies_producer(self):
        original_count = len(Movie.query.all())

        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_patch_actors_public(self):
        res = self.client().patch('/actors/1', json={'age': "33"})

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_assistant(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': "33"},
            headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_director(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': "33"},
            headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_producer(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': "33"},
            headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch(
            '/actors/1000',
            json={
                'age': "33"},
            headers=self.producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1', headers=self.producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "New Title"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_assistant(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': " New Title"},
            headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_director(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': "New Title"},
            headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_producer(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': "New Title"},
            headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch(
            '/movies/1000',
            json={
                'title': "New Title"},
            headers=self.producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1', headers=self.producer_header)

        self.assertEqual(res.status_code, 404)

    def test_delete_actors_public(self):
        res = self.client().delete('/actors/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_assistant(self):
        res = self.client().delete('/actors/1', headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_director(self):
        res = self.client().delete('/actors/1', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actors_producer(self):
        res = self.client().delete('/actors/1', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.producer_header)

        self.assertEqual(res.status_code, 404)

    def test_delete_movies_public(self):
        res = self.client().delete('/movies/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_assistant(self):
        res = self.client().delete('/movies/1', headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_director(self):
        res = self.client().delete('/movies/1', headers=self.director_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_producer(self):
        res = self.client().delete('/movies/1', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=self.producer_header)

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
