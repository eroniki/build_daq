import numpy as np
import cv2
import json
import sys
import time
import os
from flask import Flask, render_template, Response, request, make_response

import flask_login
import flask

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
        # self.login_manager = flask_login.LoginManager()
        # self.login_manager.init_app(self.app)
        # self.login_manager.user_loader(self.user_loader)
        # self.login_manager.request_loader(self.request_loader)

        self.create_endpoints()

    def load_users(self):
        return self.um.read_json("users.json")

    def load_rooms(self):
        devices_data = self.um.read_json("devices.json")
        rooms = self.um.parse_rooms(devices_data)
        return rooms

    def create_endpoints(self):
        self.app.add_url_rule("/", "index", self.index)

        self.app.add_url_rule("/check_experiment/<int:id>",
                              "check_experiment",
                              self.check_experiment)

        self.app.add_url_rule("/clone/<int:id>",
                              "clone",
                              self.clone)

        self.app.add_url_rule("/list_experiments",
                              "list_experiments",
                              self.list_experiments)

        self.app.add_url_rule("/status_rooms/<room_name>",
                              "status_room",
                              self.status_room)

        self.app.add_url_rule("/status_rooms",
                              "status_rooms",
                              self.status_all_rooms)

        # self.app.add_url_rule("/login",
        #                       "login",
        #                       self.login)
        #
        # self.app.add_url_rule("/logout",
        #                       "logout",
        #                       self.logout)

        self.app.view_functions['index'] = self.index
        self.app.view_functions['check_experiment'] = self.check_experiment
        self.app.view_functions['clone'] = self.clone
        self.app.view_functions['list_experiments'] = self.list_experiments
        self.app.view_functions['status_room'] = self.status_room
        self.app.view_functions['status_rooms'] = self.status_all_rooms

        # self.app.view_functions['login'] = self.login
        # self.app.view_functions['logout'] = self.logout

    # @flask_login.login_required
    def check_experiment(self, id):
        cam_statement = str()
        for i in range(7):
            fname = os.path.join("data/", str(id), "/", str(i)+"/")
            if os.path.exists(fname):
                n = len(pd.find_images(fname))
            else:
                n = 0
            cam_statement += "Camera {i}: {n} images found! ".format(i=i, n=n)

        date = self.um.timestamp_to_date(id/1000)
        exp = {"timestamp": id,
               "date": date,
               "camera": cam_statement,
               "room": "room"}
        return render_template('experiment.html', user=exp)

    def index(self):
        return render_template('index.html')

    # @flask_login.login_required
    def clone(self, id):
        return str(id)

    def list_experiments(self):
        subfolders = self.um.list_subfolders("data/*/")
        experiments = self.um.list_experiments(subfolders)
        statement = ""
        for exp in experiments:
            try:
                date = self.um.timestamp_to_date(int(exp)/1000)
                statement += "<a href=check_experiment/{exp}>{exp} - ({date})</a><br />".format(
                    exp=exp, date=date)
            except:
                print "Skipped"
        return statement

    def status_room(self, room_name):
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0
        else:
            return "Wrong room id"
        devices = self.rooms[room_id]["devices"]
        statement_all = "{n} cameras placed here. <br />".format(n=len(devices))
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
        password = hashlib.md5(request.form.get('password', None)).hexdigest().upper()

        if email in self.users:
            if self.users[email]['password'] == password:
                user = User()
                user.id = email
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('protected'))
            else:
                return "wrong password"
        else:
            return "user not found"

        return 'Bad login'

    def logout(self):
        flask_login.logout_user()
        return 'Logged out'

    # @flask_login.login_required
    def protected():
        return 'Logged in as: ' + flask_login.current_user.id

    class User(flask_login.UserMixin):
        pass

    # @login_manager.user_loader
    def user_loader(self, email):
        if email not in self.users:
            return

        user = User()
        user.id = email
        return user

    # @login_manager.request_loader
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
#
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
#
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
# @app.route("/status/<room_name>", methods=["POST", "GET"])
# def status_cears(room_name):
#     if room_name.lower() == "cears":
#         room_id = 1
#     else:
#         room_id = 0
#     devices = app.config["rooms"][room_id]["devices"]
#     statement_all = "{n} cameras placed here. <br />".format(n=len(devices))
#     for dev_id, dev in enumerate(devices):
#         if os.path.exists(dev):
#             statement = "Device {dev_id} found. {dev}<br />".format(
#                 dev_id=dev_id, dev=dev)
#         else:
#             statement = "Device {dev_id} NOT found. {dev}<br />".format(
#                 dev_id=dev_id, dev=dev)
#         statement_all += statement
#     return statement_all
#
#
# @app.route("/status", methods=["POST", "GET"])
# def status_all():
#     statements = str()
#     for room_id in range(2):
#         print room_id
#         devices = app.config["rooms"][room_id]["devices"]
#         statement_all = "Room Name: {rm}<br />{n} cameras placed here. <br />".format(
#             rm=app.config["rooms"][room_id]["name"], n=len(devices))
#         for dev_id, dev in enumerate(devices):
#             if os.path.exists(dev):
#                 statement = "Device {dev_id} found. {dev}<br />".format(
#                     dev_id=dev_id, dev=dev)
#             else:
#                 statement = "Device {dev_id} NOT found. {dev}<br />".format(
#                     dev_id=dev_id, dev=dev)
#             statement_all += statement
#
#         statements += statement_all
#     return statements
#
#
# @app.route('/video/<room_name>', methods=['GET', 'POST'])
# def video(room_name):
#     if room_name.lower() == "cears":
#         app.config["room_id"] = 1
#     else:
#         app.config["room_id"] = 0
#     return render_template('video.html')
#
#
#
# @app.route('/video_feed')
# def video_feed():
#     room_id = app.config["room_id"]
#     if room_id is None:
#         room_id = 0
#     else:
#         room_id = int(room_id)
#     exp_id = str(int(time.time()*1000))
#     devices = app.config["rooms"][room_id]["devices"]
#     return Response(gen(VideoCamera(devices, exp_id)),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/test_camera/<cam_id>')
# def test_camera(cam_id):
#     return cam_id
#

