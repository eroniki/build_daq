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
from pose_detection import pose_detection
from utils import utils

import logging
from logging.handlers import RotatingFileHandler
import tailer


class flask_app(object):
    """docstring for flask_app."""

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
        return self.um.read_json("users.json")

    def load_rooms(self):
        devices_data = self.um.read_json("devices.json")
        rooms = self.um.parse_rooms(devices_data)
        return rooms

    def create_endpoints(self):
        self.app.add_url_rule("/",
                              "index",
                              self.index)

        self.app.add_url_rule("/video/<room_name>",
                              "video",
                              self.video)

        self.app.add_url_rule("/video_feed/<room_name>",
                              "video_feed",
                              self.video_feed)

        self.app.add_url_rule("/check_experiment/<int:id>",
                              "check_experiment",
                              self.check_experiment)

        self.app.add_url_rule("/clone/<int:id>",
                              "clone",
                              self.clone)

        self.app.add_url_rule("/list_experiments",
                              "list_experiments",
                              self.list_experiments)

        self.app.add_url_rule("/delete_experiment/<exp_id>",
                              "delete_experiment",
                              self.delete_experiment)

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

        self.app.add_url_rule("/log<int:n>",
                              "logn",
                              self.log_n)

        self.app.add_url_rule("/test_camera/<cam_id>",
                              "test_camera",
                              self.test_camera)

        self.app.view_functions['index'] = self.index
        self.app.view_functions['video'] = self.video
        self.app.view_functions['video_feed'] = self.video_feed
        self.app.view_functions['check_experiment'] = self.check_experiment
        self.app.view_functions['clone'] = self.clone
        self.app.view_functions['list_experiments'] = self.list_experiments
        self.app.view_functions['delete_experiment'] = self.delete_experiment
        self.app.view_functions['status_room'] = self.status_room
        self.app.view_functions['status_rooms'] = self.status_all_rooms

        self.app.view_functions['login'] = self.login
        self.app.view_functions['logout'] = self.logout

        self.app.view_functions['log'] = self.log
        self.app.view_functions['log_n'] = self.log_n

    def index(self):
        return render_template('index.html')

    def video(self, room_name):
        return render_template('video.html', user=room_name)

    def video_feed(self, room_name):
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0
        else:
            return "Wrong Room ID is selected!"

        exp_id = str(int(time.time() * 1000))
        devices = self.rooms[room_id]["devices"]
        return Response(self.gen(VideoCamera(devices, exp_id)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self, camera):
        img_id = 0
        while True:
            frame = camera.get_all_frames(img_id)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            img_id += 1

    @flask_login.login_required
    def check_experiment(self, id):
        cam_statement = str()
        for i in range(7):
            fname = os.path.join("data/", str(id), "/", str(i) + "/")
            if os.path.exists(fname):
                n = len(pd.find_images(fname))
            else:
                n = 0
            cam_statement += "Camera {i}: {n} images found! ".format(i=i, n=n)

        date = self.um.timestamp_to_date(id / 1000)
        exp = {"timestamp": id,
               "date": date,
               "camera": cam_statement,
               "room": "room"}
        return render_template('experiment.html', user=exp)

    # TODO: Implement this
    @flask_login.login_required
    def clone(self, id):
        return str(id)

    @flask_login.login_required
    def list_experiments(self):
        subfolders = self.um.list_subfolders("data/*/")
        experiments = self.um.list_experiments(subfolders)
        statement = ""
        for exp in experiments:
            try:
                date = self.um.timestamp_to_date(int(exp) / 1000)
                statement += "<a href=check_experiment/{exp}>{exp} - ({date})</a><br />".format(
                    exp=exp, date=date)
            except:
                print "Skipped"

        if statement == "":
            statement = "No experiments conducted yet!"
        return statement

    def delete_experiment(self, exp_id):
        folder = self.um.experiment_path(exp_id)
        self.um.delete_folder(folder)

        return "OK"

    def status_room(self, room_name):
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

    def status_all_rooms(self):
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
        flask_login.logout_user()
        return 'Logged out'

    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + flask_login.current_user.id

    def user_loader(self, email):
        if email not in self.users:
            return
        print "loader calisti"

        user = User()
        user.id = email
        return user

    def request_loader(self, request):
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
        return 'Unauthorized user!'

# @app.route("/pose_detection/<exp_id>/<camera_id>/<img_id>")
# def pose(self, exp_id, camera_id, img_id):
#     pd = pose_detection()
#     fname = os.path.join("data", exp_id, camera_id, img_id+".png")
#     pose = pd.detect_pose(fname)
#     if isinstance(pose, str):
#         return pose
#     else:
#         retval, buffer = cv2.imencode('.png', pose)
#         print buffer.shape
#         response = make_response(buffer.tobytes())
#         response.headers['Content-Type'] = 'image/png'
#     return response

# @app.route("/pose_detection/<exp_id>/<camera_id>")
# def pose_all_images(exp_id, camera_id):
#     pd = pose_detection()
#
#     fname = os.path.join("data/", exp_id, camera_id +"/")
#
#     if os.path.exists(fname):
#         fnames = pd.find_images(fname)
#         fnames.sort()
#         n = len(fname)
#     else:
#         n = 0
#
#     for fname in fnames:
#         pose = pd.detect_pose(fname)
#
#     return "{n} number of images were processed!".format(n=n)
#
# @app.route("/pose_detection/<int:exp_id>/<int:ncameras>")
# def pose_all(exp_id, ncameras):
#     pd = pose_detection()
#     for camera_id in range(ncameras):
#         fname = os.path.join("data/", str(exp_id), str(camera_id) +"/")
#
#         if os.path.exists(fname):
#             fnames = pd.find_images(fname)
#             fnames.sort()
#             n = len(fname)
#         else:
#             n = 0
#
#         for fname in fnames:
#             pose = pd.detect_pose(fname)
#
#     return "{n} number of images were processed!".format(n=n)
#
#
    def test_camera(self, cam_id):
        # TODO: Implement this
        return cam_id

    def log(self):
        lines = tailer.tail(open('logs/status.log'), 10)

        statement = ""

        for line in lines:
            statement += (line + "<br />")
        return statement

    def log_n(self, n):
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

# if __name__ == '__main__':
#
#
#     handler = RotatingFileHandler('logs/status.log', maxBytes=10000, backupCount=99)
#     formatter = logging.Formatter(
#         "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
#     handler.setLevel(logging.DEBUG)
#     handler.setFormatter(formatter)
#     app.logger.addHandler(handler)
#
#     log = logging.getLogger('werkzeug')
#     log.setLevel(logging.DEBUG)
#     log.addHandler(handler)
