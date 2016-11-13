import logging
from logging.handlers import TimedRotatingFileHandler

from backend.abstract.observer import Observer, LimitedObserver, ErrorEvent


class PrintLogger(Observer):
    """
    Very basic observer/logger which just prints every event to the console
    """

    def _notify(self, event):
        print(event.message, event.data)


class PyLogger(LimitedObserver):
    """
    Adapter for the python logging library into an Observer. While this does extend the LimitedObserver, it observes
     all events by default and can be overridden by subclasses

    :param logger: the python logging handle to the specific logger
    :param handler: The handler type to be used for logging. Its format will be overridden by the fmt parameter. This
        parameter is ignored if the logger already exists and already has a handler
    :param fmt: Logging message format for this logger. Uses % style formatting
    :param level: Only logs messages at this level or greater. Overrides previous setting if using the same logger
        twice. Defaults to printing all messages
    """

    def __init__(self, logger, handler, fmt='%(asctime)s - %(ip)-15s %(levelname)-8s %(message)s', level=1, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        if not self.logger.handlers:
            self.logger.propagate = False
            handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def __getattr__(self, item):
        """
        Passes through to logger so less verbose calls can be made like "self.debug" or "self.error"
        :param item: Attribute name
        :return: Attribute value
        """
        return getattr(self.logger, item)

    def _notify(self, event):
        self.debug(str(event.message), extra={"ip": "123.456.789.012"})

    def observed(self, event):
        return True


class ConsoleLogger(PyLogger):
    """
    Observer which logs events to the console.
    :param fmt: Logging message format for this logger. Uses % style formatting
    :param level: Only logs messages at this level or greater.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            logging.getLogger("console"),
            logging.StreamHandler(),
            *args,
            **kwargs
        )


class FileLogger(PyLogger):
    """
    Observer which logs events to a file. Rotates files at midnight and automatically deletes the oldest backup,
     retaining the given number of copies.
    :param filename: Name/path of the file to log to. Can be relative or absolute
    :param backups: Number of backups to retain. A value of 0 means backups are never deleted.
    :param fmt: Logging message format for this logger. Uses % style formatting
    :param level: Only logs messages at this level or greater.
    """
    def __init__(self, filename, backups=5, *args, **kwargs):
        super().__init__(
            logging.getLogger(filename),
            TimedRotatingFileHandler(filename, when='midnight', backupCount=backups),
            *args,
            **kwargs
        )


class ConsoleErrorLogger(ConsoleLogger):
    """
    Extension of the ConsoleLogger which only logs ErrorEvents at the level of Error.
    """
    def _notify(self, event):
        self.error(event.data, extra={"ip": "123.456.789.012"})

    def observed(self, event):
        return isinstance(event, ErrorEvent)
