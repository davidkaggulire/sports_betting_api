# oddschema.py

from marshmallow import Schema, fields, validate


class OddSchema(Schema):
    league = fields.String(required=True, error_messages={"required": "League is required."}, validate=validate.Length(min=1))
    home_team = fields.String(required=True, error_messages={"required": "Home_team is required."}, validate=validate.Length(min=1))
    away_team = fields.String(required=True, error_messages={"required": "Away_team is required."}, validate=validate.Length(min=1))
    home_team_win_odds = fields.Float(required=True, error_messages={"required": "Home_team_win_odds is required."})
    away_team_win_odds = fields.Float(required=True, error_messages={"required": "Away_team_win_odds is required."})
    draw_odds = fields.Float(required=True,error_messages={"required": "Draw_odds is required."})
    game_date = fields.Date(required=True, error_messages={"required": "Game_date is required."})
