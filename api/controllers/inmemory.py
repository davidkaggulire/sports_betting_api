# inmemory.py

from interfaces.db_interface import IDatabase
from datetime import datetime

db = []


class InMemoryDatabase(IDatabase):
    def __init__(self):
        pass

    __instance = None

    @staticmethod
    def get_instance():
        if InMemoryDatabase.__instance is None:
            return InMemoryDatabase()
        return InMemoryDatabase.__instance

    def connect(self):
        print("connected to database")
        return True

    def disconnect(self):
        print("disconnecting from database")
        return super().disconnect()

    def create(self, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:
            odds = {
                'id': len(db) + 1,
                'league': league,
                'home_team': home_team,
                'away_team': away_team,
                'home_team_win_odds': home_team_win_odds,
                'away_team_win_odds': away_team_win_odds,
                'draw_odds': draw_odds,
                'game_date': datetime.strptime(game_date, "%Y-%m-%d").strftime("%d-%m-%Y")
            }

            db.append(odds)
            print(db)
            view_odds = odds.copy()
            return True, view_odds
        except Exception as e:
            print(e)
            return False, "failed to create odds"

    def read(self, league, date_from, date_to):
        read_list = []
        try:
            for odd in db:
                if odd['league'] == league and odd['date_from'] == date_from and odd['date_to'] == date_to:
                    odd_copy = odd.copy()
                    read_list.append(odd_copy)

            return True, read_list
        except Exception as e:
            print(e)
            return False, "failed to read odds"

    def update(self, odd_id, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:
            for odd in db:
                if odd['id'] == int(odd_id):
                    odd.update({
                        "league": league,
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_team_win_odds": home_team_win_odds,
                        "away_team_win_odds": away_team_win_odds,
                        "draw_odds": draw_odds,
                        "game_date": datetime.strptime(
                            game_date.strip(), "%d-%m-%Y")
                    })
            return True, odd
        except Exception as e:
            print(e)
            return False, "failed to update"

    def delete(self, league, home_team, away_team, game_date):
        try:
            for odd in db:
                if odd['league'] == league and odd['home_team'] == home_team and odd['away_team'] == away_team and odd['game_date'] == game_date:
                    db.pop(odd)
            return True, "deleted successfully"

        except Exception as e:
            print(e)
            return False, "failed to delete odds"
