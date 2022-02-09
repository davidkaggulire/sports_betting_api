# db_interface.py

from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        """connect database"""

    @abstractmethod
    def disconnect(self):
        """disconnect database"""

    @abstractmethod
    def create(self):
        """creates objects that are saved into the database"""

    @abstractmethod
    def read(self):
        """views records in database"""

    @abstractmethod
    def update(self):
        """updates record in database"""

    @abstractmethod
    def delete(self):
        """deletes record from database"""
