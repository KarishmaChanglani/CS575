#!/usr/bin/python3
from backend.loggers import ConsoleLogger, ConsoleErrorLogger
from backend.server import ServerFactory
from backend.routing.manager import FlaskIOManager

if __name__ == "__main__":
    sf = ServerFactory(ConsoleLogger(level=1))
    sf.routing(FlaskIOManager())
    server = sf.build()
    if server.success:
        server.value.run()
    else:
        raise server.error
