API Reference

Introduction
    This project is a soccer club and player manager. Managers are able to get detailed information on players and teams, add players, delete players, and update players. Fans can view general information about players and teams. As part of the Udacity Fullstack nanodegree, this project serves as the capstone project, where skills used in the previous modules, such as data modeling, API architecture and testing, third-party authentication, code quality, documentation, and deployment, are demonstrated.


Pre-requisites and Local Development

Developers using this project should already have Python3 and pip installed on their local machines. Run the following commands in the main folder to download the dependencies:

    pip install -r requirements.txt

If local deployment is desired, The backend app can be hosted at the default, http://127.0.0.1:8080/. To run the application navigate to the main folder and run the following commands:

    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

These commands put the application in development mode and directs the application to use app.py. Development mode restarts the server when changes are made to the application and shows an interactive debugger in the console. Review flask documentation for further information.

Heroku Deployment

First, we need to create an account with Heroku, which can be done at the following:
    
    https://signup.heroku.com

After creating an account, install Heroku CLI with Homebrew by running:

    brew tap heroku/brew && brew install heroku

Alternatively Heroku CLI web download instructions can be found

    https://devcenter.heroku.com/categories/command-line

Once Heroku CLI has been downloaded, the running Heroku commands is now available. Enter the following into the terminal and then provide your authentication information:
    
    heroku login 

In order to create the Heroku app run the following in the terminal:
    
    heroku create {name_of_your_app}

The output will include a git url for your Heroku application. Copy this. Using the git url obtained previously, in terminal run the following:
    
    git remote add heroku {heroku_git_url}

Run this code in order to create a database and connect it to the application: 
    heroku addons:create heroku-postgresql:hobby-dev --app {name_of_your_application}

the following command can optionally be run to in order to check your configuration variables in Heroku.
    
    heroku config --app name_of_your_application 

DATABASE_URL and the URL of the database that was just created will be seen. In the browser, go to the Heroku Dashboard, login, and access your application's settings. Reveal the applications config variables and add all of the required environment variables for the project. Then, run the following command to push the reposity to Heroku:

    git push heroku master

Once the application is deployed, run migrations by running:    
    
    heroku run python manage.py db upgrade --app {name_of_your_application}

The application can now be opened from your Heroku Dashboard


Tests

In order to run tests run the following commands in the main folder:

    python test_app.py

All tests are kept in that file and should be maintained as updates are made to app functionality.


Getting Started

    Base URL: https://thomas-soccer-app.herokuapp.com/
    Authentication: this application requires authentication through Auth0.
        fan jwt: 
            eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTI1NTZiNGRlOTAwNjk1Y2JmNjAiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjMyODM1MDUsImV4cCI6MTYyMzI5MDcwNSwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwbGF5ZXJzIiwiZ2V0OnRlYW1zIl19.aloHQdGOzT8UXuC-Z-UJQouzY1IqV9pWuLXsd2cDHDijLz81MN3oivb2tdtd-lV6YbZv9JUQtZ9_5i4GW30PsTzG-dcBmac8KL5JHZG9ss9q1CSijPl72XnYKGl1JjX8YI6eXQM_VRBJh4Ums-8sa4TBvSVRFuUIun4QQHqDnpXajzFGvSmcTRgQclO0WY_9qRBGKWP0xFYkbUyen4gRZyHqyORlTlrXq9bDmO0vl6b659vCEUwEnVx4twhbJIA2tS3KFnTuubDVvvNDDzOTyFRuJg5ZaSOYZpJc-atytFx_77R_SxolFBeqPpquVoACZG8_W5AwHIk7VP_CEKRRxw
        
        manager jwt:        
            eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJjekZUM1VUTU02TjAzNWhZT2Z3MCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdGhvbWFzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDg0OTIyYTU5OWY4MzAwNmFkNjQ4NWYiLCJhdWQiOiJzb2NjZXIiLCJpYXQiOjE2MjMyODMzNzAsImV4cCI6MTYyMzI5MDU3MCwiYXpwIjoiWjhqVWJYUUFCM1pzNHJmVXA3eGlaZmNyd282YkFlcVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwbGF5ZXIiLCJnZXQ6cGxheWVycyIsImdldDpwbGF5ZXJzLWRldGFpbCIsImdldDp0ZWFtcyIsImdldDp0ZWFtcy1kZXRhaWwiLCJwYXRjaDpwbGF5ZXIiLCJwb3N0OnBsYXllciIsInBvc3Q6dGVhbSJdfQ.R0nSmCIfumwgYmp5VmVaM59iGeX4Bk--4qbF22JYakaQj-wApbIjynyrn0ukZg8JZhsZDcHE4IckVMHCWF2MkkccbbbLNsejcCiJPEo9hrgEWwZKrK-DC6kYkgftV_Ed6XyBH9bHgE-phnQuGmNgudiO4Ypn5N2nYImAeITJjWBXyfcD0JaJcpbLk5BLHmbSCVoCLeanIxM2tMZ1aWm1-g2Kbw_DohbG6WDl11_VoTVk4JL-dACjgVq1fWagVAfs6oZg0-djY8PAGb62iEzxeC1O6USuvthR3erCzYnObrO158E8KrtjDb3sYhUkNGceZZCpF76sUq_goKwNIMyprg


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


Deployment

