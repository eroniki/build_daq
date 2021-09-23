"""
This module contains a class to create the REST API.

The flask_app class contains all the functions and utilities needed to provide
the REST API.
"""
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

from utils.utils import misc


class flask_app(object):
    """This module contains a class to create the REST API.

    The flask_app class contains all the functions and utilities needed."""

    def __init__(self, context, key=None):
        super(flask_app, self).__init__()
        if not misc.check_folder_exists("logs"):
            misc.create_folder("logs")


        self.users = self.load_users()
        self.rooms = self.load_rooms()
        self.app = Flask(__name__)
        self.app.secret_key = key

        self.app.add_url_rule("/", view_func=self.index)


    def load_rooms(self):
        """Load rooms for authorization purposes from the json file."""
        devices_data = misc.read_json("devices.json")
        rooms = misc.parse_rooms(devices_data)
        return rooms

if __name__ == '__main__':
    pass
