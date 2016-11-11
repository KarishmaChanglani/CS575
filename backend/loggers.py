import logging
from abc import *

from backend.abstract.observer import Observer


class PrintLogger(Observer):
    def _notify(self, event):
        print(event.message, event.data)


class ConsoleLogger(Observer, metaclass=ABCMeta):
    def __init__(self, level=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("console")
        if not self.logger.hasHandlers():
            self.logger.propagate = False
            self.logger.addHandler(logging.StreamHandler())
        if level is not None:
            self.logger.setLevel(level)


class FileLogger(Observer, metaclass=ABCMeta):
    def __init__(self, file, level=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(str(file))
        if not self.logger.hasHandlers():
            self.logger.propagate = False
            self.logger.addHandler(logging.StreamHandler())
        if level is not None:
            self.logger.setLevel(level)
