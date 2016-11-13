import logging

from flask import Flask, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEGUB=True,
    SECRET_KEY="dev_key",
    LOGGER_HANDLER_POLICY="never",
))
app.config.from_envvar('CS575_SETTINGS', silent=True)

# Disable default logging to replace with our own
logging.getLogger('werkzeug').setLevel(100)


# This has to be here so that flask's circular importing works correctly
# noinspection PyPep8,PyUnresolvedReferences
import backend.routing.views
import backend.routing.cli
