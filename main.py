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

import hashlib
import logging
from logging.handlers import RotatingFileHandler
import tailer

from app import flask_app


def main():
    fa = flask_app("asda")
    fa.app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
    # rooms = parse_json("devices.json")
    # users = parse_json("users.json")
    # app.config["rooms"] = rooms
    #
    # handler = RotatingFileHandler('logs/status.log', maxBytes=10000, backupCount=99)
    # formatter = logging.Formatter(
    #     "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    # handler.setLevel(logging.DEBUG)
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)
    #
    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.DEBUG)
    # log.addHandler(handler)
