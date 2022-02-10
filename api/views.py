# views.py

from flask import Flask
from flask import Blueprint
from flask import jsonify, request
from itsdangerous import json
from api.controllers.postgresdb import PostgreSQLDatabase
from decorators.decorators import required_params
from api.controllers.inmemory import InMemoryDatabase
from schemas.oddschema import CreateSchema, DeleteSchema, ReadSchema, UpdateSchema

app = Flask(__name__)

main_bp = Blueprint(
    'main_bp', __name__,
)


@main_bp.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."


@main_bp.route('/api/v1/odds', methods=['POST'])
@required_params(CreateSchema())
def create_odds():
    form_data = request.get_json(force=True)
    print(form_data)

    league = form_data['league']
    home_team = form_data['home_team']
    away_team = form_data['away_team']
    home_team_win_odds = form_data['home_team_win_odds']
    away_team_win_odds = form_data['away_team_win_odds']
    draw_odds = form_data['draw_odds']
    game_date = form_data['game_date']

    try:
        # db = InMemoryDatabase()
        # status = db.get_instance().connect()
        # print(status)

        db = PostgreSQLDatabase()
        status = db.connect()

        created, odds = db.create(
            league,
            home_team,
            away_team,
            home_team_win_odds,
            away_team_win_odds,
            draw_odds,
            game_date
        )
        print(odds)

        if created:
            message = {
                "status": "success",
                "message": "Odds created Successfully",
                "odds": odds
            }
            return jsonify(message), 200
        else:
            message = {
                "status": "error",
                "message": "failed to create odds",
            }
            return jsonify(message), 500
    except Exception as e:
        print(e)
        error = {
            "status": "error",
            "message": "Failed to create odds"
        }
        return jsonify(error), 500


@main_bp.route('/api/v1/odds', methods=['GET'])
@required_params(ReadSchema())
def read_odds():
    form_data = request.get_json(force=True)
    print(form_data)

    league = form_data['league']
    date_range = form_data['date_range']

    # split range into individual dates
    date_from = date_range.split("to")[0].strip()
    date_to = date_range.split("to")[1].strip()

    try:
        # db = InMemoryDatabase()
        # status = db.get_instance().connect()
        # print(status)

        db = PostgreSQLDatabase()
        status = db.connect()

        read, odds = db.read(league, date_from, date_to)
        print(odds)
        if read is False:
            return jsonify({"message": "odds not found"}), 404
        if odds:
            message = {
                "message": "Odds read successfully",
                "odds": odds
            }
            return jsonify(message), 200
        else:
            message = {
                "error": "Not found"
            }
            return jsonify(message), 404

    except Exception as e:
        print(e)
        error = {
            "status": "error",
            "message": "Failed to read odds"
        }
        return jsonify(error), 500


@main_bp.route('/api/v1/odds/<int:odd_id>', methods=['PUT'])
@required_params(UpdateSchema())
def update_odd(odd_id):
    form_data = request.get_json(force=True)
    print(form_data)
    print(f"Odd_id is the {odd_id}")

    league = form_data['league']
    home_team = form_data['home_team']
    away_team = form_data['away_team']
    home_team_win_odds = form_data['home_team_win_odds']
    away_team_win_odds = form_data['away_team_win_odds']
    draw_odds = form_data['draw_odds']
    game_date = form_data['game_date']

    try:
        # db = InMemoryDatabase()
        # status = db.get_instance().connect()
        # print(status)

        db = PostgreSQLDatabase()
        status = db.connect()
        print(status)

        read, odds = db.get_odd(odd_id=odd_id)

        if not read:
            return jsonify({"message": "odds not found"}), 404
        if odds:
            updated, odd_update_list = db.update(
                odd_id,
                league,
                home_team,
                away_team,
                home_team_win_odds,
                away_team_win_odds,
                draw_odds,
                game_date
            )

            if updated:
                message = {
                    "message": "Odds updated successfully",
                    "odd_updated": odd_update_list
                }
                return jsonify(message), 200
            else:
                message = {
                    "error": "Failed to update"
                }
                return jsonify(message), 500
        else:
            return jsonify({"message": "Odds not found"}), 404
    except Exception as e:
        print(e)
        error = {
            "status": "error",
            "message": "Failed to update odds"
        }
        return jsonify(error), 500


@main_bp.route('/api/v1/odds', methods=['DELETE'])
@required_params(DeleteSchema())
def delete_odds():
    form_data = request.get_json(force=True)
    print(form_data)

    league = form_data['league']
    home_team = form_data['home_team']
    away_team = form_data['away_team']
    game_date = form_data['game_date']

    try:
        # db = InMemoryDatabase()
        # status = db.get_instance().connect()
        # print(status)

        db = PostgreSQLDatabase()
        status = db.connect()
        print(status)

        read, odds = db.find_by_field(league, home_team, away_team, game_date)
        print(odds)
        if read is False:
            return jsonify({"message": "odds not found"}), 404
        if odds:
            deleted, odds_data = db.delete(league, home_team, away_team, game_date)
            print("this is the deleted data")
            print(odds_data)
            if deleted:
                message = {
                    "message": "Odds deleted successfully",
                }
                return jsonify(message), 200
            else:
                message = {"message": "Error deleting data from database"}
                return jsonify(message), 500
        else:
            message = {"message": "Odds not found"}
            return jsonify(message), 404
    except Exception as e:
        print(e)
        error = {
            "status": "error",
            "message": "Error deleting"
        }
        return jsonify(error), 500
