# postgresdb.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from interfaces.db_interface import IDatabase

load_dotenv()


class PostgreSQLDatabase(IDatabase):
    """postgresql database"""
    def __init__(self):
        pass

    __instance = None

    @staticmethod
    def get_instance(re_init=False):
        if PostgreSQLDatabase.__instance is None or re_init is True:
            return PostgreSQLDatabase()
        return PostgreSQLDatabase.__instance

    def connect(self):
        try:
            db_name = os.environ.get('DB_NAME')
            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=DB_USER,
                password=DB_PASSWORD,
                host="localhost",
                port="5432"
            )
            print(self.conn)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.dict_cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print(f"Connected to {db_name}")
        except Exception:
            print("Connection to PostgreSQL failed")
        return True

    # def disconnect(self):
    #     if self.conn:
    #         query = "DROP TABLE IF EXISTS contact"
    #         self.cur.execute(query)
    #         self.cur.close()
    #         self.conn.close()
    #         print("PostgreSQL connection is closed")
    #     return super().disconnect()

    def create_table(self):
        create_table = ("CREATE TABLE IF NOT EXISTS odds"
                        "("
                        "id serial PRIMARY KEY,"
                        "league VARCHAR (50) NOT NULL,"
                        "home_team VARCHAR (50) NOT NULL,"
                        "away_team VARCHAR (50) NOT NULL,"
                        "home_team_win_odds real NOT NULL,"
                        "away_team_win_odds real NOT NULL,"
                        "draw_odds real NOT NULL,"
                        "game_date DATE"
                        ")")

        self.cur.execute(create_table)
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
        try:
            self.create_table()

            insert_stmt = (
                """INSERT INTO odds
                (
                    league,
                    home_team,
                    away_team,
                    home_team_win_odds,
                    away_team_win_odds,
                    draw_odds,
                    game_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
            )
            record_to_insert = (
                league,
                home_team,
                away_team,
                home_team_win_odds,
                away_team_win_odds,
                draw_odds,
                game_date
            )
            record_id = self.cur.execute(insert_stmt, record_to_insert)
            count = self.cur.rowcount
            # getting record id
            record = self.cur.fetchone()
            sql_select_query = """SELECT * from odds where id=%s"""
            self.cur.execute(sql_select_query, (record,))
            # getting full record_object
            record_data = self.cur.fetchone()

            recordObject = []
            columnNames = [column[0] for column in self.cur.description]

            if record is not None:
                created_object = dict(zip(columnNames, record_data))
                recordObject.append(dict(zip(columnNames, record_data)))
                print(recordObject)
                print(count, "Record inserted successfully into Odds table")
                reason = "Data inserted into database successfully"
                return True, created_object

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table: ", error)
            reason = "failed to create data in location"
            return False, reason

    def read(self, league, date_from, date_to):
        print("Reading data from database ")
        sql_select_query = """SELECT * from odds where league=%s AND game_date>=%s AND game_date<=%s"""
        self.cur.execute(sql_select_query, (league, date_from, date_to,))
        records = self.cur.fetchall()

        insertObject = []
        columnNames = [column[0] for column in self.cur.description]

        print(records)
        # converting tuple to dictionary
        if records is not None:
            for record in records:
                insertObject.append(dict(zip(columnNames, record)))
            reason = "-Data viewed successfully from database"
            print(reason)
            return True, insertObject

        else:
            print("Error in read operation")
            reason = (
                "-Failed to read odds in database "
            )
            return False, reason

    def update(
        self,
        odd_id: int,
        league: str,
        home_team: str,
        away_team: str,
        home_team_win_odds: float,
        away_team_win_odds: float,
        draw_odds: float,
        game_date
    ):

        # Update single record now

        sql_update_query = """UPDATE odds SET league=%s, home_team=%s, away_team=%s,
                                home_team_win_odds=%s, away_team_win_odds=%s,
                                draw_odds=%s, game_date=%s
                                where id=%s
                            """
        odd_id = int(odd_id)
        data = (
            league,
            home_team,
            away_team,
            home_team_win_odds,
            away_team_win_odds,
            draw_odds,
            game_date,
            odd_id,
        )
        self.cur.execute(sql_update_query, data)

        count = self.cur.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        print(f"this is the {odd_id}")
        sql_select_query = """select * from odds where id = %s"""
        self.cur.execute(sql_select_query, (odd_id,))
        record = self.cur.fetchone()
        print(record)

        recordObject = []
        columnNames = [column[0] for column in self.cur.description]

        if record is not None:
            updated_object = dict(zip(columnNames, record))
            print(f"{updated_object} xxxxxxxxxxxxxxxxxxxxxx")
            recordObject.append(dict(zip(columnNames, record)))
            reason = "Data updated into database successfully"
            return True, updated_object

        else:
            print("Error in update operation")
            reason = (
                "-Failed to update odds in database"
            )
            return False, reason

    def delete(self, league, home_team, away_team, game_date):
        try:
            # Delete mulitple records
            sql_delete_query = """
                                DELETE FROM odds where league=%s
                                AND  home_team=%s
                                AND away_team=%s
                                AND game_date=%s
                            """
            data = (
                league,
                home_team,
                away_team,
                game_date,
            )
            self.cur.execute(sql_delete_query, data)
            count = self.cur.rowcount
            print(count, "Record deleted successfully ")
            reason = "-Data deleted successfully from database"
            print(reason)
            return True, reason
        except (Exception, psycopg2.Error) as error:
            print("Error in Delete operation", error)
            reason = "Record not found"
            print(reason)
            return False, reason

    def get_odd(self, odd_id):
        print("Table Before updating record ")
        try:
            odd_id = int(odd_id)
            sql_select_query = """select * from odds where id = %s"""
            self.cur.execute(sql_select_query, (odd_id,))
            record = self.cur.fetchone()
            print(record)
            return True, record
        except Exception as e:
            print(f"Error {e} in retrieving data")
            reason = "Record not found"
            return False, reason

    def find_by_field(self, league, home_team, away_team, game_date):
        try:
            sql_select_query = """
                    select * from odds where league=%s AND home_team=%s
                    AND away_team=%s AND game_date=%s
                """
            data = (league, home_team, away_team, game_date,)
            self.cur.execute(sql_select_query, data)
            records = self.cur.fetchall()
            print(records)
            return True, records
        except Exception as e:
            print(f"Error {e} in retrieving data")
            reason = "Records not found"
            return False, reason
