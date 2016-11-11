from abc import *
from functools import wraps


class Observer(metaclass=ABCMeta):
    """
    Abstract Observer class for implementing the Observer pattern
    """
    def notify(self, event):
        """
        Notifies this observer about the occurrence of some event
        :param event: subclass of Event which signals some occurrence
        """
        self._notify(event)

    @abstractmethod
    def _notify(self, event):
        """
        Internal notify procedure called by self.notify
        :param event: subclass of Event which signals some occurrence
        """
        pass


class LimitedObserver(Observer, metaclass=ABCMeta):
    """
    Observer which only observers certain types of events. Useful for subjects which broadcast a wide variety of event
    types
    """
    def notify(self, event):
        """
        Notifies this observer if the event is permitted by observed()
        :param event: subclass of Event which signals some occurrence
        """
        if self.observed(event):
            self._notify(event)

    @abstractmethod
    def observed(self, event):
        """
        Declares whether this type of event is observed by this observer
        :param event: subclass of Event which signals some occurrence
        :return: True if this event is observed
        """
        pass


class ErrorObserver(LimitedObserver, metaclass=ABCMeta):
    """
    Limited observer designed to listen only to error events
    """
    def observed(self, event):
        """
        True when event is an error event
        :param event: subclass of Event which signals some occurrence
        :return: True if this event is an error
        """
        return isinstance(event, ErrorEvent)


class Observable:
    """
    Observable class for implementing the subject in the Observer pattern
    :param observers: list of observers to subscribe to this object
    """
    def __init__(self, *args, observers=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.observers = observers or []

    def register(self, *observers):
        """
        Registers a group of observers with this object. Notifies all observers with an ObservableError if an observer
        is registered twice
        :param observers: list of observers to add
        """
        for observer in observers:
            if observer not in self.observers:
                self.observers.append(observer)
            else:
                self._error(ObservableError("Duplicate registration: {!r}".format(observer)))

    def deregister(self, *observers):
        """
        Removes observers from the list. Notifies all observers (potentially including some of those being removed) with
        an ObservableError if trying to de-register something not already registered.
        :param observers: list of observers to remove
        """
        for observer in observers:
            if observer in self.observers:
                self.observers.remove(observer)
            else:
                self._error(ObservableError("De-register non-observer: {!r}".format(observer)))

    def _notify(self, event):
        """
        Internal notify function to notify all observers of some event
        :param event: Event signalling some occurrence
        """
        for observer in self.observers:
            observer.notify(event)

    def _error(self, error):
        """
        Simplified wrapper of _notify to notify observers of some error
        :param error: Error or Exception which has occurred
        """
        self._notify(ErrorEvent(error))


def notify(pre=False, post=False):
    """
    Wrapper for Observable object to easily add observations to methods
    :param pre: Whether to notify objects before the execution of this method
    :param post: Whether to notify objects after the execution of this method
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            if pre:
                self._notify(MethodEvent(f, pre=True))
            ret = f(self, *args, **kwargs)
            if post:
                self._notify(MethodEvent(f, pre=False))
            return ret
        return wrapped
    return wrapper


class ObservableError(Exception):
    """
    An exception indicating an issue with an Observable class
    """
    pass


class Event:
    """
    A generic wrapper for some event
    :param message: message to be stored
    :param data: relevant data for the event type
    """
    def __init__(self, message, data, *args, **kwargs):
        self.message = message
        self.data = data


class ErrorEvent(Event):
    """
    A generic wrapper for an error or exception. Internally stores the exception object as the "data" attribute
    :param message: error message, or ''
    :param data: exception object
    """
    def __init__(self, error, *args, **kwargs):
        message = "" if not error.args else error.args[0]
        super().__init__(message, error)


class MethodEvent(Event):
    """
    Event relating to the execution of a function or method
    :param function: function that executed
    :param pre: Default True. Whether this event is from before the function's execution or after. The attribute 'post'
        stores the opposite of this condition.
    """
    def __init__(self, function, pre=True):
        self.pre = pre
        super().__init__(function.__name__, function.__qualname__)

    @property
    def post(self):
        return not self.pre
