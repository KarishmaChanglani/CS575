import os

from flask import Flask, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEGUB=True,
    SECRET_KEY="dev_key",
    SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(app.instance_path, 'storage.db')),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_ECHO=True,
))
app.config.from_envvar('CS575_SETTINGS', silent=True)

# This has to be here so that flask's circular importing works correctly
# noinspection PyPep8,PyUnresolvedReferences
import backend.routing
import backend.abstract
