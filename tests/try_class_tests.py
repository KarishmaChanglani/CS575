import unittest

from tests.abstract.observer_tests import TestObserver
from backend.try_class import *

TEST_ERR = AssertionError("test_error")


def error():
    raise TEST_ERR


def error2(val):
    raise TEST_ERR


class SampleClass(Observable):
    @try_method
    def method_val(self):
        return 1234

    @try_method
    def method_err(self):
        raise TEST_ERR

    @try_notify
    def notify_val(self):
        return 1234

    @try_notify
    def notify_err(self):
        raise TEST_ERR

    @try_mapped
    def mapped_val(self, a, b):
        return a + b

    @try_mapped
    def mapped_err(self, a, b):
        raise TEST_ERR


class TryTestCase(unittest.TestCase):
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
        test.map(error2)
        assert test.failure
        assert test.error == TEST_ERR

    def test_error(self):
        test = Try(error)
        assert test.failure
        assert test.error == TEST_ERR
        assert not test.success
        assert not test.value
        test.map(lambda x: x+1)
        assert test.failure
        assert test.error == TEST_ERR
        test.map(error2)
        assert test.failure
        assert test.error == TEST_ERR


class ObservedTryTestCase(unittest.TestCase):
    def test_success(self):
        ob = TestObserver()
        test = ObservedTry(lambda: 1234, observers=[ob])
        assert test.success
        assert ob.pop_event() is None

    def test_error(self):
        ob = TestObserver()
        test = ObservedTry(error, observers=[ob])
        assert test.failure
        assert ob.pop_event().data == TEST_ERR

    def test_map(self):
        ob = TestObserver()
        test = ObservedTry(lambda: 1234)
        test.register(ob)
        assert ob.pop_event() is None
        assert test.success
        test.map(error2)
        assert test.failure
        assert ob.pop_event().data == TEST_ERR


class DecoratorTestCase(unittest.TestCase):
    def test_try_wrapper(self):
        test = SampleClass()
        assert test.method_val().success
        err = test.method_err()
        assert err.failure
        assert err.error == TEST_ERR

    def test_notify_wrapper(self):
        test = SampleClass()
        ob = TestObserver()
        test.register(ob)
        assert test.notify_val().success
        assert ob.pop_event() is None
        err = test.notify_err()
        assert err.failure
        assert err.error == TEST_ERR
        assert ob.pop_event().data == TEST_ERR

    def test_mapped_wrapper(self):
        test = SampleClass()
        assert test.mapped_val(1, 2).value == 3
        assert test.mapped_val(1, Try.Success(2)).value == 3
        assert test.mapped_val(1, Try.Failure(TEST_ERR)).error == TEST_ERR
        assert test.mapped_val(Try.Failure(TEST_ERR), Try.Failure(AssertionError("foo"))).error == TEST_ERR
        assert test.mapped_err(1, 2).error == TEST_ERR
        assert test.mapped_err(Try.Failure(AssertionError("foo")), 2).error != TEST_ERR
