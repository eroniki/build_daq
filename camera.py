import cv2
import numpy as np
import os
import experiment


class VideoCamera(object):
    def __init__(self, devices, room_name):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
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

            self.img_id[dev] = 0

    def __del__(self):
        for cam in self.cams:
            cam.release()

        self.exp.update_metadata(change_image_number=True,
                                 n_images=self.img_id)

    def get_frame(self, cam):
        success, image = cam.read()
        return image

    def get_all_frames(self, img_id):
        if len(self.cams) != 0:
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
        else:
            return "error"

    def save_img(self, img, cam_id, img_id):
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
