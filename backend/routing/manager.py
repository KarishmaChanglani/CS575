from abc import *

from abstract.observer import notify
from abstract.visitor import VisitableObservable
from commands.command import CommandHandler
from try_class import try_notify


class IOFactory(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.iomanager = self.create_manager(*args, **kwargs)

    @try_notify
    def add_route(self, route, methods, serialization, commands):
        self.iomanager.add_route(Endpoint(route, methods, self.create_serializer(serialization), commands))

    def build(self):
        return self.iomanager

    @abstractmethod
    def create_serializer(self, serialization):
        pass

    @abstractmethod
    def create_manager(self, *args, **kwargs):
        pass


class IOManager(CommandHandler):
    def add_route(self, endpoint):
        self.add_child(endpoint)


class Endpoint(CommandHandler):
    def __init__(self, route, methods, serializer, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route = route
        self.methods = methods
        self.commands = commands
        self.serializer = serializer

    @try_notify
    def deserialize(self, request):
        result = self.serializer.deserialize(request)
        if type(result) not in self.commands:
            raise SerializationError("Invalid endpoint for command: " + request)
        return result

    def serialize(self, response):
        return self.serializer.serialize(response)

    @notify(pre="Received {}", post="Response {}")
    def respond(self, request):
        data = self.deserialize(request)
        response = data.map(lambda d: self.handle(d))
        return self.serialize(response)


class Serializer(VisitableObservable, metaclass=ABCMeta):
    @abstractmethod
    def deserialize(self, request):
        pass

    @abstractmethod
    def serialize(self, response):
        pass


class Request:
    def __init__(self, route, method, data, raw):
        self.route = route
        self.method = method
        self.data = data
        self.raw = raw


class NetworkRequest(Request):
    def __init__(self, ip, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip = ip
        self.port = port


class SerializationError(Exception):
    pass
