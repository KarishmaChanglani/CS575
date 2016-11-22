from abc import *

from flask import Flask

from backend import config
from backend.controllers import Controller
from backend.routes import FlaskRoute, FlaskSerializer


class Server(metaclass=ABCMeta):
    """
    Server which processes commands. This abstractly represents the bridge between client requests and server actions
    and leaves room for potential asynchronous tasks later by using a call and response mechanism.
    :param controller: Backend strategy for executing the command
    """
    def __init__(self, controller):
        self.tasks = {}
        self.controller = controller

    @abstractmethod
    def add_task(self, name, task):
        """
        Adds a command to the list of tasks for the server to execute
        :param name: Unique task name (uuid)
        :param task: Command to execute
        """
        pass

    @abstractmethod
    def get_task(self, name):
        """
        Gets a result for the given task if it is completed, and otherwise blocks
        :param name: Name of the task (uuid)
        :return: Result of executing the command
        """
        pass


class SimpleServer(Server):
    """
    Simple linear server which adds tasks to a dictionary and lazily executes them when needed
    """
    def add_task(self, name, task):
        self.tasks[name] = task

    def get_task(self, name):
        return self.controller.handle(self.tasks.pop(name))


class Application(metaclass=ABCMeta):
    """
    Complete application object which consists of a server, a backend, and a set of routes through which it can receive
    commands.
    :param server: The server object for handling execution of commands
    """
    def __init__(self, server):
        self.server = server

    @abstractmethod
    def add_route(self, endpoint, command_cls):
        """
        Adds a route to the application. Should only be called by the application factory and not during runtime
        :param endpoint:
        :param command_cls:
        :return:
        """
        pass

    @abstractmethod
    def run(self):
        """
        Begins running the application and listening for commands
        """
        pass


class FlaskApplication(Application):
    """
    Application using the Flask library for handling HTTP requests over a port. All commands are added as "POST"
    commands to be able to receive user data as JSON.
    :param server: The server object for handling execution of commands
    """
    def __init__(self, server):
        super().__init__(server)
        self.app = Flask(__name__)

    def add_route(self, endpoint, command_cls):
        route = FlaskRoute(command_cls, FlaskSerializer(), self.server)
        self.app.add_url_rule(endpoint, endpoint, route, methods=("POST",))

    def run(self):
        self.app.run("0.0.0.0", config.PORT)


class InitializationError(Exception):
    """Represents an error raised during initial setup of the application"""
    pass


class ApplicationFactory:
    """
    Builds an application and confirms that all of the components exist and are of the correct type
    """
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