#
# @app.route('/log')
# def log():
#     lines = tailer.tail(open('logs/status.log'), 10)
#
#     statement = ""
#
#     for line in lines:
#         statement += (line + "<br />")
#     return statement
#
#
# @app.route('/log/<int:n>')
# def log_n(n):
#     lines = tailer.tail(open('logs/status.log'), n)
#
#     statement = ""
#
#     for line in lines:
#         statement += (line + "<br />")
#     return statement
#
# #
# # @app.route('/delete_experiment/<exp_id>')
# # def delete_experiment(exp_id):
# #     u = utils.misc()
# #     folder = u.experiment_path(exp_id)
# #     u.delete_folder(folder)
# #
# #     return "OK"
#
# def gen(camera):
#     img_id = 0
#     while True:
#         frame = camera.get_all_frames(img_id)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         img_id += 1
#
#
#
#
# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return 'Logged out'
#
# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if flask.request.method == 'GET':
#         return '''
#                <form action='login' method='POST'>
#                 <input type='text' name='email' id='email' placeholder='email'/>
#                 <input type='password' name='password' id='password' placeholder='password'/>
#                 <input type='submit' name='submit'/>
#                </form>
#                '''
#
#     # email = flask.request.form['email']
#     email = request.form.get('email', None)
#     password = hashlib.md5(request.form.get('password', None)).hexdigest().upper()
#
#     print "EMAIL", email, "Pass", password, type(password)
#     if email in users:
#         if users[email]['password'] == password:
#             user = User()
#             user.id = email
#             flask_login.login_user(user)
#             return flask.redirect(flask.url_for('protected'))
#         else:
#             return "wrong password"
#     else:
#         return "user not found"
#
#     return 'Bad login'
#
#

#
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
#
#     app.run(host='0.0.0.0', debug=True)
