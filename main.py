import numpy as np
import cv2
import json
import sys
import time
import os
from flask import Flask, render_template, Response, request, make_response

from camera import VideoCamera
from pose_detection import pose_detection
from utils import utils

import time
from logging.config import dictConfig

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    app.config["room_id"] = request.args.get('room')
    return render_template('index.html')

@app.route("/check_dataset", methods=["POST", "GET"])
def check_dataset():
    pd = pose_detection()
    exp_id = request.args.get("exp_id")
    statement = str()
    for i in range(7):
        fname = os.path.join("data/", exp_id, str(i)+"/")
        if os.path.exists(fname):
            n = len(pd.find_images(fname))
        else:
            n = 0
        statement += "Camera {i}: {n} images found!<br/>".format(i=i, n=n)
    return statement

@app.route("/pose_detection/<exp_id>/<camera_id>/<img_id>")
def pose(exp_id, camera_id, img_id):
    pd = pose_detection()
    fname = os.path.join("data", exp_id, camera_id, img_id+".png")
    pose = pd.detect_pose(fname)
    if isinstance(pose, str):
        return pose
    else:
        retval, buffer = cv2.imencode('.png', pose)
        print buffer.shape
        response = make_response(buffer.tobytes())
        response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/pose_detection/<exp_id>/<camera_id>")
def pose_all_images(exp_id, camera_id):
    pd = pose_detection()

    fname = os.path.join("data/", exp_id, camera_id +"/")

    if os.path.exists(fname):
        fnames = pd.find_images(fname)
        fnames.sort()
        n = len(fname)
    else:
        n = 0

    for fname in fnames:
        pose = pd.detect_pose(fname)

    return "{n} number of images were processed!".format(n=n)


@app.route("/status/<room_name>", methods=["POST", "GET"])
def status_cears(room_name):
    if room_name.lower() == "cears":
        room_id = 0
    else:
        room_id = 1
    devices = app.config["rooms"][room_id]["devices"]
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


@app.route("/status", methods=["POST", "GET"])
def status_all():
    statements = str()
    for room_id in range(2):
        print room_id
        devices = app.config["rooms"][room_id]["devices"]
        statement_all = "Room Name: {rm}<br />{n} cameras placed here. <br />".format(
            rm=app.config["rooms"][room_id]["name"], n=len(devices))
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


@app.route('/video/<room_name>', methods=['GET', 'POST'])
def video(room_name):
    if room_name.lower() == "cears":
        app.config["room_id"] = 1
    else:
        app.config["room_id"] = 0
    return render_template('video.html')



@app.route('/video_feed')
def video_feed():
    room_id = app.config["room_id"]
    if room_id is None:
        room_id = 0
    else:
        room_id = int(room_id)
    exp_id = str(int(time.time()*1000))
    devices = app.config["rooms"][room_id]["devices"]
    return Response(gen(VideoCamera(devices, exp_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/list_experiments')
def list_experiments():
    u = utils.misc()

    subfolders =  u.list_subfolders("data/*/")
    experiments = u.list_experiments(subfolders)
    statement = ""
    for exp in experiments:
        try:
            date = u.timestamp_to_date(int(exp)/1000 )
            statement += "{exp} - ({date})<br />".format(exp=exp, date=date)
        except:
            print "Skipped"
    return statement

# 
# @app.route('/delete_experiment/<exp_id>')
# def delete_experiment(exp_id):
#     u = utils.misc()
#     folder = u.experiment_path(exp_id)
#     u.delete_folder(folder)
#
#     return "OK"

def gen(camera):
    img_id = 0
    while True:
        frame = camera.get_all_frames(img_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        img_id += 1


def parse_json(fname):
    with open(fname) as file_handler:
        devices = json.load(file_handler)

    dev_path = devices["dev_path"]
    rooms = list()

    for room_id, room in enumerate(devices["rooms"]):
        dev_list = list()
        for dev in room["device_list"]:
            dev_ = os.path.join(dev_path, dev)
            dev_list.append(dev_)
        rooms.append({"name": room["name"],
                      "devices": dev_list
                      })
    return rooms


if __name__ == '__main__':
    # global devices
    arg_len = len(sys.argv)
    if arg_len == 1:
        fname = "devices.json"
    else:
        fname = sys.argv[1]

    rooms = parse_json(fname)
    app.config["rooms"] = rooms
    app.run(host='0.0.0.0', debug=True)
    # main(devices)
