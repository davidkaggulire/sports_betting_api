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
        global db
        try:
            odds = {
                'id': len(db) + 1,
                'league': league,
                'home_team': home_team,
                'away_team': away_team,
                'home_team_win_odds': home_team_win_odds,
                'away_team_win_odds': away_team_win_odds,
                'draw_odds': draw_odds,
                'game_date': datetime.strptime(game_date.strip(), "%Y-%m-%d")
            }

            db.append(odds)
            print(db)
            view_odds = odds.copy()
            return True, view_odds
        except Exception as e:
            print(e)
            return False, "failed to create odds"

    def read(self, league, date_from, date_to):
        global db
        read_list = []
        date_from = datetime.strptime(date_from.strip(), "%Y-%m-%d")
        date_to = datetime.strptime(date_to.strip(), "%Y-%m-%d")
        try:
            for odd in db:
                if odd['league'] == league and odd['game_date'] >= date_from and odd['game_date'] <= date_to:
                    odd_copy = odd.copy()
                    odd_copy['game_date'] = datetime.strftime(odd_copy['game_date'], "%d-%m-%Y")
                    read_list.append(odd_copy)
            
            print(read_list)
            return True, read_list
        except Exception as e:
            print(e)
            return False, "failed to read odds"

    def update(self, odd_id, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        global db
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
                            game_date.strip(), "%Y-%m-%d")
                    })
                return True, odd
        except Exception as e:
            print(e)
            return False, "failed to update"

    def delete(self, league, home_team, away_team, game_date):
        global db
        game_date = datetime.strptime(game_date.strip(), "%Y-%m-%d")
        try:
            for odd in db:
                print(odd['game_date'])
                if odd['league'] == league and odd['home_team'] == home_team and odd['away_team'] == away_team and odd['game_date'] == game_date:
                    index = db.index(odd)
                    # delete index of odd
                    db.pop(index)
            return True, "deleted successfully"

        except Exception as e:
            print(e)
            return False, "failed to delete odds"

    def get_odd(self, odd_id):
        """get single odd"""
        global db
        odd_list = []
        try:
            for odd in db:
                if odd["id"] == int(odd_id):
                    odd_list.append(odd)
            return True, odd_list       
        except:
            return False, "Can't find odds in db"


    def find_by_field(self, league, home_team, away_team, game_date):
        """find specific field"""
        global db
        odds_list = []
        game_date = datetime.strptime(game_date.strip(), "%Y-%m-%d")
        try:
            for odds in db:
                if odds["league"] == league and odds["home_team"] == home_team and odds["away_team"] == away_team and odds["game_date"] == game_date:
                    odds_list.append(odds)
            return True, odds_list
        except:
            return False, "failed to read from db"
