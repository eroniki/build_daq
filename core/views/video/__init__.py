import time
from flask import Blueprint
from flask import render_template
from flask import Response

from ...utils.experiment import experiment
from ...utils.utils import misc


from .camera import VideoCamera

video_blueprint = Blueprint('video', __name__)


@video_blueprint.route('/<room_name>')
def room(room_name):
    """Render the video page."""
    return render_template('video.html', room_name=room_name)


@video_blueprint.route('/feed/<room_name>')
def feed(room_name):
    """Run the cameras in a room."""
    if room_name.lower() == "cears":
        room_id = 1
    elif room_name.lower() == "computer_lab":
        room_id = 0
    else:
        return "Wrong Room ID is selected!"

    devices = [
        "/dev/CEARS/A",
        "/dev/CEARS/B",
        "/dev/CEARS/C",
        "/dev/CEARS/D",
        "/dev/CEARS/E",
        "/dev/CEARS/F",
        "/dev/CEARS/G",
        "/dev/CEARS/H"
    ]
    devices = [
        "/dev/cam_A",
        "/dev/CEARS/B"
    ]
    c = VideoCamera(devices, room_name)
    return Response(gen(c),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    """Camera generator for the actual tests."""
    img_id = 0
    while True:
        frame = camera.get_all_frames(img_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        img_id += 1
