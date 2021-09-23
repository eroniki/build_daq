from core.decorators import login_required
import time
from flask import Blueprint, Response, render_template
import tailer

system_blueprint = Blueprint('system', __name__)


@system_blueprint.route('/log')
def log(n=10):
    """Return the system logs. 10 lines default."""
    def generate():
        lines = tailer.tail(open('log/status.log'), n)
        statement = ""

        for line in lines:
            statement += (line + "<br />")

        yield statement
    return Response(generate(), mimetype='text')


@system_blueprint.route("/time")
def time_feed():
    def generate():
        yield str(int(time.time() * 1000))
    return Response(generate(), mimetype='text')
