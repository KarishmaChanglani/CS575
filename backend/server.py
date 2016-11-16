from backend.abstract.observer import Observable, Event, notify
from backend.try_class import try_notify


class Server(Observable):
    def __init__(self, routing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routing = routing

    @notify(pre="Running Server", post="Stopping Server")
    def run(self):
        self.routing.run(host="0.0.0.0", debug=False, use_reloader=False)


class ServerFactory(Observable):
    required = {'routing', }

    def __init__(self, logger, *args, **kwargs):
        if not logger:
            raise InitializationError("No logger provided for initialization")
        super().__init__(*args, **kwargs)
        self.register(logger)
        self.params = {'observers': [logger]}

    def logger(self, logger):
        if logger in self.params['observers']:
            self._error(InitializationError("Added logger twice"))
        else:
            self.params['observers'].append(logger)

    def routing(self, routing):
        self.params['routing'] = routing

    @try_notify
    def build(self):
        missing = self.required - self.params.keys()
        if missing:
            raise InitializationError("Attempted to initialize with missing parameters: {}".format(missing))
        else:
            self._notify(Event("Successfully built server", ""))
            return Server(**self.params)


class InitializationError(Exception):
    pass
