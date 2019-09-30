"""
This module contains a class for primitive computer vision operations.

The computer_vision class contains all the functions and utilities needed for
the provide primitive computer vision operations.
"""
import cv2
import numpy as np


class computer_vision(object):
    """
    This module contains a class for primitive computer vision operations.

    The computer_vision class contains all the functions and utilities needed
    for the provide primitive computer vision operations.
    """

    def __init__(self):
        super(computer_vision, self).__init__()

    @staticmethod
    def triangulate(P1, P2, points1, point2):
        """Triangulate corresponding points with given projection matrices."""
        return cv2.triangulatePoints(P1, P2, points1, points2)

    @staticmethod
    def extract_features(img, thr=0.005):
        """Extract features from an image, return keypoints and descriptors."""
        if img.ndims == 3:
            img = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

        detector = cv2.AKAZE_create()
        (kpts, descs) = detector.detectAndCompute(img, None)
        return kpts, descs

    @staticmethod
    def match_features(desc1, desc2):
        """Match extracted descriptors, return good matching ones."""
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
        """Extract a thumbnail from an image, containing only one person."""
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
        """Undistort points to eliminate the lens distortion."""
        return cv2.undistortPoints(points, K, dist)

    @staticmethod
    def _calculate_camera_pose(frame, K, d, corners, pattern_shape=(6, 4), grid_size=30):  # noqa: E501
        """Calculate camera pose with a frame containing checkerboard in it."""
        img = frame.copy()
        axis = np.float32([[grid_size, 0, 0], [0, grid_size, 0],
                           [0, 0, -grid_size]]).reshape(-1, 3)*2

        objp = np.zeros((np.prod(pattern_shape), 3), np.float32)
        objp[:, :2] = np.mgrid[0:pattern_shape[0],
                               0:pattern_shape[1]].T.reshape(-1, 2) * grid_size

        _, rvecs, tvecs = cv2.solvePnP(objp, corners, K, d)
        R, _ = cv2.Rodrigues(rvecs)
        # project 3D points onto image plane
        imgpts, _ = cv2.projectPoints(axis,
                                      rvecs, tvecs,
                                      K, d)

        canvas = computer_vision.draw_axis(img, corners, imgpts)
        return R, tvecs, canvas

    @staticmethod
    def calculate_camera_pose(frame,  K, d, pattern_shape=(6, 4), grid_size=30):  # noqa: E501
        """Calculate camera pose with a frame containing checkerboard in it."""
        corners, canvas = computer_vision.detect_chessboard(frame, pattern_shape)  # noqa: E501

        if corners is None:
            canvas = frame
            text = "No checkerboard"
            return text, corners, canvas, None, None
        else:
            canvas = cv2.undistort(canvas, K, d)
            R, t, canvas = computer_vision._calculate_camera_pose(frame,
                                                                  K, d,
                                                                  corners,
                                                                  pattern_shape,  # noqa: E501
                                                                  grid_size)
            text = " ".join(np.round(t, 2).ravel().astype(str))
        return text, corners, canvas, R, t

    @staticmethod
    def detect_chessboard(frame, pattern_shape=(7, 6)):
        """Detect chessboard with a given shape in the frame."""
        corners = None
        canvas = None
        img = frame.copy()
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, pattern_shape)
        if ret:
            corners = cv2.cornerSubPix(gray, corners,
                                       (11, 11), (-1, -1), criteria)
            canvas = cv2.drawChessboardCorners(img, pattern_shape,
                                               corners, ret)

        return corners, canvas

    @staticmethod
    def draw_axis(img, corners, imgpts):
        """Draw 3D axis on a given image."""
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
        return img
