import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Players, Teams
#actual jwts 
manager_jwt = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTIyYTU5OWY4MzAwNmFkNjQ4NWYiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjUzOTQsImV4cCI6MTYyMTQzMjU5NCwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwbGF5ZXIiLCJnZXQ6cGxheWVycyIsImdldDpwbGF5ZXJzLWRldGFpbCIsImdldDp0ZWFtcyIsImdldDp0ZWFtcy1kZXRhaWwiLCJwYXRjaDpwbGF5ZXIiLCJwb3N0OnBsYXllciIsInBvc3Q6dGVhbSJdfQ.OEBevFuwXhn4gZjS5p68qxTJf2bNWjbjIdDmDptyk1ZUkD8iZ7dzZWJQXSVcTYP3OyE9sIODTx-EYO7Fx0CnVnJ0rga_4Q0XjJYdIsPFu9qmPYn92EUhh5j2lMY5TEs1XgEoF-CdQpdruTqYx9INtPyC--HcGmCrXC6eHZyc0W1WH2bYNjLI_ewV8TwGO8O4dqlfnjXZhse6Y1ADDbRmSWfnLX8ti12WmCaup8Q2sw9xkemOD9TftmG2XTn8WJQMdqzzRspxtL9M8VXRKOsXpmMIMHyiV5fgdr1vV4KMWQ-KBXo8vnH00OX9P0XTSYMrx_Zh2uKGgEsFKUOd5bKJhw'
fan_jwt = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjU0MzIsImV4cCI6MTYyMTQzMjYzMiwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.TDClBKcCbADvZzirmTGhAFRTtldafZ3WMFB3qtSN0hFE2A0MTi56k3RzVfwacXxIZF5pProeJBrZ_3MDUYRK43-ExQTPjSUNK3wy2kp0AKqeDIr4rCKLRleBBL0nA2-RxJxCRFto2_QhGZ6kSXLxQeZ-RRnSkOCNxZR17wBkhJo8UZtofqccFWvBZdi-4C0CreOitoCYMQ9g1lgUuTt6lUQp6q2Cd2qpFeeqSsckJ16nxihAY5w6hdzxU0Q-UB-JP_yjI0v0_PRz4QCKOO13AkcDIjJreAzcEjJTLha-5cARtyeHdBzMq9b9VdUvxQjm5YxfeTI2J6jXK_J7Rz4SGQ'

