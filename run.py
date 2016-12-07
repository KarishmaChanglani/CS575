from backend.server import FlaskApplication, SimpleServer, ApplicationFactory
from backend.database import SqliteController
from backend.config import COMMAND_ROUTES

factory = ApplicationFactory()
factory.app = FlaskApplication
factory.server = SimpleServer
factory.controller = SqliteController

for endpoint, command_cls in COMMAND_ROUTES.items():
    factory.add_route(endpoint, command_cls)

app = factory.build()
app.run()
