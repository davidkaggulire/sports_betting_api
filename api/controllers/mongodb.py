# mongodb.py

from interfaces.db_interface import IDatabase
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# load config from a .env file
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')


class MongoNoSQLDatabase(IDatabase):
    def __init__(self) -> None:
        # creating database
        self.db: MongoClient = None

        # creating collection
        self.contact = None
        super().__init__()

    def connect(self):
        return super().connect()

    def disconnect(self):
        return super().disconnect()

    def create(self):
        return super().create()