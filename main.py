import numpy as np
import cv2
import json
import sys
import time
import os
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    app.config["room_id"] = request.args.get('room')
    return render_template('index.html')


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


def gen(camera):
    img_id = 0
    while True:
        frame = camera.get_all_frames(img_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        img_id += 1
# def main(devices):
#     cams = list()
#     for dev in devices:
#         print "Accessing:", dev
#         cam = cv2.VideoCapture(dev)
#         cam.set(cv2.CAP_PROP_FPS, 3)
#         cams.append(cam)
#         # cv2.namedWindow(dev, cv2.WINDOW_NORMAL)
#
#     cv2.namedWindow("imgs")
#
#
#     while(True):
#         frames = list()
#         for cam_id, cam in enumerate(cams):
#             frame = get_frame(cam)
#             # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             frame = cv2.resize(frame, (128, 96))
#             frames.append(frame)
#         frame_montage = np.concatenate(frames, axis=1)
#
#         cv2.imshow("imgs", frame_montage)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     stop_cameras(cams)
#
#     cv2.destroyAllWindows()


# def get_frame(cam):
#     ret, frame = cam.read()
#     # print ret
#     if ret is False:
#         frame = np.zeros((128, 96, 3), dtype=np.uint8)
#     return frame
#
#
# def stop_cameras(cameras):
#     for cam in cameras:
#         stop_camera(cam)
#
#
# def stop_camera(cam):
#     cam.release()


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
