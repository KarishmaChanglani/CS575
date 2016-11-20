from flask import Flask, request, jsonify
from flask_classy import FlaskView

import server
from operations import UserError, Login

app = Flask(__name__)


@app.errorhandler(UserError)
def user_error(e):
    return response(False, status=400, reason=e.args[0] if e.args else "")


@app.errorhandler(Exception)
def server_error(e):
    return response(False, status=500, reason=repr(e))


def parse_json(*required):
    json = request.get_json(force=True, silent=True)
    if json is None:
        raise UserError("Invalid json")
    for r in required:
        if r not in json:
            raise UserError("Missing required value: '{}'".format(r))
    return json


def response(success, status=200, **kwargs):
    ret = {"status": "success" if success else "failure"}
    ret.update(kwargs)
    return jsonify(ret), status


class UserView(FlaskView):
    def index(self):
        data = parse_json('user', 'password')
        server.server.add_task("foo", Login(data['user'], data['password']))
        result = server.server.get_task("foo")
        return response(True, userid=result)


UserView.register(app)
