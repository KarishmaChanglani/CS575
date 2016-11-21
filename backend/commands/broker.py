import random
from abc import *
from datetime import datetime, timedelta

from backend.commands import operations


class Broker(operations.Visitor, metaclass=ABCMeta):
    def visit(self, node):
        # The one time I wish python had real polymorphism
        ops = {
            operations.GetUser: self.visit_get_user,
            operations.GetMachine: self.visit_get_machine,
            operations.GetMachineUsers: self.visit_get_machine_users,
            operations.GetMachineRecords: self.visit_get_machine_records,
            operations.GetUserRecords: self.visit_get_user_records,
            operations.GetUserAuthorized: self.visit_get_user_authorized,
            operations.AddRecord: self.visit_add_record,
            operations.SetUserAuthorization: self.visit_set_user_authorized
        }
        for op, func in ops.items():
            if isinstance(node, op):
                func(node)

    @abstractmethod
    def visit_get_user(self, node):
        pass

    @abstractmethod
    def visit_get_machine(self, node):
        pass

    @abstractmethod
    def visit_get_machine_users(self, node):
        pass

    @abstractmethod
    def visit_get_machine_records(self, node):
        pass

    @abstractmethod
    def visit_get_user_records(self, node):
        pass

    @abstractmethod
    def visit_get_user_authorized(self, node):
        pass

    @abstractmethod
    def visit_add_record(self, node):
        pass

    @abstractmethod
    def visit_set_user_authorized(self, node):
        pass


class MockBroker(Broker):
    class FakeObj:
        def __init__(self, **kw):
            self.__dict__.update(kw)

    class FakeRecord:
        def __init__(self, timestamp, category, machine=None):
            self.timestamp = timestamp
            self.machine = machine if machine is not None else random.randrange(0, 2)
            if category == "ip":
                self.data = "{}.{}.{}.{}".format(
                    random.randrange(0, 256),
                    random.randrange(0, 256),
                    random.randrange(0, 256),
                    random.randrange(0, 256)
                )
            else:
                self.data = random.randrange(0, 100)

    def visit_get_user(self, node):
        node.result = self.FakeObj(
            username=node.username,
            password="password",
            id="id"
        )

    def visit_set_user_authorized(self, node):
        node.result = True

    def visit_get_machine(self, node):
        node.result = self.FakeObj(
            name="machine"+str(node.machine_id)
        )

    def visit_get_machine_records(self, node):
        node.result = []
        start = datetime.today()
        for i in range(node.start, node.start+node.count):
            node.result.append(self.FakeRecord(start - i*timedelta(hours=1), node.category, node.machine_id))

    def visit_add_record(self, node):
        node.result = True

    def visit_get_user_authorized(self, node):
        node.result = True

    def visit_get_user_records(self, node):
        node.result = []
        start = datetime.today()
        for i in range(node.start, node.start+node.count):
            node.result.append(self.FakeRecord(start - i*timedelta(hours=1), node.category))

    def visit_get_machine_users(self, node):
        node.result = ["user1", "user2"]
