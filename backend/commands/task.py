from abc import *

from abstract.visitor import VisitableObservable


class Task(VisitableObservable, metaclass=ABCMeta):
    @abstractmethod
    def execute(self, database):
        pass


class GetUserTask(Task):
    def execute(self, database):
        return