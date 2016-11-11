from functools import wraps

from backend.abstract.observer import Observable


class Try:
    """
    Wrapper for functions which may throw errors to push error handling to later without breaking the chain of execution
    :param func: Function of 0 parameters to attempt executing
    """
    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = self.error = None
        try:
            self.value = func()
        except BaseException as e:
            self.error = e

    @property
    def success(self):
        # Keyed off of error because func could return None
        return self.error is None

    @property
    def failure(self):
        return self.error is not None

    def map(self, func):
        """
        Attempts to execute a function on the contained value, if there is one, and switch to failure if the map raised
        an error.
        :param func: Function of 1 parameter to execute on the contained value, if this is a Success object
        """
        if self.success:
            try:
                self.value = func(self.value)
            except BaseException as e:
                self.error = e

    @classmethod
    def Success(cls, value, *args, **kwargs):
        return cls(lambda: value, *args, **kwargs)

    @classmethod
    def Failure(cls, error, *args, **kwargs):
        def err(): raise error
        return cls(err, *args, **kwargs)


class ObservedTry(Try, Observable):
    """
    Mix of observable and try to notify observers if the function failed. If successive maps fail, observers will be
    notified then
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.failure:
            self._error(self.error)

    def map(self, func):
        """
        Attempts to execute a function on the contained value, if there is one, and switch to failure if the map raised
        an error. Will notify observers with error if switched from success to failure
        :param func: Function of 1 parameter to execute on the contained value, if this is a Success object
        """
        # Redundant, but necessary to not re-notify on the same error
        if self.success:
            super().map(func)
            if self.failure:
                self._error(self.error)


def try_method(f):
    """
    Decorator to wrap method execution in a Try
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        return Try(lambda: f(*args, **kwargs))
    return wrapped


def try_notify(f):
    """
    Decorator to wrap method execution in an observable try with the object's observers
    """
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        return ObservedTry(lambda: f(self, *args, **kwargs), observers=self.observers)
    return wrapped


def try_mapped(f):
    """
    Decorator to execute function only if all "Try" arguments are successes. Passes arguments through unpacked from
    their Try classes. Returns result as a Try, and only first error is kept if multiple arguments had errors.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        arg_failures = list(filter(lambda a: isinstance(a, Try) and a.failure, args))
        arg_failures += list(filter(lambda v: isinstance(v, Try) and v.failure, kwargs.values()))
        if arg_failures:
            return arg_failures[0]
        else:
            return try_method(f)(
                *(a.value if isinstance(a, Try) else a for a in args),
                **{k: (v.value if isinstance(v, Try) else v) for k, v in kwargs}
            )
    return wrapped
