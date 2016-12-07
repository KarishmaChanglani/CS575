import uuid
from abc import *

from flask import request, jsonify

from backend.controllers import UserError


class Route(metaclass=ABCMeta):
    """
    Represents a route taken by the user which translates into some command for the server to execute.
    :param command_cls: Command associated with this route
    :param serializer: Data serializer to translate the route's information into usable data for the command
    :param server: Server class to handle execution of the command and return a response
    """
    def __init__(self, command_cls, serializer, server):
        self.command_cls = command_cls
        self.serializer = serializer
        self.server = server

    def __call__(self, *args, **kwargs):
        """
        Executes when the route is accessed by some client. Translates and executes the proper command, and returns a
        response to the client. Arguments are passed through to the "request" function to create a request object
        :param args: Arguments sent by the caller
        :param kwargs: Keyword arguments sent by the caller
        :return: Response from the server which varies based on the command being executed and the type of application
        """
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
        """
        Packages a result object into some appropriate form of response for the subclass of Route
        :param result: The result of executing the command associated with this route on the server
        :return: Response to send to the client
        """
        pass

    @abstractmethod
    def request(self, *args, **kwargs):
        """
        Extracts the request object from the context and arguments from the client
        :param args: Arguments from the client
        :param kwargs: Keyword arguments from the client
        :return: Request object as data for the command
        """
        pass

    @abstractmethod
    def error(self, e):
        """
        Packages an error which occurred during execution as a response to the client to inform them that something went
        wrong. Can also execute other functionality to inform the admins, log the error, etc.
        :param e: Error that occurred
        :return: Response to send to the client
        """
        pass


class Serializer(metaclass=ABCMeta):
    """
    Serializer strategy used by Routes to translate between client data and server objects
    """
    @abstractmethod
    def serialize(self, data):
        """
        Transforms data from the server into data for the client
        :param data: Data from the server
        :return: Data for the client
        """
        pass

    @abstractmethod
    def deserialize(self, data):
        """
        Transforms data from the client into data for the server
        :param data: Data from the client
        :return: Data for the server
        """
        pass


class FlaskRoute(Route):
    """
    Represents a route using the Flask server library
    """
    def request(self, *args, **kwargs):
        return request

    def package(self, result, code=200):
        return result, code, {"Content-Type": "application/json"}

    def error(self, e):
        data = {"status": "failure"}
        if isinstance(e, UserError):
            data['reason'] = e.args[0]
            return self.package(self.serializer.serialize(data), 400)
        data['reason'] = repr(e)
        return self.package(self.serializer.serialize(data), 500)


class FlaskSerializer(Serializer):
    """
    Represents a JSON serializer specifically for a Flask application
    """
    def deserialize(self, data):
        json = data.get_json(force=True, silent=True)
        if json is None:
            raise UserError("Invalid json")
        return json

    def serialize(self, data):
        return jsonify(data)