#test jwt
non_bearer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjU0MzIsImV4cCI6MTYyMTQzMjYzMiwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.TDClBKcCbADvZzirmTGhAFRTtldafZ3WMFB3qtSN0hFE2A0MTi56k3RzVfwacXxIZF5pProeJBrZ_3MDUYRK43-ExQTPjSUNK3wy2kp0AKqeDIr4rCKLRleBBL0nA2-RxJxCRFto2_QhGZ6kSXLxQeZ-RRnSkOCNxZR17wBkhJo8UZtofqccFWvBZdi-4C0CreOitoCYMQ9g1lgUuTt6lUQp6q2Cd2qpFeeqSsckJ16nxihAY5w6hdzxU0Q-UB-JP_yjI0v0_PRz4QCKOO13AkcDIjJreAzcEjJTLha-5cARtyeHdBzMq9b9VdUvxQjm5YxfeTI2J6jXK_J7Rz4SGQ'
missing_token = 'bearer'
expired_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjE0MjU0MzIsImV4cCI6MTYyMTQzMjYzMiwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.TDClBKcCbADvZzirmTGhAFRTtldafZ3WMFB3qtSN0hFE2A0MTi56k3RzVfwacXxIZF5pProeJBrZ_3MDUYRK43-ExQTPjSUNK3wy2kp0AKqeDIr4rCKLRleBBL0nA2-RxJxCRFto2_QhGZ6kSXLxQeZ-RRnSkOCNxZR17wBkhJo8UZtofqccFWvBZdi-4C0CreOitoCYMQ9g1lgUuTt6lUQp6q2Cd2qpFeeqSsckJ16nxihAY5w6hdzxU0Q-UB-JP_yjI0v0_PRz4QCKOO13AkcDIjJreAzcEjJTLha-5cARtyeHdBzMq9b9VdUvxQjm5YxfeTI2J6jXK_J7Rz4SGQ'
missing_kid_token = 
wrong_audience_token = 
unparsable_token = 
missing_rsa_key_token = 
not_jwt_token = 'not jwt token'
no_permissions_token = 

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(True)
        self.client = self.app.test_client
        self.client().post('/teams', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Bayern", 
            "nation": "Germany", "rating": 95}
            )
        self.client().post('/players', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Manuel Neuer", 
            "nationality": "German", "rating": 95, "team_id": 1}
            )
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_add_team(self):
        res = self.client().post('/teams', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Dortmund", 
            "nation": "Germany", "rating": 88}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_add_team_422_error_out_bounds_rating(self):
        res = self.client().post('/teams', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Barcelona", 
            "nation": "Spain", "rating": 1000}
            )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_team_422_error_missing_team_info(self):
        res = self.client().post('/teams', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Barcelona", 
            "nation": "Spain"}
            )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")
        
    def test_add_player(self):
        res = self.client().post('/players', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "Thomas Mueller", 
            "nationality": "German", "rating": 88, "team_id": 1}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_add_player_422_error_out_bounds_rating(self):
        res = self.client().post('/players', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "David Alaba", 
            "nationality": "Austrian", "rating": 105, "team_id": 1}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_player_422_error_missing_player_info(self):
        res = self.client().post('/players', headers = {'Content-Type': 'application/json',
            'Authorization': manager_jwt}, json={"name": "David Alaba", 
            "nationality": "Austrian", "team_id": 1}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_get_players(self):
        res = self.client().get('/players', headers = {
            'Content-Type': 'application/json',
            'Authorization': fan_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])

    def test_get_teams(self):
        res = self.client().get('/teams', headers = {
            'Content-Type': 'application/json',
            'Authorization': fan_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])
    
    def test_get_player_detailed(self):
        res = self.client().get('/players/1', headers = {
            'Content-Type': 'application/json',
            'Authorization': manager_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_get_player_detailed_404_error_id_does_not_exist(self):
        res = self.client().get('/players/2000', headers = {
            'Content-Type': 'application/json',
            'Authorization': manager_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_get_team_detailed(self):
        res = self.client().get('/teams/1', headers = {
            'Content-Type': 'application/json',
            'Authorization': manager_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_get_team_detailed_404_error_id_does_not_exist(self):
        res = self.client().get('/teams/2000', headers = {
            'Content-Type': 'application/json',
            'Authorization': manager_jwt
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_update_player(self):
        res = self.client().patch('/players/1', headers = {
            'Content-Type': 'application/json', 'Authorization': manager_jwt}, json={
            "rating": 94}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_update_player_404_error_id_does_not_exist(self):
        res = self.client().patch('/players/1000', headers = {
            'Content-Type': 'application/json', 'Authorization': manager_jwt}, json={
            "rating": "94"}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Unprocessable")

    def test_update_player_422_error_invalid_data_type(self):
        res = self.client().patch('/players/1', headers = {
            'Content-Type': 'application/json', 'Authorization': manager_jwt}, json={
            "rating": "ninety four"}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_delete_player(self):
        res = self.client().delete('/players/1', headers = {
            'Content-Type': 'application/json', 'Authorization': manager_jwt}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player_id'])

    def test_delete_player_404_error_id_does_not_exist(self):
        res = self.client().patch('/players/1000', headers = {
            'Content-Type': 'application/json', 'Authorization': manager_jwt}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Unprocessable")


    # Authentication errors
    def test_401_error_bearer_token_required(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': non_bearer_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization header must start with "Bearer".')

    def test_401_error_token_missing(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': missing_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Token not found.')

    def test_401_error_more_than_two_parts_to_token(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': not_jwt_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization header must be bearer token.')

    def test_401_error_token_missing_kid(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': missing_kid_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization malformed.')

    def test_401_error_token_expired(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': expired_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Token expired.')

    def test_401_error_wrong_audience(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': wrong_audience_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 
            'Incorrect claims. Please, check the audience and issuer.')

    def test_400_can_not_parse_token(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': unparsable_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Unable to parse authentication token.')
    
    def test_400_missing_rsa_key(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': missing_rsa_key_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Unable to find the appropriate key.')

    def test_400_error_permissions_not_included(self):
        res = self.client().get('/players', headers = {'Content-Type': 'application/json',
            'Authorization': no_permissions_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Permissions not included in JWT.')

    def test_403_error_required_permission_not_included(self):
        res = self.client().get('/players/1', headers = {'Content-Type': 'application/json',
            'Authorization': fan_jwt}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Permission not found.')
    

 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
