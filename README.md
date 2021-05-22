API Reference

Introduction
    This API is intended to provide an interface for fans to get general information on soccer players and teams. This API also allows managers to manage the players and teams that are available to fans to view.


Getting Started

    Base URL: 
    Authentication: this application rerquires authentication through Auth0.
        fan:
            email: fryethomas23@yahoo.com
            password: 
        
        manager:
            email: fryethomas23@gmail.com
            password: 


Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return five error types when requests fail:

    400: Bad Request
    401: Unauthorized
    403: Forbidden
    404: Resource Not Found
    422: Not Processable

Endpoints
GET /players

    General:
        Returns a list of player objects containing player's id, name, nationilty, and team; and success value. Requires json web token from auth0 and get:players permission to access.
    Sample: curl http://127.0.0.1:5432/players -H "Content-Type: application/json, Authorization: {manager_jwt or fan_jwt}"

{
    "players": [
        {
            "id": 1,
            "name": "Thomas Mueller",
            "nationality": "German",
            "team": "Bayern Muenchin"
        },
        {
            "id": 2,
            "name": "Manuel Neuer",
            "nationality": "German",
            "team": "Bayern Muenchin"
        },
        {
            "id": 3,
            "name": "Serge Gnabry",
            "nationality": "German",
            "team": "Bayern Muenchin"
        },
        {
            "id": 4,
            "name": "David Alaba",
            "nationality": "Austrian",
            "team": "Bayern Muenchin"
        },
        {
            "id": 5,
            "name": "Lionel Messi",
            "nationality": "Argentine",
            "team": "FC Barcelona"
        }
    ],
    "success": true
}

GET /players/{player_id}

    General:
        Returns a player object containing player's id, name, nationilty, rating, and team; and success value. Requires json web token from Auth0 and get:players-detail permission to access.
    Sample: curl http://127.0.0.1:5432/players/1 -H "Content-Type: application/json, Authorization: {manager_jwt}"
{
    "player": {
        "id": 1,
        "name": "Thomas Mueller",
        "nationality": "German",
        "rating": 88,
        "team": "Bayern Muenchin"
    },
    "success": true
}

GET /teams

    General:
        Returns a list of team objects containing teams's id, name, nation, and list of player objects; and success value. Requires json web token from Auth0 and get:teams permission to access.
    Sample: curl http://127.0.0.1:5432/teams -H "Content-Type: application/json, Authorization: {manager_jwt or fan_jwt}"
{
    "teams": [
        {
            "id": ,
            "name": "Bayern Muenchin",
            "nationality": "Germany",
            "players": [
                {
                    "id": 1,
                    "name": "Thomas Mueller",
                    "nationality": "German",
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 2,
                    "name": "Manuel Neuer",
                    "nationality": "German",
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 3,
                    "name": "Serge Gnabry",
                    "nationality": "German",
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 4,
                    "name": "David Alaba",
                    "nationality": "Austrian",
                    "team": "Bayern Muenchin"
                }
            ]
        },
        {
            "id": 2,
            "name": "FC Barcelona",
            "nationality": "Spain",
            "players": [
                {
                    "id": 5,
                    "name": "Lionel Messi",
                    "nationality": "Argentine",
                    "team": "FC Barcelona"
                }
            ]
        }
    ],
    "success": true
}

GET /teams/{team_id}

    General:
        Returns a team object containing a team's id, name, nationilty, rating, and list of player objects; and success value. Requires json web token from Auth0 and get:teams-detail permission to access.
    Sample: curl http://127.0.0.1:5432/players/1 -H "Content-Type: application/json, Authorization: {manager_jwt}"

{
    "team": [
        {
            "id": ,
            "name": "Bayern Muenchin",
            "nationality": "Germany",
            "rating": 92,
            "players": [
                {
                    "id": 1,
                    "name": "Thomas Mueller",
                    "nationality": "German",
                    "rating": 88,
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 2,
                    "name": "Manuel Neuer",
                    "nationality": "German",
                    "rating": 94,
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 3,
                    "name": "Serge Gnabry",
                    "nationality": "German",
                    "rating": 86,
                    "team": "Bayern Muenchin"
                },
                {
                    "id": 4,
                    "name": "David Alaba",
                    "nationality": "Austrian",
                    "rating": 88,
                    "team": "Bayern Muenchin"
                }
            ]
        }
    ],
    "success": true
}

POST /players

    General:
        Creates a new player using the submitted name, nationality, rating, and team id. Returns the  created player object and success value. Requires json web token from auth0 and post:player permission to access.
    curl http://127.0.0.1:5432/players -X POST -H "Content-Type: application/json, Authorization: {manager_jwt}" -d '{"name":"Robert Lewendawski", "nationality":"Polish", "rating":"93", 
    "team_id": 1}

{
  "player": {
        "id": 6,
        "name": "Robert Lewendawski",
        "nationality": "Polish"
        "rating": 93,
        "team": "Bayern Muenchin"
    },
    "success": true,
}

POST /teams

    General:
        Creates a new team using the submitted name, nation, and rating. Returns the created team object and success value. Requires json web token from Auth0 and post:teams permission to acess.
    curl http://127.0.0.1:5432/players -X POST -H "Content-Type: application/json, Authorization: {manager_jwt}" -d '{"name":"Dortmund", "nationality":"German", "rating":"86"}

{
  "team": {
        "id": 3,
        "name": "Dortmund",
        "nationality": "Germany"
        "rating": 86,
    },
    "success": true,
}

DELETE /players/{player_id}

    General:
        Deletes the player of the given ID if it exists. Returns the id of the deleted player and success value. Requires json web token from Auth0 and delete:player permission to acess.
    curl http://127.0.0.1:5432/players/1 -X DELETE -H "Content-Type: application/json, Authorization: {manager_jwt}"

{
    "player_id": 1,
    "success": true
}

PATCH /playesr/{player_id}

    General:
        If provided, updates the name, nationality, and/or rating of the specified player. Returns the success value and updated player object. Requires json web token from Auth0 and patch:player permission to acess.
    curl http://127.0.0.1:5432/players/1 -X PATCH -H "Content-Type: application/json, Authorization: {manager_jwt}" -d '{"rating":"87"}'

{
    "player": {
        "id": 1,
        "name": "Thomas Mueller",
        "nationality": "German",
        "rating": 87,
        "team": "Bayern Muenchin"
    },
    "success": true
}
