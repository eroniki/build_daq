import glob
import os
import cv2
import numpy as np

class pose_detection(object):
    """docstring for pose_detection."""
    def __init__(self):
        super(pose_detection, self).__init__()

    def find_images(self, folder):
        return glob.glob(folder + "*.png")
