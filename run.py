from backend.server import FlaskApplication, SimpleServer, ApplicationFactory
from backend.database import SqliteController
from backend.command import *

factory = ApplicationFactory()
factory.app = FlaskApplication
factory.server = SimpleServer
factory.controller = SqliteController

routes = {
    GetUserCommand: "/user/",
    GetUserDataCommand: "/user/data/",
    GetMachineCommand: "/machine/",
    GetMachineDataCommand: "/machine/data",
    SaveAuthCommand: "/save/auth/",
    SaveRecordCommand: "/save/data/"
}

for command_cls, endpoint in routes.items():
    factory.add_route(endpoint, command_cls)

app = factory.build()
app.run()
