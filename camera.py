"""
This module contains a class which is used for video capturing purposes.

The VideoCamera class contains all the functions and utilities needed in the
actual image acquisition process.
"""
import cv2
import numpy as np
import os
import experiment


class VideoCamera(object):
    def __init__(self, devices, room_name):
        """Init"""
        self.cams = list()
        self.exp = experiment.experiment(new_experiment=True,
                                         camera_names=devices,
                                         room=room_name)
        self.exp_id = str(self.exp.ts)
        self.device_ids = list()
        self.img_id = dict()
        self.devices = devices

        for dev in devices:
            print "Accessing:", dev
            self.device_ids.append(os.path.basename(dev))
            cam = cv2.VideoCapture(dev)
            if cam.isOpened():
                cam.set(cv2.CAP_PROP_FPS, 3)
                cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                self.cams.append(cam)
                print dev, "is opened"
            else:
                print "error in", dev
            self.img_id[dev] = 0

    def __del__(self):
        """Delete object to release the cameras.

        By having this property of the class, the cameras are turned off after
        the webpage is closed.
        """
        for cam in self.cams:
            cam.release()

        self.exp.update_metadata(change_image_number=True,
                                 n_images=self.img_id)

    def get_frame(self, cam):
        """Given a cam object, read one image and return it."""
        success, image = cam.read()
        return image

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
        for cam_id, cam in enumerate(self.cams):
            frame = self.get_frame(cam)
            self.save_img(frame, self.device_ids[cam_id], img_id)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            try:
                frame_resized = cv2.resize(frame, (128, 96))
            except:
                frame_resized = np.zeros((128, 96, 3))
            frames.append(frame_resized)
        frame_montage = np.concatenate(frames, axis=1)
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
            # print "folder already exists"
            pass
        else:
            print "create folder"
            os.makedirs(data_loc)
        fname = os.path.join(data_loc, str(img_id) + ".png")
        retval = cv2.imwrite(fname, img)
        print "{fname} is saved!".format(fname=fname)

        cc = os.path.join("/dev/v4l/by-id", cam_id)
        self.img_id[cc] = img_id
        self.exp.update_metadata(change_image_number=True,
                                 n_images=self.img_id)
        return retval
