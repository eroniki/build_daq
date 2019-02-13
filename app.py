"""
This module contains a class to create the REST API.

The flask_app class contains all the functions and utilities needed to provide
the REST API.
"""
import numpy as np
import cv2
import json
import sys
import time
import os

import flask
from flask import Flask, render_template, Response, request, make_response

import flask_login

from camera import VideoCamera
import experiment
from pose_detection import pose_detection
from utils import utils

import logging
from logging.handlers import RotatingFileHandler
import tailer


class flask_app(object):
    """
    This module contains a class to create the REST API.

    The flask_app class contains all the functions and utilities needed to provide
    the REST API.
    """

    def __init__(self, key):
        super(flask_app, self).__init__()
        self.um = utils.misc()

        self.users = self.load_users()
        self.rooms = self.load_rooms()
        self.app = Flask(__name__)
        self.app.secret_key = key
        self.login_manager = flask_login.LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.user_loader(self.user_loader)
        self.login_manager.unauthorized_handler(self.unauthorized_handler)
        self.login_manager.request_loader(self.request_loader)

        handler = RotatingFileHandler(
            'logs/status.log', maxBytes=10000, backupCount=99)
        formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        self.app.logger.addHandler(handler)

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)

        self.create_endpoints()

    def load_users(self):
        """Load users for authorization purposes from the json file."""
        return self.um.read_json("users.json")

    def load_rooms(self):
        """Load rooms for authorization purposes from the json file."""
        devices_data = self.um.read_json("devices.json")
        rooms = self.um.parse_rooms(devices_data)
        return rooms

    def create_endpoints(self):
        """Create API endpoints."""
        self.app.add_url_rule("/",
                              "index",
                              self.index)

        self.app.add_url_rule("/video/<room_name>",
                              "video",
                              self.video)

        self.app.add_url_rule("/video_feed/<room_name>",
                              "video_feed",
                              self.video_feed)

        self.app.add_url_rule("/label_experiment/<int:exp_id>",
                              "label_experiment",
                              self.label_experiment, methods=['POST'])

        self.app.add_url_rule("/check_experiment/<int:id>",
                              "check_experiment",
                              self.check_experiment)

        self.app.add_url_rule("/clone_experiment/<int:id>",
                              "clone_experiment",
                              self.clone_experiment)

        self.app.add_url_rule("/list_experiments",
                              "list_experiments",
                              self.list_experiments)

        self.app.add_url_rule("/delete_experiment/<exp_id>",
                              "delete_experiment",
                              self.delete_experiment)

        self.app.add_url_rule("/delete_archive/<exp_id>",
                              "delete_archive",
                              self.delete_archive)

        self.app.add_url_rule("/compress_experiment/<exp_id>",
                              "compress_experiment",
                              self.compress_experiment)

        self.app.add_url_rule("/status_rooms/<room_name>",
                              "status_room",
                              self.status_room)

        self.app.add_url_rule("/status_rooms",
                              "status_rooms",
                              self.status_all_rooms)

        self.app.add_url_rule("/login",
                              "login",
                              self.login,
                              methods=['GET', 'POST'])

        self.app.add_url_rule("/logout",
                              "logout",
                              self.logout)

        self.app.add_url_rule("/log",
                              "log",
                              self.log)

        self.app.add_url_rule("/log/<int:n>",
                              "logn",
                              self.log_n)

        self.app.add_url_rule("/test_camera/<int:camera>",
                              "test_camera",
                              self.test_camera)

        self.app.add_url_rule("/pose_detection/<exp_id>/<int:camera_id>/<int:img_id>",
                              "pose_img",
                              self.pose_img)

        self.app.add_url_rule("/pose_detection/<exp_id>/<camera_id>",
                              "pose_cam",
                              self.pose_cam)

        self.app.add_url_rule("/pose_detection/<int:exp_id>",
                              "pose_exp",
                              self.pose_exp)

        self.app.add_url_rule("/match_people/<int:exp_id>",
                              "match_people",
                              self.match_people)

        self.app.add_url_rule("/make_thumbnails/<int:exp_id>",
                              "make_thumbnails",
                              self.make_thumbnails)

        self.app.add_url_rule("/triangulate/<int:exp_id>",
                              "triangulate",
                              self.triangulate)

        self.app.view_functions['index'] = self.index
        self.app.view_functions['video'] = self.video
        self.app.view_functions['video_feed'] = self.video_feed

        self.app.view_functions['label_experiment'] = self.label_experiment
        self.app.view_functions['check_experiment'] = self.check_experiment
        self.app.view_functions['clone_experiment'] = self.clone_experiment
        self.app.view_functions['list_experiments'] = self.list_experiments
        self.app.view_functions['delete_experiment'] = self.delete_experiment
        self.app.view_functions['delete_archive'] = self.delete_archive

        self.app.view_functions['compress_experiment'] = self.compress_experiment

        self.app.view_functions['status_room'] = self.status_room
        self.app.view_functions['status_rooms'] = self.status_all_rooms

        self.app.view_functions['login'] = self.login
        self.app.view_functions['logout'] = self.logout

        self.app.view_functions['log'] = self.log
        self.app.view_functions['log_n'] = self.log_n
        self.app.view_functions['test_camera'] = self.test_camera

        self.app.view_functions['pose_img'] = self.pose_img
        self.app.view_functions['pose_cam'] = self.pose_cam
        self.app.view_functions['pose_exp'] = self.pose_exp
        self.app.view_functions['match_people'] = self.match_people
        self.app.view_functions['make_thumbnails'] = self.make_thumbnails
        self.app.view_functions['triangulate'] = self.triangulate

    def index(self):
        """Render the homepage."""
        return render_template('index.html')

    @flask_login.login_required
    def video(self, room_name):
        """Render the video page."""
        return render_template('video.html', user=room_name)

    @flask_login.login_required
    def video_feed(self, room_name):
        """Run the cameras in a room."""
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0
        else:
            return "Wrong Room ID is selected!"

        exp_id = str(int(time.time() * 1000))
        devices = self.rooms[room_id]["devices"]
        return Response(self.gen(VideoCamera(devices, room_name)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask_login.login_required
    def test_camera(self, camera):
        """Test the camera and return the image."""
        dev = list()
        for room in self.rooms:
            for device in room["devices"]:
                dev.append(device)
        return Response(self.gen_testcamera(dev[int(camera)]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self, camera):
        """Camera generator for the actual tests."""
        img_id = 0
        while True:
            frame = camera.get_all_frames(img_id)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            img_id += 1

    def gen_testcamera(self, camera):
        """Camera generator for the test_camera endpoint."""
        cap = cv2.VideoCapture(camera)
        retval, frame = cap.read()
        cap.release()
        if retval:
            cv2.imwrite('t.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        else:
            yield("Problem in camera")

    @flask_login.login_required
    def label_experiment(self, exp_id):
        """Create/Update the label of an experiment."""
        exp = experiment.experiment(new_experiment=False, ts=str(exp_id))
        label = request.form.get('label')
        exp.update_metadata(change_label=True, label=label)

        return "OK"

    @flask_login.login_required
    def check_experiment(self, id):
        """Provide details of an experiment."""
        exp = experiment.experiment(new_experiment=False, ts=id)

        start_time = time.time()
        condition = True

        while exp.metadata is None and condition:
            now = time.time()
            if now-start_time > 3:
                condition = False
                return "Experiment is not found!"
            exp = experiment.experiment(new_experiment=False, ts=id)
            time.sleep(0.01)

        cam_statement = str()
        for i in range(7):
            fname = os.path.join("data/", str(id), "/", str(i) + "/")
            if os.path.exists(fname):
                n = len(self.um.find_images(fname))
            else:
                n = 0
            cam_statement += "Camera {i}: {n} images found! ".format(i=i, n=n)

        date = self.um.timestamp_to_date(id / 1000)
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "backup", str(id)+".zip")
        is_archived = self.um.check_file_exists(f)
        if is_archived:
            img = "true.png"
        else:
            img = "false.png"

        pd_images = exp.metadata["pose_detection"].values()
        user = {"timestamp": id,
                "date": date,
                "camera": exp.metadata["number_of_cameras"],
                "n_images": exp.metadata["number_of_images"],
                "room": exp.metadata["room"],
                "label": exp.metadata["label"],
                "image": img,
                "exp": exp.metadata,
                "pose_detection_processed_images": pd_images}
        return render_template('experiment.html', user=user)

    @flask_login.login_required
    def clone_experiment(self, id):
        """Clone experiment to the cloud."""
        archive_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "backup", str(id)+".zip")
        cmd = ["rclone", "copy", archive_name, "Team_BUILD:/backup"]
        retval = self.um.run_process(cmd)
        return "Process started"

    @flask_login.login_required
    def list_experiments(self):
        """List all the experiments."""
        subfolders = self.um.list_subfolders("data/*/")
        experiment_folders = self.um.list_experiments(subfolders)
        experiments = list()
        for exp in experiment_folders:
            try:
                date = self.um.timestamp_to_date(int(exp) / 1000)
                exp_class = experiment.experiment(new_experiment=False, ts=exp)

                if "label" in exp_class.metadata:
                    label = exp_class.metadata["label"]
                else:
                    label = None

                exp_dict = {"date": date,
                            "ts": exp,
                            "label": label
                            }
                experiments.append(exp_dict)
            except:
                print "Skipped"

        return render_template('experiments.html', user=experiments)

    @flask_login.login_required
    def delete_experiment(self, exp_id):
        """Delete an experiment with the given id."""
        folder = self.um.experiment_path(exp_id)
        self.um.delete_folder(folder)

        return "OK"

    @flask_login.login_required
    def delete_archive(self, exp_id):
        """Delete the zip file."""
        archive_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "backup", str(exp_id)+".zip")
        self.um.delete_file(archive_name)

        return "OK"

    @flask_login.login_required
    def compress_experiment(self, exp_id):
        """Compress the whole data corresponding to an experiment."""
        exp_folder = self.um.experiment_path(str(exp_id))[:-1]
        exp_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), exp_folder)
        archive_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "backup", str(exp_id)+".zip")

        print exp_folder, archive_name
        retval = self.um.compress_folder_zip(exp_folder, archive_name)
        if retval:
            return "Success"
        else:
            return "Failure"

    @flask_login.login_required
    def status_room(self, room_name):
        """Check the status of a room."""
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0
        else:
            return "Wrong room id"
        devices = self.rooms[room_id]["devices"]
        statement_all = "{n} cameras placed here. <br />".format(
            n=len(devices))
        for dev_id, dev in enumerate(devices):
            if os.path.exists(dev):
                statement = "Device {dev_id} found. {dev}<br />".format(
                    dev_id=dev_id, dev=dev)
            else:
                statement = "Device {dev_id} NOT found. {dev}<br />".format(
                    dev_id=dev_id, dev=dev)
            statement_all += statement
        return statement_all

    @flask_login.login_required
    def status_all_rooms(self):
        """Check the status of all rooms."""
        statements = str()
        for room_id in range(2):
            devices = self.rooms[room_id]["devices"]
            statement_all = "Room Name: {rm}<br />{n} cameras placed here. <br />".format(
                rm=self.rooms[room_id]["name"], n=len(devices))
            for dev_id, dev in enumerate(devices):
                if os.path.exists(dev):
                    statement = "Device {dev_id} found. {dev}<br />".format(
                        dev_id=dev_id, dev=dev)
                else:
                    statement = "Device {dev_id} NOT found. {dev}<br />".format(
                        dev_id=dev_id, dev=dev)
                statement_all += statement

            statements += statement_all
        return statements

    def login(self):
        """Login to the system."""
        if flask.request.method == 'GET':
            return '''
                   <form action='login' method='POST'>
                    <input type='text' name='email' id='email' placeholder='email'/>
                    <input type='password' name='password' id='password' placeholder='password'/>
                    <input type='submit' name='submit'/>
                   </form>
                   '''

        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password = self.um.get_md5hash(password)

        print email, password

        if email in self.users:
            if self.users[email]['password'] == password:
                user = User()
                user.id = email
                flask_login.login_user(user)
                return flask.redirect("/")
            else:
                return "wrong password"
        else:
            return "user not found"

        return 'Bad login'

    def logout(self):
        """Logout from the system."""
        flask_login.logout_user()
        return 'Logged out'

    @flask_login.login_required
    def protected():
        """Show logged username."""
        return 'Logged in as: ' + flask_login.current_user.id

    def user_loader(self, email):
        """Check if the user in the user.json file."""
        if email not in self.users:
            return

        user = User()
        user.id = email
        return user

    def request_loader(self, request):
        """Handle each request."""
        email = request.form.get('email')
        if email not in self.users:
            return

        user = User()
        user.id = email

        # DO NOT ever store passwords in plaintext and always compare password
        # hashes using constant-time comparison!
        user.is_authenticated = request.form['password'] == self.users[email]['password']

        return user

    def unauthorized_handler(self):
        """If the user is unauthorized, direct him/her to the login page."""
        return flask.redirect("/login")

    def pose_img(self, exp_id, camera_id, img_id):
        """Employ pose detection on a single image."""
        pd = pose_detection()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        camera_name = os.path.basename(devices[camera_id])
        fname = os.path.join("data", exp_id, "raw",
                             camera_name, str(img_id) + ".png")
        retval = pd.detect_pose(fname)
        if isinstance(retval, str):
            return retval
        else:
            pose = retval[0]
            retval, buffer = cv2.imencode('.png', pose)
            print buffer.shape
            response = make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/png'
        return response

    def pose_cam(self, exp_id, camera_id):
        """
        Employ pose_detection on the all images with a given experiment and
        the camera id.
        """
        pd = pose_detection()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        camera_name = os.path.basename(devices[int(camera_id)])

        fname = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "data", exp_id, "raw", str(camera_name), "")
        fname_result_joint = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                          "data", exp_id, "output", "pose",
                                          str(camera_name), "")

        fname_result_img = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        "data", exp_id, "output", "img",
                                        str(camera_name), "")

        img_files = list()
        if os.path.exists(fname):
            img_files = self.um.find_images(fname)
            n = len(img_files)
            if n == 0:
                return "No images were found!"
        else:
            return "Experiment {id} was not found".format(id=exp_id)

        print "{n} number of images were found!".format(n=n)

        img_files.sort()
        for idx, fname in enumerate(img_files):

            retval = pd.detect_pose(fname)

            if isinstance(retval, str):
                continue
            else:
                joints = retval[1]
                # save joints here
                # self.um.save_json(blabla)
                exp.update_metadata(change_pd=True, pd={camera_name: idx})

        return "{n} number of images were processed!".format(n=n-1)

    def pose_exp(self, exp_id):
        """
        Given an experiment id to employ pose_detection on the whole images
        collected from all the cameras.
        """
        pd = pose_detection()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        ncamera = exp.metadata["number_of_cameras"]
        room_name = exp.metadata["room"]
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        statement = ""
        for camera_id in range(len(devices)):
            st = self.pose_cam(str(exp_id), int(camera_id)) + "<br />"
            statement += st
        return statement

    def match_people(self, exp_id):
        """Match people based on feature matching algorithm."""
        n = 99999

        return "{n} number of images were processed!".format(n=n)

    def make_thumbnails(self, exp_id):
        """Create a thumbnail from an image, which contains only one person."""
        n = 99999

        return "{n} number of images were processed!".format(n=n)

    def triangulate(self, exp_id):
        """Triangulate people's locations."""
        n = 99999

        return "{n} number of images were processed!".format(n=n)

    def log(self):
        """Return the system logs. 10 lines."""
        lines = tailer.tail(open('logs/status.log'), 10)

        statement = ""

        for line in lines:
            statement += (line + "<br />")
        return statement

    def log_n(self, n):
        """Return n number of lines from the system logs."""
        lines = tailer.tail(open('logs/status.log'), n)

        statement = ""

        for line in lines:
            statement += (line + "<br />")
        return statement


class User(flask_login.UserMixin):
    # TODO: Implement this
    pass


if __name__ == '__main__':
    pass
