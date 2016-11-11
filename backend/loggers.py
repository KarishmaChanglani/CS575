import logging
from abc import *
from logging.handlers import TimedRotatingFileHandler

from backend.abstract.observer import Observer


class PrintLogger(Observer):
    def _notify(self, event):
        print(event.message, event.data)


class PyLogger(Observer):
    def __init__(self, logger, handler, fmt='%(asctime)s - %(ip)-15s %(levelname)-8s %(message)s', level=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        if not self.logger.handlers:
            self.logger.propagate = False
            handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(handler)
        if level is not None:
            self.logger.setLevel(level)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def _notify(self, event):
        self.debug(str(event.message), extra={"ip": "123.456.789.012"})


class ConsoleLogger(PyLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(
            logging.getLogger("console"),
            logging.StreamHandler(),
            *args,
            **kwargs
        )


class FileLogger(PyLogger):
    def __init__(self, file, *args, **kwargs):
        super().__init__(
            logging.getLogger("console"),
            TimedRotatingFileHandler(file, when='midnight'),
            *args,
            **kwargs
        )
