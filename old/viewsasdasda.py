import flask
from flask import Flask, render_template, Response, request, make_response
from flask import stream_with_context
from flask import send_file, send_from_directory


def index(self):
        """Render the homepage."""
        return render_template('index.html')
        # return "Hello!"

@flask_login.login_required
def video(self, room_name):
    """Render the video page."""
    return render_template('video.html', user=room_name)
