from collections import namedtuple


class Command:
    def type(self):
        """
        Returns a string "type" for this command. This function should be overridden in classes whose names do not
        follow the format "Somthing...Command"
        :return: Type of command
        """
        return self.__class__.__name__[:-len("Command")]


class GetUserCommand(Command, namedtuple("GetUserCommand", ["user", "password"])):
    pass


class GetUserDataCommand(Command, namedtuple("GetUserDataCommand", ["user", "category", "start", "count"])):
    pass


class GetMachineCommand(Command, namedtuple("GetMachineCommand", ["machine", "user"])):
    pass


class GetMachineDataCommand(Command, namedtuple("GetMachineDataCommand", ["user", "machine", "category", "start", "count"])):
    pass


class SaveAuthCommand(Command, namedtuple("SaveAuthCommand", ["action", "user", "machine"])):
    @property
    def authorize(self):
        return self.action == "authorize"


class SaveRecordCommand(Command, namedtuple("SaveRecordCommand", ["machine", "datetime", "category", "data"])):
    pass
