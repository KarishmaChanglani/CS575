import unittest

from backend.abstract.observer import Event
from backend import loggers


class ConsoleTestCase(unittest.TestCase):
    def test_debug(self):
        logger = loggers.FileLogger()
        logger.notify(Event("foo", "bar"))
