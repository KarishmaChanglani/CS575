from backend.server import FlaskApplication, SimpleServer, ApplicationBuilder
from backend.database import SqliteController
from backend.config import COMMAND_ROUTES


class Main:
    def __init__(self, builder):
        self.builder = builder
        self.app = None

    def construct(self):
        self.builder.app = FlaskApplication
        self.builder.server = SimpleServer
        self.builder.controller = SqliteController

        for endpoint, command_cls in COMMAND_ROUTES.items():
            self.builder.add_route(endpoint, command_cls)

        self.app = self.builder.build()

    def run(self):
        self.app.run()


if __name__ == "__main__":
    main = Main(ApplicationBuilder())
    main.construct()
    main.run()
