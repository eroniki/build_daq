import glob
import os
import cv2
import numpy as np
from openpose import OpenPose
import json


class pose_detection(object):
    """docstring for pose_detection."""

    def __init__(self):
        super(pose_detection, self).__init__()
        params = dict()
        params["logging_level"] = 3
        params["output_resolution"] = "-1x-1"
        params["net_resolution"] = "-1x1072"
        params["model_pose"] = "BODY_25"
        params["alpha_pose"] = 0.6
        params["scale_gap"] = 0.3
        params["scale_number"] = 1
        params["render_threshold"] = 0.05
        params["num_gpu_start"] = 0
        params["disable_blending"] = False
        params["default_model_folder"] = "/home/immersivemidiaopenposeclone/openpose/models/"
        self.openpose = OpenPose(params)

    @staticmethod
    def find_images(folder):
        return glob.glob(folder + "*.png")

    def detect_pose(self, fname):
        img = cv2.imread(fname)
        if img is None:
            return "image not found"
        else:
            joints, output_image = self.openpose.forward(img, display=True)
            # print joints.shape, output_image.shape
            print fname
            with open(fname+".json", 'w') as outfile:
                json.dump(joints.tolist(), outfile)
            dirname = os.path.dirname(fname)
            cv2.imwrite(fname+".jpg", output_image)
            return output_image
