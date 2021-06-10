import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Players, Teams


# Actual jwts
manager_jwt = 'bearer ' + os.getenv('MANAGER_JWT')
fan_jwt = 'bearer ' + os.getenv('FAN_JWT')

# Test jwts
non_bearer_token = os.getenv('NON_BEARER_TOKEN')
missing_token = 'bearer'
expired_token = os.getenv('EXPIRED_TOKEN')
missing_kid_token = os.getenv('MISSING_KID_TOKEN')
wrong_audience_token = os.getenv('WRONG_AUDIENCE_TOKEN')
unparsable_token = os.getenv('UNPARSABLE_TOKEN')
missing_rsa_key_token = os.getenv('MISSING_RSA_KEY_TOKEN')
not_jwt_token = 'not jwt token'
no_permissions_token = os.getenv('NO_PERMISSIONS_TOKEN')


class SoccerTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(True)
        self.client = self.app.test_client
        self.client().post(
            '/teams',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={"name": "Bayern", "nation": "Germany", "rating": 95}
        )
        self.client().post(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={
                "name": "Manuel Neuer",
                "nationality": "German",
                "rating": 95,
                "team_id": 1
            }
        )

    # def tearDown(self):
    #     """Executed after reach test"""
    #     pass

    def test_add_team(self):
        res = self.client().post(
            '/teams',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={"name": "Dortmund", "nation": "Germany", "rating": 88})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_add_team_422_error_out_bounds_rating(self):
        res = self.client().post(
            '/teams',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={"name": "Barcelona", "nation": "Spain", "rating": 1000})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_team_422_error_missing_team_info(self):
        res = self.client().post(
            '/teams',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
                },
            json={"name": "Barcelona", "nation": "Spain"}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_player(self):
        res = self.client().post(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={
                "name": "Thomas Mueller",
                "nationality": "German",
                "rating": 88,
                "team_id": 1
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_add_player_422_error_out_bounds_rating(self):
        res = self.client().post(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={
                "name": "David Alaba",
                "nationality": "Austrian",
                "rating": 105, "team_id": 1
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_add_player_422_error_missing_player_info(self):
        res = self.client().post(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={
                "name": "David Alaba",
                "nationality": "Austrian",
                "team_id": 1
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_get_players(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': fan_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])

    def test_get_teams(self):
        res = self.client().get(
            '/teams',
            headers={
                'Content-Type': 'application/json',
                'Authorization': fan_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])

    def test_get_player_detailed(self):
        res = self.client().get(
            '/players/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_get_player_detailed_404_error_id_does_not_exist(self):
        res = self.client().get(
            '/players/2000',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_get_team_detailed(self):
        res = self.client().get(
            '/teams/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['team'])

    def test_get_team_detailed_404_error_id_does_not_exist(self):
        res = self.client().get(
            '/teams/2000',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_update_player(self):
        res = self.client().patch(
            '/players/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt},
            json={"rating": 94}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_update_player_404_error_id_does_not_exist(self):
        res = self.client().patch(
            '/players/1000',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={"rating": "94"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    def test_update_player_422_error_invalid_data_type(self):
        res = self.client().patch(
            '/players/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            },
            json={"rating": "ninety four"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_delete_player(self):
        res = self.client().delete(
            '/players/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player_id'])

    def test_delete_player_404_error_id_does_not_exist(self):
        res = self.client().patch(
            '/players/1000',
            headers={
                'Content-Type': 'application/json',
                'Authorization': manager_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")

    # Authentication errors

    def test_401_error_bearer_token_required(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': non_bearer_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_missing(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': missing_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_more_than_two_parts_to_token(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': not_jwt_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_missing_kid(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': missing_kid_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_error_token_expired(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': expired_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_400_can_not_parse_token(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': unparsable_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_400_missing_rsa_key(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': missing_rsa_key_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_400_error_permissions_not_included(self):
        res = self.client().get(
            '/players',
            headers={
                'Content-Type': 'application/json',
                'Authorization': no_permissions_token
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_403_error_required_permission_not_included(self):
        res = self.client().get(
            '/players/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': fan_jwt
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Forbidden')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
