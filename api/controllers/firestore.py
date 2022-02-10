import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from interfaces.db_interface import IDatabase
from datetime import datetime


load_dotenv()

config = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Apply credentials
cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred)

db = firestore.client()


class FireStoreDB(IDatabase):

    __instance = None

    def __init__(self):
        FireStoreDB.connect(self)

    @staticmethod
    def get_instance(re_init=False):
        if FireStoreDB.__instance is None or re_init is True:
            return FireStoreDB()
        return FireStoreDB.__instance

    def connect(self):
        print("Connecting to Firestore")
        self.odds_ref = db.collection('odds')
        return self.odds_ref

    def disconnect(self):
        print("Disconnecting from Firestore database")
        return True

    def create(
        self,
        league: str,
        home_team: str,
        away_team: str,
        home_team_win_odds: float,
        away_team_win_odds: float,
        draw_odds: float,
        game_date
    ):
        print("-Creating data in Firestore")

        try:
            odd = {
                'league': league,
                'home_team': home_team,
                'away_team': away_team,
                'home_team_win_odds': home_team_win_odds,
                'away_team_win_odds': away_team_win_odds,
                'draw_odds': draw_odds,
                'game_date': datetime.strptime(game_date.strip(), "%Y-%m-%d")
            }

            saved_odds = self.odds_ref.add(odd)
            print(saved_odds[1].id)
            added_odds = self.odds_ref.document(saved_odds[1].id).get().to_dict()

            reason = "Successfully created"
            print(reason)
            return True, added_odds
        except Exception as e:
            reason = (
                "-Failed to create data in Firestore: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def read(self, league, date_from, date_to):
        print("-Viewing data")
        # read data from database
        date_from = datetime.strptime(date_from.strip(), "%Y-%m-%d")
        date_to = datetime.strptime(date_to.strip(), "%Y-%m-%d")
        read_odds = []
        try:
            docs = self.odds_ref.where(
                'league', '==', league).where(
                'game_date', '>=', date_from).where(
                'game_date', '<=', date_to).stream()

            for doc in docs:
                print('{} => {} '.format(doc.id, doc.to_dict()))
                read_odds.append(doc.to_dict())
            reason = "-Data viewed successfully in location"
            print(reason)
            return True, read_odds
        except Exception as e:
            reason = (
                f"-Failed to read data in location {e}"
            )
            print(reason)
            return False, reason, ""

    def update(
        self,
        odd_id,
        league,
        home_team,
        away_team,
        home_team_win_odds,
        away_team_win_odds,
        draw_odds,
        game_date
    ):
        print("-Updating odds ")
        # update data from database
        try:
            updated_doc = self.odds_ref.document(odd_id).set({
                "league": league,
                "home_team": home_team,
                "away_team": away_team,
                "home_team_win_odds": home_team_win_odds,
                "away_team_win_odds": away_team_win_odds,
                "draw_odds": draw_odds,
                "game_date": datetime.strptime(game_date.strip(), "%Y-%m-%d")
            })

            reason = "-Odds updated successfully"
            print(reason)
            returned, odd = FireStoreDB.get_odd(self, odd_id)
            return True, odd
        except Exception as e:
            reason = (
                f"-Failed to update data, error- {e} "
            )
            print(reason)
            return False, reason

    def delete(self, location: str):
        print(f"-Deleting data in location {location}")
        my_query = {"_id": location}
        read_value = self.contact.find_one(my_query)

        if read_value:
            print(read_value)
            self.contact.delete_one(my_query)
            reason = f"-Data deleted successfully in location {location}"
            return True, reason
        else:
            reason = (
                f"-Failed to delete data in location {location}"
            )
            print(reason)
            return False, reason

    def get_odd(self, odd_id):
        try:
            doc = self.odds_ref.document(odd_id).get().to_dict()
            if doc:
                print(doc)
                return True, [doc]
            return False, "Odds not found"
        except Exception as e:
            return False, f"An Error Occured: {e}"