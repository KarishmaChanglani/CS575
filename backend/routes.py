import uuid
from abc import *

from flask import request, jsonify

from backend.controllers import UserError


class Route(metaclass=ABCMeta):
    def __init__(self, command_cls, serializer, server):
        self.command_cls = command_cls
        self.serializer = serializer
        self.server = server

    def __call__(self, *args, **kwargs):
        try:
            data = self.serializer.deserialize(self.request(*args, **kwargs))
        except Exception as e:
            return self.error(e)
        try:
            key_diff = set(self.command_cls._fields) - data.keys()
            if key_diff:
                raise UserError("Missing keys: {}".format(key_diff))
            # Ignores any extra keys the user sent
            command = self.command_cls(**{key: data[key] for key in data.keys() & set(self.command_cls._fields)})
        except KeyError as e:
            # This only occurs if the user is missing some key in their json, so it is a UserError
            return self.error(UserError(*e.args))
        except Exception as e:
            return self.error(e)
        try:
            task_id = uuid.uuid4()
            self.server.add_task(task_id, command)
            result = self.server.get_task(task_id)
            result['status'] = "success"
            return self.package(self.serializer.serialize(result))
        except Exception as e:
            return self.error(e)

    @abstractmethod
    def package(self, result):
        pass

    @abstractmethod
    def request(self, *args, **kwargs):
        pass

    @abstractmethod
    def error(self, e):
        pass


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, data):
        pass

    @abstractmethod
    def deserialize(self, data):
        pass


class FlaskRoute(Route):
    def request(self, *args, **kwargs):
        return request

    def package(self, result, code=200):
        return result, code, {"Content-Type": "application/json"}

    def error(self, e):
        # TODO: Remove this
        raise e
        data = {
            "status": "failure",
            "reason": repr(e)
        }
        if isinstance(e, UserError):
            return self.package(self.serializer.serialize(data), 400)
        return self.package(self.serializer.serialize(data), 500)


class FlaskSerializer(Serializer):
    def deserialize(self, data):
        json = data.get_json(force=True, silent=True)
        if json is None:
            raise UserError("Invalid json")
        return json

    def serialize(self, data):
        return jsonify(data)
