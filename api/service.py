from interfaces.db_interface import IDatabase
from controllers import inmemory

class APISystem:
    # # System set up

    def __init__(self, db_service_provider: IDatabase) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup complete")

    def create(self):
        self.db.create()
