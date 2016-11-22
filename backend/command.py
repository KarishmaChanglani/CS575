from collections import namedtuple


class Command:
    """
    Abstractly represents a command to the server from the client. The type of the command represents the intended
    action for the server (used since python does not have strict typing)
    """
    def type(self):
        """
        Returns a string "type" for this command. This function should be overridden in classes whose names do not
        follow the format "Somthing...Command"
        :return: Type of command
        """
        return self.__class__.__name__[:-len("Command")]


class GetUserCommand(Command, namedtuple("GetUserCommand", ["user", "password"])):
    """
    Get information about a single user
    :param user: The username
    :param password: The user's password
    """
    pass


class GetUserDataCommand(Command, namedtuple("GetUserDataCommand", ["user", "category", "start", "count"])):
    """
    Get records that the given user has access to
    :param user: The user's id
    :param category: The category of records to retrieve
    :param start: The first record to retrieve
    :param count: The number of records to retrieve
    """
    pass


class GetMachineCommand(Command, namedtuple("GetMachineCommand", ["machine", "user"])):
    """
    Get information for a given machine
    :param machine: The machine to lookup
    :param user: The user id, used to check authentication
    """
    pass


class GetMachineDataCommand(Command, namedtuple("GetMachineDataCommand", ["user", "machine", "category", "start", "count"])):
    """
    Get records from a single machine, if the user has access
    :param machine: The machine to get records for
    :param user: The user's id
    :param category: The category of records to retrieve
    :param start: The first record to retrieve
    :param count: The number of records to retrieve
    """
    pass


class SaveAuthCommand(Command, namedtuple("SaveAuthCommand", ["action", "user", "machine"])):
    """
    Save authorization state for the user
    :param action: Either 'authorize' or 'deauthorize'
    :param user: The user to authorize or deauthorize
    :param machine: The machine whose access is being modified
    """

    @property
    def authorize(self):
        """
        :return: True if action is 'authorize'
        """
        return self.action == "authorize"


class SaveRecordCommand(Command, namedtuple("SaveRecordCommand", ["machine", "datetime", "category", "data"])):
    """
    Save a record for the machine
    :param machine: The machine the record belongs to
    :param datetime: A timestamp for the record
    :param category: The type of record
    :param data: The binary record data
    """
    pass
