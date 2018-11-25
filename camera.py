import cv2
import numpy as np
import os


class VideoCamera(object):
    def __init__(self, devices, exp_id):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.exp_id = exp_id
        self.cams = list()
        for dev in devices:
            print "Accessing:", dev
            cam = cv2.VideoCapture(dev)
            cam.set(cv2.CAP_PROP_FPS, 3)
            self.cams.append(cam)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        for cam in self.cams:
            cam.release()

    def get_frame(self, cam):
        success, image = cam.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # ret, jpeg = cv2.imencode('.jpg', image)
        # return jpeg.tobytes()
        return image

    def get_all_frames(self, img_id):
        frames = list()
        for cam_id, cam in enumerate(self.cams):
            frame = self.get_frame(cam)
            self.save_img(frame, cam_id, img_id)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_resized = cv2.resize(frame, (128, 96))
            frames.append(frame_resized)
        frame_montage = np.concatenate(frames, axis=1)
        ret, jpeg = cv2.imencode('.jpg', frame_montage)
        return jpeg.tobytes()

    def save_img(self, img, cam_id, img_id):
        data_loc = os.path.join("data/", self.exp_id, str(cam_id))
        if os.path.isdir(data_loc):
            # print "folder already exists"
            pass
        else:
            print "create folder"
            os.makedirs(data_loc)
        fname = os.path.join(data_loc, str(img_id)+".png")
        # print fname
        return cv2.imwrite(fname, img)
