"""
This module contains a class which is used for video capturing purposes.

The VideoCamera class contains all the functions and utilities needed in the
actual image acquisition process.
"""
import cv2
import numpy as np
import os
from . import experiment
import time
from threading import Thread


class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream", width=320, height=180):
        self.fps = 3.0
        self.width = width
        self.height = height
        self.frame = np.zeros([width, height, 3], dtype=np.uint8)
        self.stream = cv2.VideoCapture(src)
        time.sleep(self.fps)

        if self.stream.isOpened():
            self.stream.set(cv2.CAP_PROP_FPS, 3)
            self.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            self.stream.set(cv2.CAP_PROP_BUFFERSIZE, self.fps)
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.last = time.time()*1000.0
        # initialize the thread name
        self.name = name
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            self.last = time.time()*1000.0
            time.sleep(self.fps)

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def __del__(self):
        self.stream.release()


class VideoCamera:
    """
    VideoCamera class contains image acquisition system.

    VideoCamera class contains all the functions and utilities needed in the
    actual image acquisition process.
    """

    def __init__(self, devices, room_name):
        self.cams = list()
        self.exp = experiment(new_experiment=True,
                              camera_names=devices,
                              room=room_name)
        self.exp_id = str(self.exp.ts)
        self.device_ids = list()
        self.img_id = dict()
        self.devices = devices

        for dev in devices:
            print("Accessing:", dev)
            self.device_ids.append(os.path.basename(dev))
            cam = WebcamVideoStream(dev, name=dev, width=640, height=360)
            cam.start()
            self.cams.append(cam)

    def __del__(self):
        """Delete object to release the cameras.

        By having this property of the class, the cameras are turned off after
        the webpage is closed.
        """
        for cam in self.cams:
            del cam

        self.exp.update_metadata(change_image_number=True,
                                 n_images=self.img_id)

    def get_all_frames(self, img_id):
        """
        Collect images from all the cameras.

        This function's role is 3-folds:
        1. Checks if we have at least 1 camera attached to the system.
        Otherwise, the system reports the problem.
        2. Captures frames from all the cameras and saves it.
        3. Creates a montage from the images and returns it to the REST server.
        """
        if len(self.cams) == 0:
            img = cv2.imread("static/task.jpg")
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()

        frames = list()
        frames_resized_list = list()

        for cam_id, cam in enumerate(self.cams):
            if time.time()*1000.0 - cam.last > 10000:
                frame = cam.read()
            else:
                cam.stop()
                frame = np.zeros_like(cam.frame)
            frames.append(frame)

        for frame in frames:
            try:
                frame_resized = cv2.resize(frame, (320, 180))
                # self.save_img(frame, self.device_ids[cam_id], img_id)
            except:
                frame_resized = np.zeros((180, 320, 3), dtype=np.uint8)

            frames_resized_list.append(frame_resized)

        frame_montage = np.concatenate(frames_resized_list, axis=1)
        ret, jpeg = cv2.imencode('.jpg', frame_montage)
        return jpeg.tobytes()

    def save_img(self, img, cam_id, img_id):
        """
        Save an image to a file.

        1. Checks if the folder exists. If it doesn't exists, creates it.
        1. Constructs the image file name from _cam_id_ _img_id_
        1. Saves the image to the file.
        1. Updates the metadata of the experiment for REST API.
        """
        data_loc = os.path.join("data/", self.exp_id, "raw", str(cam_id))
        if os.path.isdir(data_loc):
            pass
        else:
            # print "create folder"
            os.makedirs(data_loc)
        fname = os.path.join(data_loc, str(img_id) + "_" +
                             str(int(time.time()*1000.0)) + ".png")
        # retval = cv2.imwrite(fname, img)
        # print "{fname} is saved!".format(fname=fname)

        cc = os.path.join("/dev/v4l/by-id", cam_id)
        self.img_id[cc] = img_id
        self.exp.update_metadata(change_image_number=True,
                                 n_images=self.img_id)
        return retval
