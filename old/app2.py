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
import sys

import flask
from flask import Flask, render_template, Response, request, make_response
from flask import stream_with_context
from flask import send_file, send_from_directory

from flask_paginate import Pagination, get_page_args
import flask_login

# from backend import backend
# from camera import VideoCamera
# import experiment
# from pose_detection import pose_detection
# from utils.utils import misc
# from tf.tf import TFTree
# from skeleton.skeleton import people, skeleton
# import visualization
# from computer_vision import computer_vision

import logging
from logging.handlers import RotatingFileHandler
import tailer


class flask_app(backend):
    """This module contains a class to create the REST API.

    The flask_app class contains all the functions and utilities needed."""

    def __init__(self, context, key=None):
        super(flask_app, self).__init__(context, key)

        if not misc.check_folder_exists("logs"):
            misc.create_folder("logs")

        self.make_endpoint("/",
                           "index",
                           self.index)
        self.make_endpoint("/video/<room_name>",
                           "video",
                           self.video)

        self.make_endpoint("/reload_settings",
                           "reload_settings",
                           self.reload_settings)

        self.make_endpoint("/time_feed",
                           "time_feed",
                           self.time_feed)

        self.make_endpoint("/video_feed/<room_name>",
                           "video_feed",
                           self.video_feed)

        self.make_endpoint("/label_experiment/<int:exp_id>",
                           "label_experiment",
                           self.label_experiment, methods=['GET'])

        self.make_endpoint("/check_experiment/<int:id>",
                           "check_experiment",
                           self.check_experiment)

        self.make_endpoint("/clone_experiment/<int:id>",
                           "clone_experiment",
                           self.clone_experiment)

        self.make_endpoint("/list_experiments",
                           "list_experiments",
                           self.list_experiments)

        self.make_endpoint("/delete_experiment/<exp_id>",
                           "delete_experiment",
                           self.delete_experiment)

        self.make_endpoint("/delete_archive/<exp_id>",
                           "delete_archive",
                           self.delete_archive)

        self.make_endpoint("/compress_experiment/<exp_id>",
                           "compress_experiment",
                           self.compress_experiment)

        self.make_endpoint("/backup_experiment/<exp_id>",
                           "backup_experiment",
                           self.backup_experiment)

        self.make_endpoint("/status_rooms/<room_name>",
                           "status_room",
                           self.status_room)

        self.make_endpoint("/status_rooms",
                           "status_rooms",
                           self.status_all_rooms)

        self.make_endpoint("/login",
                           "login",
                           self.login,
                           methods=['GET', 'POST'])

        self.make_endpoint("/logout",
                           "logout",
                           self.logout)

        self.make_endpoint("/log",
                           "log",
                           self.log)

        self.make_endpoint("/test_camera/<int:camera>",
                           "test_camera",
                           self.test_camera)

        self.make_endpoint("/pose_detection/<exp_id>/<int:camera_id>/<int:img_id>",
                           "pose_img",
                           self.pose_img)

        self.make_endpoint("/pose_detection/<exp_id>/<camera_id>",
                           "pose_cam",
                           self.pose_cam)

        self.make_endpoint("/pose_detection/<int:exp_id>",
                           "pose_exp",
                           self.pose_exp)

        self.make_endpoint("/match_people/<int:exp_id>",
                           "match_people",
                           self.match_people)

        self.make_endpoint("/make_thumbnails/<int:exp_id>",
                           "make_thumbnails",
                           self.make_thumbnails)

        self.make_endpoint("/triangulate/<int:exp_id>",
                           "triangulate",
                           self.triangulate)

        self.make_endpoint("/draw_matchstick_frame/<int:exp_id>/<int:cam_id>/<int:frame_id>",
                           "draw_matchstick_frame",
                           self.skeletons)

        self.make_endpoint("/draw_matchsticks/<int:exp_id>/<camera_id>",
                           "draw_matchsticks",
                           self.draw_matchsticks)

        self.make_endpoint("/make_videofrom_matchsticks/<int:exp_id>/<camera_id>/<int:fps>",
                           "make_videofrom_matchsticks",
                           self.make_videofrom_matchsticks)

        self.make_endpoint("/get_matchstick_video/<int:exp_id>/<camera_id>",
                           "get_matchstick_video",
                           self.get_matchstick_video)

        self.make_endpoint("/locate_camera/<exp_id>/<left_cam_id>/<right_cam_id>/<frame_id>",
                           "locate_camera_frame",
                           self.locate_camera_frame)

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
        label = request.args.get('label')

        if len(label) == 0:
            return Response(misc.json_dumps("Label not found"),
                            status=400,
                            mimetype="application/json")

        exp.update_metadata(change_label=True, label=label)
        msg = "{id} was labeled as: {label}".format(id=exp_id, label=label)
        return Response(misc.json_dumps(msg),
                        status=200,
                        mimetype="application/json")

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
                n = len(misc.find_images(fname))
            else:
                n = 0
            cam_statement += "Camera {i}: {n} images found! ".format(i=i, n=n)

        date = misc.timestamp_to_date(id / 1000)
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "backup", str(id)+".zip")
        is_archived = misc.check_file_exists(f)
        if is_archived:
            img = "true.png"
        else:
            img = "false.png"

        try:
            label = exp.metadata["label"]
        except:
            label = None

        pd_images = exp.metadata["pose_detection"].values()
        user = {"timestamp": id,
                "date": date,
                "camera": exp.metadata["number_of_cameras"],
                "n_images": exp.metadata["number_of_images"],
                "room": exp.metadata["room"],
                "label": label,
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
        process = misc.run_process(cmd)
        return process

    @flask_login.login_required
    def list_experiments(self):
        """List all the experiments."""
        subfolders = misc.list_subfolders("data/*/")
        experiment_folders = misc.list_experiments(subfolders)
        experiments = list()
        for exp in experiment_folders:
            try:
                date = misc.timestamp_to_date(int(exp) / 1000)
                exp_class = experiment.experiment(new_experiment=False, ts=exp)

                if "label" in exp_class.metadata:
                    label = exp_class.metadata["label"]
                else:
                    label = None

                exp_dict = {"date": date, "ts": exp, "label": label}
                experiments.append(exp_dict)
            except:
                self.app.logger.info("Skipped {exp}".format(exp=exp))

        experiments.reverse()
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        total = len(experiments)
        pagination_experiments = experiments[offset:offset+per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')

        return render_template('experiments.html',
                               user=experiments,
                               pagination_experiments=pagination_experiments,
                               page=page,
                               per_page=per_page,
                               pagination=pagination)

    @flask_login.login_required
    def delete_experiment(self, exp_id):
        """Delete an experiment with the given id."""
        response_str = None
        response_code = 200
        try:
            folder = misc.experiment_path(exp_id)
            misc.delete_folder(folder)
            response_str = "Experiment {id} was deleted!".format(id=exp_id)
        except IOError as e:
            response_str = str(e)
            response_code = 400
        except Exception as e:
            response_str = "Unhandled Error Caught: {msg}".format(msg=str(e))
            response_code = 400

        return Response(misc.json_dumps(response_str),
                        status=response_code,
                        mimetype="application/json")

    @flask_login.login_required
    def delete_archive(self, exp_id):
        """Delete the zip file."""
        archive_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "backup", str(exp_id)+".zip")
        misc.delete_file(archive_name)

        return "OK"

    @flask_login.login_required
    def compress_experiment(self, exp_id):
        """Compress the whole data corresponding to an experiment."""
        exp_folder = misc.experiment_path(str(exp_id))[:-1]
        exp_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), exp_folder)
        archive_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "backup", str(exp_id)+".zip")

        self.app.logger.info(exp_folder)
        self.app.logger.info(archive_name)
        retval = misc.compress_folder_zip(exp_folder, archive_name)
        if retval:
            return "Success"
        else:
            return "Failure"

    @flask_login.login_required
    def backup_experiment(self, exp_id):
        """Compress the whole data corresponding to an experiment."""
        def generate():
            response = dict()
            try:
                comp_res = self.compress_experiment(exp_id)
                process = self.clone_experiment(exp_id)
                clon_res = ""

                while process.poll() is None:
                    clon_res = "Working"
                    response = {"compression": comp_res,
                                "cloning": clon_res}
                    yield misc.json_dumps(response)

                outs, errs = process.communicate()
                clon_res = {"out": outs, "err": errs}
                response = {"compression": comp_res,
                            "cloning": clon_res}
                yield misc.json_dumps(response)

            except Exception as e:
                response = {"error": e}
                yield misc.json_dumps(response)

        return Response(stream_with_context(generate()),
                        mimetype="application/json")

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
        self.app.logger.info(fname)
        retval = pd.detect_pose(fname)
        if isinstance(retval, str):
            return retval
        else:
            pose = retval[0]
            retval, buffer = cv2.imencode('.png', pose)
            response = make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/png'
        self.app.logger.info(response)
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
        devices.sort()
        camera_name = os.path.basename(devices[int(camera_id)])

        fname = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "data", exp_id, "raw", str(camera_name), "")
        fname_result_joint = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                          "data", exp_id, "output", "pose", "pose",
                                          str(camera_name))

        self.app.logger.info(fname_result_joint)
        try:
            misc.create_folder(fname_result_joint)
        except:
            pass

        fname_result_img = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        "data", exp_id, "output", "pose", "img",
                                        str(camera_name))

        try:
            misc.create_folder(fname_result_img)
        except:
            pass

        img_files = list()
        if os.path.exists(fname):
            img_files = misc.find_images(fname)
            n = len(img_files)
            if n == 0:
                return "No images were found!"
        else:
            return "Experiment {id} was not found".format(id=exp_id)

        st = "{n} number of images were found!".format(n=n)
        self.app.logger.info(st)
        img_files.sort()
        for idx, fname in enumerate(img_files):

            retval = pd.detect_pose(fname)

            if isinstance(retval, str):
                continue
            else:
                joints = retval[1]
                img = retval[0]
                # save joints here
                fname_img = os.path.basename(fname)
                fname_json = fname_img + ".json"
                fname_img = "{folder}/{f}".format(folder=fname_result_img,
                                                  f=fname_img)
                fname_json = "{folder}/{f}".format(folder=fname_result_joint,
                                                   f=fname_json)

                cv2.imwrite(fname_img, img)
                misc.dump_json(fname=fname_json,
                                  data=joints.tolist(),
                                  pretty=True)
                self.app.logger.info(fname_img)
                camera_name_full = "/dev/v4l/by-id/" + camera_name
                exp.update_metadata(change_pd=True, pd={camera_name_full: idx})

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

    def make_videofrom_matchsticks(self, exp_id, camera_id, fps):
        """
        """
        v = visualization.visualization()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]

        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        devices.sort()
        try:
            cam_name = os.path.basename(devices[int(camera_id)])
        except Exception as e:
            self.app.logger.info(e)
            return "No cam found sorry!"

        fcamera_path = os.path.join("/dev/v4l/by-id", cam_name)
        nframes = exp.metadata["number_of_images"][fcamera_path]
        exp_path = misc.experiment_path(str(exp_id))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        pathout = os.path.join(exp_path, "output/pose/video")

        try:
            misc.create_folder(pathout)
        except:
            pass

        pathout = os.path.join(pathout, cam_name)

        try:
            misc.create_folder(pathout)
        except:
            pass

        pathout = os.path.join(pathout, "video.avi")
        self.app.logger.info(pathout)
        out = cv2.VideoWriter(pathout, fourcc, fps, (800, 600))

        for frame_id in range(nframes):
            figure = os.path.join(exp_path,
                                  "output/pose/img",
                                  cam_name,
                                  "matchstick_" + str(frame_id) + ".png")
            self.app.logger.info(figure)
            img_ = cv2.imread(figure)

            if img_ is None:

                return "I think you forgot to draw the matchsticks!"
            cv2.resize(img_, (800, 600))
            out.write(img_)

        out.release()

        return "done"

    def get_matchstick_video(self, exp_id, camera_id):
        """
        """
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]

        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        devices.sort()
        try:
            cam_name = os.path.basename(devices[int(camera_id)])
        except Exception as e:
            self.app.logger.info(e)
            return "No cam found sorry!"

        fcamera_path = os.path.join("/dev/v4l/by-id", cam_name)
        nframes = exp.metadata["number_of_images"][fcamera_path]
        exp_path = misc.experiment_path(str(exp_id))
        pathout = os.path.join(exp_path, "output/pose/video")
        pathout = os.path.join(pathout, cam_name)

        try:
            return send_from_directory(pathout, filename="video.avi",
                                       as_attachment=True,
                                       mimetype='video/x-msvideo')
        except Exception as e:
            return str(e)

    def draw_matchsticks(self, exp_id, camera_id):
        """
        """
        v = visualization.visualization()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]

        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        devices.sort()
        try:
            cam_name = os.path.basename(devices[int(camera_id)])
        except Exception as e:
            self.app.logger.info(e)
            return "No cam found sorry!"

        fcamera_path = os.path.join("/dev/v4l/by-id", cam_name)
        nframes = exp.metadata["number_of_images"][fcamera_path]
        ret_combined = ""
        for frame_id in range(nframes):
            ret = self.skeletons(exp_id, camera_id, frame_id)
            ret_combined += "<br>" + ret
        return ret_combined

    def skeletons(self, exp_id, cam_id, frame_id):
        """Test skeletons."""
        visualizer = visualization.visualization()
        exp = experiment.experiment(new_experiment=False, ts=exp_id)
        room_name = exp.metadata["room"]
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        devices.sort()
        try:
            cam_name = os.path.basename(devices[int(cam_id)])
        except:
            return "No cam found sorry!"

        exp_path = misc.experiment_path(str(exp_id))
        pose_detection_result = "output/pose"
        json = "pose"
        img = "img"
        fname = os.path.join(exp_path,
                             pose_detection_result,
                             json,
                             cam_name,
                             str(frame_id)+".png.json")

        output_fname = os.path.join(exp_path,
                                    pose_detection_result,
                                    img,
                                    cam_name,
                                    "matchstick_" + str(frame_id) + ".png")
        self.app.logger.info(fname)

        if misc.check_file_exists(fname):
            json_data = misc.read_json(fname)
            people_in_frame = people(json_data, frame_id)
            visualizer.draw_matchsticks(people_in_frame, output_fname)
            npeople = str(len(people_in_frame.list))
        else:
            npeople = 0

        return "Number of people drawn: {n}".format(n=npeople)

    def triangulate(self, exp_id):
        """Triangulate people's locations."""
        n = 99999

        return "{n} number of images were processed!".format(n=n)

    def log(self, n=10):
        """Return the system logs. 10 lines default."""
        def generate():
            lines = tailer.tail(open('logs/status.log'), n)
            statement = ""

            for line in lines:
                statement += (line + "<br />")

            yield statement
        return Response(generate(), mimetype='text')

    @flask_login.login_required
    def reload_settings(self):
        return flask.jsonify({"Rooms": self.load_rooms(),
                              "Users": self.load_users()})

    def time_feed(self):
        def generate():
            yield str(int(time.time() * 1000))
        return Response(generate(), mimetype='text')

    @flask_login.login_required
    def locate_camera_frame(self, exp_id, left_cam_id, right_cam_id, frame_id):
        """Locate the camera with respect to the checkerboard."""
        return Response(self.gen_locate_camera_frame(exp_id,
                                                     left_cam_id, right_cam_id,
                                                     frame_id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen_locate_camera_frame(self, exp_id, left_cam_id, right_cam_id, frame_id):
        """Camera generator for the test_camera endpoint."""
        exp = experiment.experiment(new_experiment=False, ts=str(exp_id))
        room_name = exp.metadata["room"]
        if room_name.lower() == "cears":
            room_id = 1
        elif room_name.lower() == "computer_lab":
            room_id = 0

        devices = self.rooms[room_id]["devices"]
        devices.sort()

        fname = str(frame_id) + ".png"

        l_camera_name = os.path.basename(devices[int(left_cam_id)])
        r_camera_name = os.path.basename(devices[int(right_cam_id)])

        path_l = os.path.join(misc.experiment_path(exp_id), "raw", l_camera_name, fname)  # noqa: E501

        path_r = os.path.join(misc.experiment_path(exp_id), "raw", r_camera_name, fname)  # noqa: E501

        frame_l = cv2.imread(path_l, )
        frame_r = cv2.imread(path_r, )

        retval = True

        if frame_l is None:
            frame_l = cv2.imread("flask_app/static/task.jpg")
            ret_val = False

        if frame_r is None:
            frame_r = cv2.imread("flask_app/static/task.jpg")
            ret_val = False

        pattern_shape = (9, 6)  # TODO: CHECK THIS
        grid_size = 30  # TODO: CHECK THIS
        text_l, corners_l, canvas_l, R_l, t_l = computer_vision.calculate_camera_pose(frame_l, self.K, self.d, pattern_shape=pattern_shape, grid_size=grid_size)  # noqa: E501
        text_r, corners_r, canvas_r, R_r, t_r = computer_vision.calculate_camera_pose(frame_r, self.K, self.d, pattern_shape=pattern_shape, grid_size=grid_size)  # noqa: E501

        T_l = np.eye(4)
        T_r = np.eye(4)
        if R_l is not None and R_r is not None:
            T_l[0:3, 0:3] = R_l
            T_r[0:3, 0:3] = R_r
            T_l[0:3, 3] = t_l.ravel()
            T_r[0:3, 3] = t_r.ravel()

            T_l = np.eye(4)
            T_r = np.linalg.inv(T_l).dot(T_r)

        canvas = np.hstack([canvas_l, canvas_r])

        text = "Left: " + text_l + " Right: " + text_r
        cv2.putText(canvas, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 0, 255), lineType=cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', canvas)

        if ret:
            img = jpeg.tobytes()
        else:
            pass

        yield (b'--frame\r\n'
               b'Content-Type: image/png;base64,\r\n\r\n' + img + b'\r\n')


if __name__ == '__main__':
    pass
