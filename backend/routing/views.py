from pathlib import Path

from flask import send_from_directory

from routing import app


@app.route('/static/<path:path>')
def statics(path: Path) -> str:
    return send_from_directory('static', path)
