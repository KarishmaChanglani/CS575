import uuid

from flask import Flask, request, jsonify
from flask_classy import FlaskView, route

from backend import server
from backend.operations import *

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
        task_id = uuid.uuid4()
        server.server.add_task(task_id, Login(data['user'], data['password']))
        result = server.server.get_task(task_id)
        return response(True, userid=result)

    def data(self):
        data = parse_json('user', 'category', 'start', 'count')
        task_id = uuid.uuid4()
        server.server.add_task(task_id, GetUserRecordsOperation(
            data['user'],
            data['category'],
            data['start'],
            data['count']
        ))
        result = server.server.get_task(task_id)
        return response(
            True,
            records=[{"machine": r.machine, "datetime": r.timestamp, "data": r.data} for r in result["records"]],
            last=result["last"]
        )


class MachineView(FlaskView):
    def index(self):
        data = parse_json('machine', 'user')
        task_id = uuid.uuid4()
        server.server.add_task(task_id, GetMachineOperation(data['machine'], data['user']))
        result = server.server.get_task(task_id)
        return response(True, name=result.name)

    def data(self):
        data = parse_json('machine', 'user', 'category', 'start', 'count')
        task_id = uuid.uuid4()
        server.server.add_task(task_id, GetMachineRecordsOperation(
            data['machine'],
            data['user'],
            data['category'],
            data['start'],
            data['count']
        ))
        result = server.server.get_task(task_id)
        return response(
            True,
            records=[{"machine": r.machine, "datetime": r.timestamp, "data": r.data} for r in result["records"]],
            last=result["last"]
        )


class SaveView(FlaskView):
    @route("/data/", methods=("POST",))
    def data(self):
        data = parse_json('machine', 'datetime', 'category', 'data')
        task_id = uuid.uuid4()
        server.server.add_task(task_id, SaveMachineData(
            data['machine'],
            data['datetime'],
            data['category'],
            data['data']
        ))
        result = server.server.get_task(task_id)
        return response(result)

    @route("/auth/", methods=("POST",))
    def auth(self):
        data = parse_json('action', 'user', 'machine')
        task_id = uuid.uuid4()
        server.server.add_task(task_id, SaveUserAuthorization(
            data['action'],
            data['user'],
            data['machine'],
        ))
        result = server.server.get_task(task_id)
        return response(result)


UserView.register(app)
MachineView.register(app)
SaveView.register(app)