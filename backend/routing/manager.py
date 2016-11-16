from abc import *

from flask import Flask, request

from abstract.visitor import VisitableObservable
from try_class import try_notify


class IOManager(VisitableObservable, metaclass=ABCMeta):
    def add_route(self, route, api):
        self.add_child(api)


class FlaskIOManager(IOManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)
        self.app.config.update(dict(
            DEBUG=False,
            SECRET_KEY="dev_key",
            LOGGER_HANDLER_POLICY="never",
        ))

    def add_route(self, route, api):
        super().add_route(route, api)
        self.app.add_url_rule(route, route, lambda: api.respond(FlaskRequest(request)))


class APIManager(VisitableObservable, metaclass=ABCMeta):
    def __init__(self, serializer, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = commands
        self.serializer = serializer

    @abstractmethod
    def respond(self, request):
        pass

    @try_notify
    def deserialize(self, request):
        result = self.serializer.deserialize(request)
        if type(result) not in self.commands:
            raise SerializationError("Invalid endpoint for command: " + request)
        return result

    def serialize(self, response):
        return self.serializer.serialize(response)


class Request:
    def __init__(self, ip, port, route, method, data):
        self.ip = ip
        self.port = port
        self.route = route
        self.method = method
        self.data = data


class FlaskRequest(Request):
    def __init__(self, frequest, *args, **kwargs):
        super().__init__(
            ip=frequest.remote_addr,
            port=frequest.environ['REMOTE_PORT'],
            route=frequest.environ['PATH_INFO'],
            method=frequest.environ['REQUEST_METHOD'],
            data=frequest.data,
            *args,
            **kwargs
        )


class SerializationError(Exception):
    pass
