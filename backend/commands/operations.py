from abc import *


class UserError(Exception):
    pass


class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visit(self, node):
        pass


class Operation(metaclass=ABCMeta):
    @property
    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        pass


class CompositeOperation(Operation, metaclass=ABCMeta):
    def __init__(self, *args, children=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = children if children is not None else {}

    def add_child(self, name, child):
        if name in self.children or name in self.__dict__:
            raise ValueError("Conflicting name for child operation")
        self.children[name] = child

    def accept(self, visitor):
        for child in self.children.values():
            child.accept(visitor)
        visitor.visit(self)

    def __getattr__(self, item):
        if item in self.children:
            return self.children[item].result


class LeafOperation(Operation):
    def __init__(self):
        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def accept(self, visitor):
        visitor.visit(self)


class GetUser(LeafOperation):
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username


class GetMachine(LeafOperation):
    def __init__(self, machine_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id


class GetMachineUsers(LeafOperation):
    def __init__(self, machine_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id


class GetMachineRecords(LeafOperation):
    def __init__(self, machine_id, category, start, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.category = category
        self.start = start
        self.count = count


class GetUserRecords(LeafOperation):
    def __init__(self, user_id, category, start, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.category = category
        self.start = start
        self.count = count


class GetUserAuthorized(LeafOperation):
    def __init__(self, user_id, machine_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.machine_id = machine_id


class AddRecord(LeafOperation):
    def __init__(self, machine_id, timestamp, category, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.timestamp = timestamp
        self.category = category
        self.data = data


class SetUserAuthorization(LeafOperation):
    def __init__(self, authorized, user_id, machine_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authorized = authorized
        self.user_id = user_id
        self.machine_id = machine_id


class Login(CompositeOperation):
    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.add_child("user", GetUser(self.username))

    @property
    def result(self):
        if self.user.password == self.password:
            return self.user.id
        raise UserError("Invalid Password")


class AuthorizedOperation(CompositeOperation):
    @property
    def result(self):
        if not self.auth:
            raise UserError("User does not have access to machine")
        return self.auth

    def __init__(self, machine_id, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.user_id = user_id
        self.add_child("auth", GetUserAuthorized(user_id, machine_id))


class GetMachineOperation(CompositeOperation):
    def __init__(self, machine_id, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.user_id = user_id
        self.add_child("auth", AuthorizedOperation(machine_id, user_id))
        self.add_child("data", GetMachine(machine_id))

    @property
    def result(self):
        if self.auth:
            return self.data
        return None


class GetMachineRecordsOperation(CompositeOperation):
    def __init__(self, machine_id, user_id, category, start, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.user_id = user_id
        self.category = category
        self.start = start
        self.count = count
        self.add_child("auth", AuthorizedOperation(machine_id, user_id))
        self.add_child("records", GetMachineRecords(machine_id, category, start, count))

    @property
    def result(self):
        if self.auth:
            return {
                "last": self.count + self.start + len(self.records),
                "records": self.records
            }
        return None


class GetUserRecordsOperation(CompositeOperation):
    def __init__(self, user_id, category, start, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.category = category
        self.start = start
        self.count = count
        self.add_child("records", GetUserRecords(user_id, category, start, count))

    @property
    def result(self):
        return {
            "last": self.count + self.start + len(self.records),
            "records": self.records
        }


class SaveMachineData(CompositeOperation):
    def __init__(self, machine_id, timestamp, category, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_id = machine_id
        self.timestamp = timestamp
        self.category = category
        self.data = data
        self.add_child("saved", AddRecord(machine_id, timestamp, category, data))

    @property
    def result(self):
        if self.saved:
            return self.saved
        raise UserError("Unable to save record to database")


class SaveUserAuthorization(CompositeOperation):
    def __init__(self, authorized, user_id, machine_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authorized = authorized
        self.user_id = user_id
        self.machine_id = machine_id
        self.add_child("saved", SetUserAuthorization(authorized, user_id, machine_id))

    @property
    def result(self):
        if self.saved:
            return self.saved
        raise UserError("Unable to update authorization")
