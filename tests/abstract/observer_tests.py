import unittest
from backend.abstract import observer


class TestObserver(observer.Observer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = None

    def _notify(self, event):
        self.event = event

    def pop_event(self):
        event = self.event
        self.event = None
        return event


class TestLimitedObserver(TestObserver, observer.ErrorObserver):
    pass


class TestObservable(observer.Observable):
    def execute(self, event):
        self._notify(event)

    @observer.notify(pre="pre {}")
    def decorated_pre(self, arg):
        return arg

    @observer.notify(post="post {} {}")
    def decorated_post(self, arg):
        return arg + 1


class ObserverTestCase(unittest.TestCase):
    def test_notify(self):
        test_event = observer.Event("test", "test")

        # Assert validity of this test mechanism
        ob = TestObserver()
        ob.notify(test_event)
        assert ob.pop_event() == test_event
        assert ob.pop_event() is None

        sub = TestObservable()

        # Test registration
        sub.register(ob)
        assert ob in sub.observers
        assert ob.pop_event() is None

        # Test notification
        sub.execute(test_event)
        assert ob.pop_event() == test_event

        # Test deregistration
        sub.deregister(ob)
        assert ob not in sub.observers
        assert ob.pop_event() is None
        sub.execute(test_event)
        assert ob.pop_event() is None

    def test_register_errors(self):
        ob = TestObserver()
        sub = TestObservable()

        # Error with double registration
        sub.register(ob)
        sub.register(ob)
        assert len(sub.observers) == 1
        assert isinstance(ob.pop_event().data, observer.ObservableError)

        # Error with deregistering something not registered
        sub.deregister(None)
        assert len(sub.observers) == 1
        assert isinstance(ob.pop_event().data, observer.ObservableError)

    def test_decoration(self):
        ob = TestObserver()
        sub = TestObservable()

        sub.register(ob)

        # Test pre-execution
        sub.decorated_pre(1)
        event = ob.pop_event()
        assert event.pre
        assert event.message == "pre 1"
        assert event.data == sub.decorated_pre.__qualname__

        # Test post-execution
        sub.decorated_post(1)
        event = ob.pop_event()
        assert event.post
        assert event.message == "post 2 1"
        assert event.data == sub.decorated_post.__qualname__


class LimitedObserverTestCase(unittest.TestCase):
    def test_notify(self):
        test_event = observer.ErrorEvent(AssertionError("test"))

        # Assert validity of this test mechanism
        ob = TestLimitedObserver()
        ob.notify(test_event)
        assert ob.pop_event() == test_event

        sub = TestObservable()
        sub.register(ob)

        # Test ignored
        sub.execute(observer.Event("test", "test"))
        assert ob.pop_event() is None

        # Test error
        sub.execute(test_event)
        assert ob.pop_event() == test_event

        sub.deregister(ob)
