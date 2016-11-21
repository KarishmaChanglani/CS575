from backend.commands.broker import MockBroker
from data.db_broker import DBBroker


class Server:
    def __init__(self):
        self.tasks = {}
        self.broker = DBBroker()

    def add_task(self, name, task):
        self.tasks[name] = task
        self.tasks[name].accept(self.broker)

    def get_task(self, name):
        return self.tasks[name].result

server = Server()
