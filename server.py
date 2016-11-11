#!/usr/bin/python3
from routing import app
from backend.server import Server

Server(app).run()
