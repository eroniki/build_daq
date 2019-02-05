import cv2
import numpy as np


class computer_vision(object):
    """docstring for computer_vision."""

    def __init__(self):
        super(computer_vision, self).__init__()

    @staticmethod
    def triangulate(P1, P2, points1, point2):
        return cv2.triangulatePoints(P1, P2, points1, points2)

    @staticmethod
    def extract_features(img, thr=0.005):
        if img.ndims == 3:
            img = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

        detector = cv2.AKAZE_create()
        (kpts, descs) = detector.detectAndCompute(img, None)
        return kpts, descs

    @staticmethod
    def match_meaturs(desc1, desc2):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(desc1, desc2, k=2)    # typo fixed

        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.9*n.distance:
                good.append([m])

        return good

    @staticmethod
    def extract_thumbnail(img, joints):
        x_min, y_min = np.min(joints, axis=0)
        x_max, y_max = np.max(joints, axis=0)
        [h, w, _] = img.shape

        if x_min > 20:
            x_min -= 20
        if y_min > 20:
            y_min -= 20

        if x_max+20 < w:
            x_max += 20
        if y_max+20 < h:
            y_max += 20

        return img[y_min:y_max, x_min:x_max, :]

    @staticmethod
    def undistort_points(points, K, dist):
        return cv2.undistortPoints(points, K, dist)
