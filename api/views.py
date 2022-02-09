from email.policy import strict
from flask import Flask
from flask import Blueprint
from flask import jsonify, request, make_response
from decorators.decorators import required_params
from api.controllers.inmemory import InMemoryDatabase
from schemas.oddschema import OddSchema

app = Flask(__name__)

main_bp = Blueprint(
    'main_bp', __name__,
)

@main_bp.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."


@main_bp.route('/api/v1/odds', methods=['POST'])
@required_params(OddSchema())
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

    db = InMemoryDatabase()
    vx = db.get_instance().connect()

    print("yyyyyyyyy")
    print(vx)
    
    created, odds = db.create(league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date)
    print(odds)

    if created:
        message = {
            "status": "success",
            "message": "Odds created Successfully",
            "odds": odds
        }
        return jsonify(message), 200
    else:
        error = {
            "status": "error",
            "messages": "Failed to create odds"
        }
        return jsonify(error), 500
