#!/usr/bin/python3
from backend.loggers import PrintLogger
from backend.routing import app
from backend.server import ServerFactory

if __name__ == "__main__":
    sf = ServerFactory(PrintLogger())
    sf.routing(app)
    server = sf.build()
    if server.success:
        server.value.run()
    else:
        raise server.error
