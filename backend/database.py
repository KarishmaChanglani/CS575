from contextlib import closing

import sqlite3

from backend import config
from backend.controllers import Controller, UserError


class AuthorizationError(UserError):
    """Error indication the user attempted to take some action without authorization"""
    pass


class SqliteController(Controller):
    """
    Concrete controller strategy for the sqlite3 database
    :param database: The database file to connect to, or ":memory:" to use an in-memory database. Defaults to
        config.DATABASE
    """
    def __init__(self, database=config.DATABASE):
        self.database = database
        self._setup()

    def _setup(self):
        with closing(sqlite3.connect(self.database)) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS"
                " User("
                "   Id INTEGER PRIMARY KEY,"
                "   token TEXT)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS"
                " Machine("
                "   Id TEXT,"
                "   Name TEXT)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS "
                " Blobs("
                "   Machine_Id TEXT,"
                "   time_stamp TEXT,"
                "   category_name TEXT,"
                "   data BLOB,"
                "   PRIMARY KEY(Machine_Id, time_stamp, category_name))"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS"
                " Authorization("
                "   User_Id INTEGER,"
                "   Machine_Id TEXT,"
                "   PRIMARY KEY(User_Id, Machine_Id))"
            )
            db.commit()

    def get_user(self, command):
        return {"id": 1}

    def get_user_data(self, command):
        with closing(sqlite3.connect(self.database)) as db:
            query = db.execute(
                "SELECT Blobs.Machine_Id, Blobs.time_stamp, Blobs.data FROM Blobs"
                " LEFT JOIN Authorization ON Blobs.Machine_Id == Authorization.Machine_Id"
                " WHERE Authorization.User_Id = ?"
                " AND Blobs.category_name = ?"
                " ORDER BY Blobs.Machine_Id, Blobs.time_stamp"
                " LIMIT ?"
                " OFFSET ?",
                [command.user, command.category, command.count, command.start]
            )
            result = {
                "last": command.start,
                "records": []
            }
            machine = ""
            for row in query:
                result['last'] += 1
                if row[0] != machine:
                    machine = row[0]
                    result['records'].append({
                        "machine": machine,
                        "data": []
                    })
                result['records'][-1]['data'].append({
                    "datetime": row[1],
                    "data": row[2]
                })
            return result

    def get_machine(self, command):
        with closing(sqlite3.connect(self.database)) as db:
            return {
                "name": command.machine,
                "users": [row[0] for row in db.execute(
                        "SELECT User_Id from Authorization WHERE Machine_Id = ?",
                        command.machine
                )]
            }

    def get_machine_data(self, command):
        query = []
        with closing(sqlite3.connect(self.database)) as db:
            authorized = len(list(db.execute(
                "SELECT 1 "
                " FROM Authorization"
                " WHERE User_Id = ?"
                " AND Machine_Id = ?",
                [command.user, command.machine]
            )))
            if not authorized:
                raise AuthorizationError("User not authorized to access machine")
            query = db.execute(
                "SELECT time_stamp, data FROM Blobs"
                " WHERE Machine_Id = ?"
                " AND category_name = ?"
                " ORDER BY time_stamp"
                " LIMIT ?"
                " OFFSET ?",
                [command.machine, command.category, command.count, command.start]
            )
            result = {
                "last": command.start,
                "records": []
            }
            for row in query:
                result['last'] += 1
                result['records'].append({
                    "datetime": row[0],
                    "data": row[1]
                })
            return result

    def save_auth(self, command):
        try:
            with closing(sqlite3.connect(self.database)) as db:
                if command.authorize:
                    db.execute(
                        "INSERT INTO Authorization"
                        " (User_Id, Machine_Id)"
                        " VALUES (?, ?)",
                        [command.user, command.machine]
                    )
                else:
                    db.execute(
                        "DELETE FROM Authorization"
                        " WHERE User_Id = ?"
                        " AND Machine_Id = ?",
                        [command.user, command.machine]
                    )
                db.commit()
        except sqlite3.IntegrityError as e:
            pass  # This means the record already existed which really isn't a problem
        return dict()

    def save_record(self, command):
        with closing(sqlite3.connect(self.database)) as db:
            db.execute(
                "INSERT INTO Blobs"
                " (Machine_Id, category_name, time_stamp, data)"
                " VALUES (?, ?, ?, ?)",
                [command.machine, command.category, command.datetime, command.data]
            )
            db.commit()
        return dict()
