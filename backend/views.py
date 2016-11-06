from pathlib import Path
from flask import render_template, send_from_directory, url_for, g
from backend import app


@app.route('/static/<path:path>')
def statics(path: Path) -> str:
    return send_from_directory('static', path)