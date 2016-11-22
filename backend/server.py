from abc import *

from flask import Flask

from backend import config
from backend.controllers import Controller
from backend.routes import FlaskRoute, FlaskSerializer


class Server(metaclass=ABCMeta):
    def __init__(self, controller):
        self.tasks = {}
        self.controller = controller

    @abstractmethod
    def add_task(self, name, task):
        pass

    @abstractmethod
    def get_task(self, name):
        pass


class SimpleServer(Server):
    def add_task(self, name, task):
        self.tasks[name] = task

    def get_task(self, name):
        return self.controller.handle(self.tasks[name])


class Application(metaclass=ABCMeta):
    def __init__(self, server):
        self.server = server

    @abstractmethod
    def add_route(self, endpoint, command_cls):
        pass

    @abstractmethod
    def run(self):
        pass


class FlaskApplication(Application):
    def __init__(self, server):
        super().__init__(server)
        self.app = Flask(__name__)

    def add_route(self, endpoint, command_cls):
        route = FlaskRoute(command_cls, FlaskSerializer(), self.server)
        self.app.add_url_rule(endpoint, endpoint, route, methods=("POST",))

    def run(self):
        self.app.run("0.0.0.0", config.PORT)


class InitializationError(Exception):
    pass


class ApplicationFactory:
    def __init__(self):
        self._app = None
        self._server = None
        self._controller = None
        self._routes = {}

    @property
    def app(self):
        if not self._app:
            raise InitializationError("Missing application")
        return self._app

    @app.setter
    def app(self, app):
        if not issubclass(app, Application):
            raise InitializationError("Tried to set '{}' as application")
        self._app = app

    @property
    def server(self):
        if not self._server:
            raise InitializationError("Missing server")
        return self._server

    @server.setter
    def server(self, server):
        if not issubclass(server, Server):
            raise InitializationError("Tried to set '{}' as server")
        self._server = server

    @property
    def controller(self):
        if not self._controller:
            raise InitializationError("Missing controller")
        return self._controller

    @controller.setter
    def controller(self, controller):
        if not issubclass(controller, Controller):
            raise InitializationError("Tried to set '{}' as controller")
        self._controller = controller

    def add_route(self, endpoint, command_cls):
        self._routes[endpoint] = command_cls

    def build(self):
        app = self.app(self.server(self.controller()))
        for endpoint, command in self._routes.items():
            app.add_route(endpoint, command)
        return app
