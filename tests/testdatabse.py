from contextlib import closing
from collections import defaultdict

import sqlite3
import unittest

from backend import config
from backend.command import *
from backend.controllers import Controller, UserError
from backend.database import AuthorizationError, SqliteController

def raiseError():
    raise AuthorizationError("This is a test error")

class TestAuthorizationError(unittest.TestCase):

    def testAuthorizationError(self):
        with self.assertRaises(AuthorizationError) as context:
            raiseError()

        self.assertTrue('This is a test error' in str(context.exception))

class TestSqliteController(unittest.TestCase):

    config.DATABASE = 'test.db'
    def check_if_table_exists(self, table_name):
        controller = SqliteController('test.db')
        with closing(sqlite3.connect(controller.database)) as db:
            query = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", [table_name])
            data = query.fetchone()
            if data is None:
                self.assertEqual(True, False, "table doesn't exist:"+table_name)
            else:
                assert(True)

    def test_setup(self):
        self.check_if_table_exists('User')
        self.check_if_table_exists('Authorization')
        self.check_if_table_exists('Machine')
        self.check_if_table_exists('Blobs')

    def testget_user(self):
        controller = SqliteController('test.db')
        user = 1
        password = 'password'
        command = GetUserCommand(user,password)
        with closing(sqlite3.connect(controller.database)) as db:
            insert_query = db.execute("INSERT INTO User VALUES(?, ?)", [user, password])
            query = db.execute("SELECT * FROM User WHERE id = ?", [user])
            test_row = controller.get_user(command)
            if query.fetchone()[0] == test_row['id']:
                assert(True)
            else:
                assert(False)
        with self.assertRaises(UserError) as context:
            command = GetUserCommand('ssadf', password)
            test_row = controller.get_user(command)

        self.assertTrue("Invalid user ID" in str(context.exception))

    def testget_user_data_and_save(self):
        controller = SqliteController('test.db')
        command = GetUserDataSplitCommand(1,'category',0,1)
        command_auth = SaveAuthCommand('authorize', 1, 'machine')
        command_data = SaveRecordCommand("machine", "datetime", "category", "data")
        try:
            controller.save_auth(command_auth)
        except sqlite3.IntegrityError:
            pass

        try:
            controller.save_record(command_data)
        except:
            pass

        data = controller.get_user_data(command)

        for row in data['records']:
            if row["machine"] == "machine" and row["data"][0]["datetime"] == "datetime" and row["data"][0]["data"] == "data":
                self.assertTrue(True)
                return
        assert(False)

    def testget_user_data_combined(self):
        controller = SqliteController('test.db')
        command = GetUserDataCommand(1,'category',0,1)
        command_auth = SaveAuthCommand('authorize', 1, 'machine')
        command_data = SaveRecordCommand("machine", "datetime", "category", "data")
        try:
            controller.save_auth(command_auth)
        except sqlite3.IntegrityError:
            pass

        try:
            controller.save_record(command_data)
        except:
            pass

        data = controller.get_user_data_combined(command)
        for row in data['records']:
            if row['machine'] == 'machine' and row['datetime'] == 'datetime' and row['data'] == 'data':
                assert(True)
                return

        assert(False)

    def testget_machine(self):
        controller = SqliteController('test.db')
        command = GetMachineCommand('machine', 1)
        command_auth = SaveAuthCommand('authorize', 1, 'machine')
        command_data = SaveRecordCommand("machine", "datetime", "category", "data")
        try:
            controller.save_auth(command_auth)
        except sqlite3.IntegrityError:
            pass

        try:
            controller.save_record(command_data)
        except:
            pass

        data = controller.get_machine(command)
        if data["name"] == 'machine':
            assert(True)
        else:
            assert(False)

    def testget_machine_data(self):
        controller = SqliteController('test.db')
        command = GetMachineDataCommand(1, 'machine', 0, 1)
        command_auth = SaveAuthCommand('authorize', 1, 'machine')
        command_data = SaveRecordCommand("machine", "datetime", "category", "data")
        try:
            controller.save_auth(command_auth)
        except sqlite3.IntegrityError:
            pass

        try:
            controller.save_record(command_data)
        except:
            pass
        data = controller.get_machine_data(command)
        for row in data["records"]:
            if row['data'] == 'data' and row['datetime'] == 'datetime':
                assert(True)
                return

        assert(False)

    def testget_machine_all(self):
        controller = SqliteController('test.db')
        command = GetMachineDataCommand(1, 'machine', 0, 1)
        command_auth = SaveAuthCommand('authorize', 1, 'machine')
        command_data = SaveRecordCommand("machine", "datetime", "category", "data")
        try:
            controller.save_auth(command_auth)
        except sqlite3.IntegrityError:
            pass

        try:
            controller.save_record(command_data)
        except:
            pass
        data = controller.get_machine_data(command)
        #for row in data['records']:

