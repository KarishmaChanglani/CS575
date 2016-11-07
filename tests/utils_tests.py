import unittest

from utils import Try


class TryTestCase(unittest.TestCase):
    err = AssertionError("test_error")

    @staticmethod
    def error():
        raise TryTestCase.err

    @staticmethod
    def error2(val):
        raise TryTestCase.err

    def test_success(self):
        val = 1234
        test = Try(lambda: val)
        assert test.success
        assert test.value == val
        assert not test.failure
        assert not test.error
        test.map(lambda x: x+1)
        assert test.success
        assert test.value == val + 1
        test.map(self.error2)
        assert test.failure
        assert test.error == self.err

    def test_error(self):
        test = Try(self.error)
        assert test.failure
        assert test.error == self.err
        assert not test.success
        assert not test.value
        test.map(lambda x: x+1)
        assert test.failure
        assert test.error == self.err
        test.map(self.error2)
        assert test.failure
        assert test.error == self.err
