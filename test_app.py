import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Players, Teams


# Actual jwts
manager_jwt = 'bearer ' + os.getenv('MANAGER_JWT', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTIyYTU5OWY4MzAwNmFkNjQ4NWYiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjMyNDA1NTksImV4cCI6MTYyMzI0Nzc1OSwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwbGF5ZXIiLCJnZXQ6cGxheWVycyIsImdldDpwbGF5ZXJzLWRldGFpbCIsImdldDp0ZWFtcyIsImdldDp0ZWFtcy1kZXRhaWwiLCJwYXRjaDpwbGF5ZXIiLCJwb3N0OnBsYXllciIsInBvc3Q6dGVhbSJdfQ.rQWv1byns6VRXw-0kjA_ZHLatSK-6npYToVuQFQld2BTbOHJtEAsRtKR2XgwjZsV1wNlbtkeb8HT22l0UyBVoBodErtsZFhhfEeXe5srnZcfi5ds6VryEbGo84lc2yeHEZwu2PAxWv4hUriX1Ju433qKqf2tRdpMiH3fFF30S7vmwySqG4AQvgAE6vHakWAj7LcYARZrc6dIU8lLjuvIb0dX8kzjQdlGTkrKCez0-PjWSD4dJ7LommUFsYOPzodILhUBgVa0YC8K8Zig8RSv5s5Zl4tApyE3fNwUQf0tU449puiTHzooV6nKmEZF1E1hRwE9F0cgMrWQwTLTh0ksdA')
fan_jwt = 'bearer ' + os.getenv('FAN_JWT', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjMyNDA4MDgsImV4cCI6MTYyMzI0ODAwOCwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.DDv-SPqQKfuKLwXAW96ZWcgKvCYHtrVHmBmDzMVZaaTCrj5JDd9F12Me81RWyx_d8tB-VNU9479bXyPFU8h3lZxoHTe6s0OVZqMtZbU3upAUoJxgJE7zLjCvNi_tqivRLeWYtA85-vbyNrDZPHtcH3aUv3sR5DdBAQqRGQ8B4yfpv_JLHNQYKfqqwct3RCJmPqq5QogqVjlYwXn2MLsdSnegM30XDpIoVrRMy1shO5TQP_bjIE38CKKEkyPurmFNoqKB8pYby9jhZyXC4DIndCc03tnNdtCVtQ9VqiWIolTckFBmxfEGC3F_4VcttACCMF4Bhz3ZkoravRXY6A3jrg')

# Test jwts
non_bearer_token = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM' +
    '1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1d' +
    'GgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdW' +
    'QiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjU0MzIsImV4cCI6MTYyMTQzMjYzMiwiYXpwIjo' +
    'iWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1p' +
    'c3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.TDClBKcCbADvZzirmTGh' +
    'AFRTtldafZ3WMFB3qtSN0hFE2A0MTi56k3RzVfwacXxIZF5pProeJBrZ_3MDUYRK43-Ex' +
    'QTPjSUNK3wy2kp0AKqeDIr4rCKLRleBBL0nA2-RxJxCRFto2_QhGZ6kSXLxQeZ-RRnSkO' +
    'CNxZR17wBkhJo8UZtofqccFWvBZdi-4C0CreOitoCYMQ9g1lgUuTt6lUQp6q2Cd2qpFee' +
    'qSsckJ16nxihAY5w6hdzxU0Q-UB-JP_yjI0v0_PRz4QCKOO13AkcDIjJreAzcEjJTLha-' +
    '5cARtyeHdBzMq9b9VdUvxQjm5YxfeTI2J6jXK_J7Rz4SGQ')
missing_token = 'bearer'
expired_token = ('bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJje' +
    'kZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzL' +
    'mF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLC' +
    'JhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjU0MzIsImV4cCI6MTYyMTQzMjYzMiwiYXp' +
    'wIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBl' +
    'cm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.TDClBKcCbADvZzir' +
    'mTGhAFRTtldafZ3WMFB3qtSN0hFE2A0MTi56k3RzVfwacXxIZF5pProeJBrZ_3MDUYRK4' +
    '3-ExQTPjSUNK3wy2kp0AKqeDIr4rCKLRleBBL0nA2-RxJxCRFto2_QhGZ6kSXLxQeZ-RR' +
    'nSkOCNxZR17wBkhJo8UZtofqccFWvBZdi-4C0CreOitoCYMQ9g1lgUuTt6lUQp6q2Cd2q' +
    'pFeeqSsckJ16nxihAY5w6hdzxU0Q-UB-JP_yjI0v0_PRz4QCKOO13AkcDIjJreAzcEjJT' +
    'Lha-5cARtyeHdBzMq9b9VdUvxQjm5YxfeTI2J6jXK_J7Rz4SGQ')
missing_kid_token = ('bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIi' +
    'OiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhd' +
    'WQiOiJkcmlua3MifQ.sIlQB2QFPXqh0YOQutsrp6wwTV_XWgDHE4yOozdzWqs')
wrong_audience_token = ('bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZC' +
    'I6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZS' +
    'I6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhdWQiOiJibGFoIiwicGVybWlzc2l' +
    'vbnMiOlsiZGVsZXRlOnBsYXllciIsImdldDpwbGF5ZXJzIiwiZ2V0OnBsYXllcnMtZGV0' +
    'YWlsIiwiZ2V0OnRlYW1zIiwiZ2V0OnRlYW1zLWRldGFpbCIsInBhdGNoOnBsYXllciIsI' +
    'nBvc3Q6cGxheWVyIiwicG9zdDp0ZWFtIl19.celqbDGelk4qp2fhI3pDM8Lm8fNfNj43-' +
    '6-SnXWCLCQ')
unparsable_token = ('bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJ' +
    'jekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpv' +
    'aG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.Ga0u64TYJ4yBldwWUbaHYY-iHbhdRtt10kJ' +
    '9lUpj1lk')
missing_rsa_key_token = ('bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZC' +
    'I6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI' +
    '6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhdWQiOiJkcmlua3MifQ.Q2s-0UlJNF' +
    'HgmLXuq3P9AP7nBLSyxXrv6UmqOV72Ieo')
not_jwt_token = 'not jwt token'
no_permissions_token = ('bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZC' +
    'I6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZS' +
    'I6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhdWQiOiJkcmlua3MifQ.Q2s-0UlJ' +
    'NFHgmLXuq3P9AP7nBLSyxXrv6UmqOV72Ieo')


class SoccerTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(True)
        self.client = self.app.test_client
        self.client().post('/teams',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Bayern", "nation": "Germany", "rating": 95})
        self.client().post('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Manuel Neuer", "nationality": "German",
            "rating": 95, "team_id": 1})

    # def tearDown(self):
    #     """Executed after reach test"""
    #     pass

    def test_add_team(self):
        res = self.client().post('/teams',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Dortmund", "nation": "Germany", "rating": 88})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_add_team_422_error_out_bounds_rating(self):
        res = self.client().post('/teams',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Barcelona", "nation": "Spain", "rating": 1000})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_team_422_error_missing_team_info(self):
        res = self.client().post('/teams',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Barcelona", "nation": "Spain"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_player(self):
        res = self.client().post('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "Thomas Mueller", "nationality": "German",
            "rating": 88, "team_id": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_add_player_422_error_out_bounds_rating(self):
        res = self.client().post('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "David Alaba", "nationality": "Austrian",
            "rating": 105, "team_id": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_player_422_error_missing_player_info(self):
        res = self.client().post('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"name": "David Alaba", "nationality": "Austrian",
            "team_id": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_get_players(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': fan_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])

    def test_get_teams(self):
        res = self.client().get('/teams',
            headers = {'Content-Type': 'application/json',
            'Authorization': fan_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])

    def test_get_player_detailed(self):
        res = self.client().get('/players/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_get_player_detailed_404_error_id_does_not_exist(self):
        res = self.client().get('/players/2000',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_get_team_detailed(self):
        res = self.client().get('/teams/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_get_team_detailed_404_error_id_does_not_exist(self):
        res = self.client().get('/teams/2000',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_update_player(self):
        res = self.client().patch('/players/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"rating": 94})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_update_player_404_error_id_does_not_exist(self):
        res = self.client().patch('/players/1000',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"rating": "94"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_update_player_422_error_invalid_data_type(self):
        res = self.client().patch('/players/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt},
            json={"rating": "ninety four"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_delete_player(self):
        res = self.client().delete('/players/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player_id'])

    def test_delete_player_404_error_id_does_not_exist(self):
        res = self.client().patch('/players/1000',
            headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    # Authentication errors

    def test_401_error_bearer_token_required(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': non_bearer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_missing(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': missing_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_more_than_two_parts_to_token(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': not_jwt_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_missing_kid(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': missing_kid_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_expired(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': expired_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_400_can_not_parse_token(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': unparsable_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')
    
    def test_400_missing_rsa_key(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': missing_rsa_key_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_400_error_permissions_not_included(self):
        res = self.client().get('/players',
            headers = {'Content-Type': 'application/json',
            'Authorization': no_permissions_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_403_error_required_permission_not_included(self):
        res = self.client().get('/players/1',
            headers = {'Content-Type': 'application/json',
            'Authorization': fan_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Forbidden')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
