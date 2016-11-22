from abc import *


class UserError(Exception):
    pass


class Controller(metaclass=ABCMeta):  # TODO: Make this observable and notify a logger when "handle" is called
    """
    Controller for handling user commands. Acts as a strategy for the Server class
    """
    def handle(self, command):
        """
        Handles the command by passing it to one of the internal functions based on its type
        :param command: Command to process
        :return: Result of processing the command (varies by command type)
        """
        return {
            "GetUser": self.get_user,
            "GetUserData": self.get_user_data,
            "GetMachine": self.get_machine,
            "GetMachineData": self.get_machine_data,
            "SaveAuth": self.save_auth,
            "SaveRecord": self.save_record,
        }[command.type()](command)

    @abstractmethod
    def get_user(self, command):
        """
        Gets information about a single user
        :param command: Command object with values "user" and "password"
        :return: {"id": "user_id"}
        """
        pass

    @abstractmethod
    def get_user_data(self, command):
        """
        Gets records that this user has access to, sorted by machine
        :param command: Command object with values "user", "category", "start", and "count"
        :return: {
            "last": 1000, // Number of last record retrieved
            "records": [
            {
                "machine": "uuid",
                "data": [
                    {
                        "datetime": "ISO 8601: YYYY-MM-DDThh:mm:ss.sss",
                        "data": "category dependent data encoding"
                    },
                    ...
                ]
            },
            ...
            ]
        }
        """
        pass

    @abstractmethod
    def get_machine(self, command):
        """
        Gets information for a machine
        :param command: Command object with values "machine" and "user"
        :return: {
            "name": "user-assigned name",
            "users": [
                "user id 1",
                "user id 2",
                ...
            ]
        }
        """
        pass

    @abstractmethod
    def get_machine_data(self, command):
        """
        Gets records from a single machine if the user has access to it
        :param command: Command object with values "user", "machine", "category", "start", and "count"
        :return: {
            "last": 1000, // Number of last record retrieved
            "records": [
            {
                "datetime": "ISO 8601: YYYY-MM-DDThh:mm:ss.sss",
                "data": "category dependent data encoding"
            },
            ...
            ]
        }
        """
        pass

    @abstractmethod
    def save_auth(self, command):
        """
        Saves authorization state for the user
        :param command: Command object with values "authorize", "user", "machine"
        :return: True if saving was successful
        """
        pass

    @abstractmethod
    def save_record(self, command):
        """
        Saves a record for the machine
        :param command: Command object with values "machine", "datetime", "category", and "data"
        :return: True if saving was successful
        """
        pass
