from flask import Flask, request, jsonify

from routing.manager import IOManager, NetworkRequest, IOFactory, Serializer
from server import InitializationError


class FlaskIOFactory(IOFactory):
    serializers = {
        "json": 1234
    }

    def create_serializer(self, serialization):
        if serialization not in self.serializers:
            raise InitializationError("Invalid serialization for IO Manager: " + serialization)
        return self.serializers[serialization]

    def create_manager(self, *args, **kwargs):
        return FlaskIOManager(*args, **kwargs)


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

    def add_route(self, endpoint):
        super().add_route(endpoint)

        def respond():
            return endpoint.respond(NetworkRequest(
                ip=request.remote_addr,
                port=request.environ['REMOTE_PORT'],
                route=request.environ['PATH_INFO'],
                method=request.environ['REQUEST_METHOD'],
                data=request.data,
                raw=request
            ))
        self.app.add_url_rule(endpoint.route, endpoint.route, respond)


class FlaskJsonSerializer(Serializer):
    def deserialize(self, request):
        data = request.raw.json

    def serialize(self, response):
        return jsonify(response.data)
