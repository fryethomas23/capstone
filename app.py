import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Players, Teams
from auth import requires_auth, AuthError

def create_app(test_config=False):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app, test_config)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  #GET ENDPOINTS
  @app.route('/players', methods=['GET'])
  @requires_auth('get:players')
  def get_players(token):
    if type(token) == AuthError:
          print(token)
          abort(token.status_code)

    players = Players.query.all()
    player_list=[]
    for player in players:
      player_list.append(player.short())

    return jsonify({
          "success": True,
          "players": player_list
      }), 200

  @app.route('/teams', methods=['GET'])
  @requires_auth('get:teams')
  def get_teams(token):
    if type(token) == AuthError:
          print(token)
          abort(token.status_code)

    teams = Teams.query.all()
    team_list = []
    for team in teams:
      team_list.append(team.short())

    return jsonify({
        "success": True,
        "teams": team_list
      }), 200

  @app.route('/players/<int:id>', methods=['GET'])
  @requires_auth('get:players-detail')
  def get_player_detail(token, id):
    print(id)
    if type(token) == AuthError:
          print(token)
          abort(token.status_code)

    player = Players.query.get(id)

    return jsonify({
          "success": True,
          "player": player.long()
      }), 200

  @app.route('/teams/<int:id>', methods=['GET'])
  @requires_auth('get:teams-detail')
  def get_team_detail(token, id):
    if type(token) == AuthError:
      print(token)
      abort(token.status_code)

    team = Teams.query.get(id)

    return jsonify({
        "success": True,
        "team": team.long()
      }), 200

  #POST/PATCH ENDPOINTS
  @app.route('/players', methods=['POST'])
  @requires_auth('post:player')
  def post_player(token):
    if type(token) == AuthError:
        print(token)
        abort(token.status_code)

    body = request.get_json()
    name = body.get('name', None)
    nationality = body.get('nationality', None)
    rating = body.get('rating', None)
    team_id = body.get('team_id', None)

    if rating <= 0 or rating >= 100:
      abort(422)

    new_player = Players(name=name, nationality=nationality, rating=rating, 
      team_id=team_id)
    
    new_player.insert()

    return jsonify({
          "success": True,
          "player": new_player.long()
      }), 200

  @app.route('/teams', methods=['POST'])
  @requires_auth('post:team')
  def post_team(token=None):
    if type(token) == AuthError:
        print(token)
        abort(token.status_code)

    body = request.get_json()
    name = body.get('name', None)
    nation = body.get('nation', None)
    rating = body.get('rating', None)

    if rating <= 0 or rating >= 100:
      abort(422)

    new_team = Teams(name=name, nation=nation, rating=rating)
    
    new_team.insert()

    return jsonify({
          "success": True,
          "team": new_team.long()
      }), 200

  @app.route('/players/<int:id>', methods=['PATCH'])
  @requires_auth('patch:player')
  def update_player(token, id):
    if type(token) == AuthError:
        print(token)
        abort(token.status_code)

    player = Players.query.filter_by(id=id).one_or_none()
    if not player:
      abort(404)

    body = request.get_json()
    name = body.get('name', None)
    nationality = body.get('nationality', None)
    rating = body.get('rating', None)

    try:
      if name:
        player.name = name
      if nationality:
        player.nationality = nationality
      if rating:
        player.rating = rating
      player.update()
    except Exception as e:
      print(e)
      abort(422)    

    return jsonify({
          "success": True,
          "player": player.long()
      }), 200

  #DELETE ENDPOINTS
  @app.route('/players/<int:id>', methods=['DELETE'])
  @requires_auth('delete:player')
  def delete_player(token, id):
    if type(token) == AuthError:
        abort(token.status_code)

    player = Players.query.filter_by(id=id).one_or_none()
    # if not player:
    #   abort(404)

    player.delete()

    return jsonify({
          "success": True,
          "player_id": id
      }), 200


  #error handling
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not Found"
        }), 404

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized"
        }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "Forbidden"
        }), 403

  @app.errorhandler(400)
  def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

  @app.errorhandler(AuthError)
  def Authentication_error(error):
    return jsonify({
        "success": False, 
        "error": error.error['code'],
        "message": error.error['description']
        }), error.status_code


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)