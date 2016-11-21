from backend.commands.broker import Broker
from backend.data.Authorization_Table_Lite import Authorization_Table_Lite
from backend.data.Blob_table_Lite import Blob_Table_Lite
from backend.data.Machine_table_lite import Machine_Table_Lite
from backend.data.User_Table_Lite import User_Table_Lite

database = 'blobs.db'


class Container:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Record:
    def __init__(self, machine_id, datetime, category, data):
        self.data = data
        self.category = category
        self.timestamp = datetime
        self.machine = machine_id


class DBBroker(Broker):
    def visit_set_user_authorized(self, node):
        table = Authorization_Table_Lite(database)
        if node.authorized == "authorize":
            # Just for now
            node.result = not table.authorize(node.user_id, node.machine_id)
        table.conn.close()

    def visit_get_user_records(self, node):
        table = Blob_Table_Lite(database)
        node.result = table.get_records_user(node.start, node.count, node.user_id, node.category)
        table.conn.close()

    def visit_get_machine_users(self, node):
        table = Authorization_Table_Lite(database)
        node.result = [row['user_id'] for row in table.get_users(node.machine_id)]
        table.conn.close()

    def visit_get_user(self, node):
        table = User_Table_Lite(database)
        node.result = Container(
            username=node.username,
            password="password",
            id=1  # TODO: have actual users
        )
        table.conn.close()

    def visit_get_user_authorized(self, node):
        table = Authorization_Table_Lite(database)
        node.result = any(node.user_id == row['user_id'] for row in table.get_users(node.machine_id))
        table.conn.close()

    def visit_get_machine_records(self, node):
        table = Blob_Table_Lite(database)
        node.result = [Record(**r) for r in table.get_records(node.start, node.count, node.machine_id, node.category)]
        table.conn.close()

    def visit_get_machine(self, node):
        table = Machine_Table_Lite(database)
        node.result = Container(name=table.get_name(node.machine_id)['name'])
        table.conn.close()

    def visit_add_record(self, node):
        table = Blob_Table_Lite(database)
        # Temporary
        node.result = not table.add_record(node.machine_id, node.timestamp, node.category, node.data)
        table.conn.close()
