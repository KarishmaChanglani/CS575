from backend.commands.broker import MockBroker


class Server:
    def __init__(self):
        self.tasks = {}
        self.broker = MockBroker()

    def add_task(self, name, task):
        self.tasks[name] = task
        self.tasks[name].accept(self.broker)

    def get_task(self, name):
        return self.tasks[name].result

server = Server()
