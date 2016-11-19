from abc import *

from abstract.visitor import VisitableObservable, Visitor, VisitableComposite
from commands.task import *
from routing.manager import SerializationError
from server import InitializationError


class CommandHandler(VisitableObservable):
    def handle(self, command):
        return self.parent.handle(command)


class Command(Visitor, VisitableComposite, metaclass=ABCMeta):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update(data)

    @staticmethod
    @abstractmethod
    def keys():
        pass

    @abstractmethod
    def tasks(self):
        pass

    def __iter__(self):
        for task in self.tasks():
            self.add_child(task)
            yield task


class CommandFactory:
    def __init__(self):
        self.commands = {}
        for command in Command.__subclasses__():
            if command.keys() in self.commands:
                raise InitializationError("Conflicting commands: {} and {}".format(
                    command.__name__,
                    self.commands[command.keys()].__name__
                ))
            self.commands[command.keys()] = command

    def build_command(self, data):
        if data.keys() not in self.commands:
            raise SerializationError("Keys do not correspond with any known command")
        return self.commands[data.keys()](**data)


class LoginError(Exception):
    pass


class LoginCommand(Command):
    @staticmethod
    def keys():
        return "username", "password"

    def tasks(self):
        yield GetUserTask()

    def visit(self, element):
        if hasattr(element, "getuser"):
            user = element.getuser(self.username)
            if user.password != self.password:
                raise LoginError("Invalid Password")
            return user
