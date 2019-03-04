# Calibration Process for the Cameras 
This document provides a brief explanation regarding the calibration process adopted in the project.
The necessity of the calibration process arises from the ill-defined nature of projective geometry forming the basis of the computer vision algorithms employed.
Hence, the calibration process referred in this document, is solely for the cameras employed in the project.

The further (strongly suggested) reading material can be found in [Wikipedia](https://en.wikipedia.org/wiki/Camera_resectioning), [OpenCV](https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html), [Dissecting the Camera Matrix, Part 1: Extrinsic/Intrinsic Decomposition](https://ksimek.github.io/2012/08/14/decompose/), and [another OpenCV tutorial](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html).

It should be noted that in this document the reader is assumed to be somewhat familiar with the data acquisition system and the camera placement.
# Table of Contents
- [Calibration Process for the Cameras](#calibration-process-for-the-cameras)
- [Table of Contents](#table-of-contents)
- [Method](#method)
  - [Tools](#tools)
- [Intrinsics Calibration with `Camera Calibrator`](#intrinsics-calibration-with-camera-calibrator)
- [Extrinsics Calibration with `Stereo Camera Calibrator`](#extrinsics-calibration-with-stereo-camera-calibrator)
- [Appendix](#appendix)
  - [Camera Names and Indices](#camera-names-and-indices)
    - [CEARS](#cears)
    - [Computer Lab](#computer-lab)

# Method
As can be seen the referred material, there are two types of calibration matrices need to be obtained in order to achieve stereo-triangulation: intrinsics and extrincins calibration (or parameters, or matrices).
Both are obtained with a similar fashion, i.e. using a chessboard with known dimensions.
For a fixed camera, a number of photos containing chessboard in them under different poses, the parameters of interests are obtained within an optimization framework.

The intrinsic parameters define how the optical characteristics of the camera unit function such as optical length of the lens, distortion coefficients etc.
Therefore, this information should/can be obtained for each camera individualy.

On the other hand, the extrinsic parameters define the location and attitude (will be referred as pose for brevity) of the camera in the global coordinate system.
This information is not so useful for monocular setups; therefore, it is customary to obtain extrinsics parameters for pairs of cameras.

**Note:** It should be noted that for the extrinsics parameters obtained from the contemprary tools are such that the first camera of the pair is assumed to be the global coordinate system while the extrinsic parameters represent the pose of the second camera with respect to the first.

## Tools
In order to obtain the calibration matrices, we use [`Matlab`](#) and its prepackaged applications.
Matlab provides two different applications for camera calibration purposes:  `Camera Calibrator` and `Stereo Camera Calibrator`.
Both of them were employed in different stages of the calibration process and will be introduced in the following sections.

# Intrinsics Calibration with `Camera Calibrator`
The intrinsics parameters of the cameras employed in the study are obtained with `Matlab` package called [`Camera Calibrator`](https://www.mathworks.com/help/vision/ref/cameracalibrator-app.html). 
This application can be run as typing the command below:
```matlab
cameraCalibrator
```
or starting from the Apps tab on top.

The workflow of the intrinsic calibration is summarized as below:
1. Initialization
   - Provide the path of the folder containing the chessboard photos. 
   - Provide the dimensions of the chessboard
2. After providing the necessary information to the application, it runs a chessboard detection algorithm on the whole set of photos.
3. After chessboard detection, the photos in which the chessboard is not detected are rejected.
4. Setting the calibration process.
   - Choose this
   - Choose that
   - Choose this
5. Calibrate!
6. Delete the photos with high reprojection error, until the mean of reprojection error goes down .75 pixels. (0.75 pixels is a the golden standard, this is a *de-facto* standard widely accepted in the Computer Vision society.)
7. Recalibrate!
8. Save the results to a mat file, note the parameters into the `devices.json` file.

Please note that in Step 6, the convention that `Matlab` uses is different that the developped software.
`Matlab` stores the intrinsic matrix as the transpose of the general convention.
Therefore, before typing the matrix into the `devices.json` file, make sure that the matrix is transposed.

In the repeated calibration sessions I had in my office, the below are the intrinsics parameters are valid for the cameras used in the study:

Intrinsics Matrix `K`:
```matlab
[374.672, 0, 0; 0, 501.706, 0; 302.039, 247.027, 1];
```
Distortion Coefficients (radial and tangential) `d`:
```matlab
[0.00170557, 0.00113633, 0.0927195, -0.20188, 0.0785958]
```


# Extrinsics Calibration with `Stereo Camera Calibrator`
The extrinsics parameters are obtained with [`Stereo Camera Calibrator`](https://www.mathworks.com/help/vision/ref/stereocameracalibrator-app.html) application provided by `Matlab`.
This application can be run as typing the command below:
```matlab
stereoCameraCalibrator
```
or starting from the Apps tab on top.

The workflow of the extrinsics calibration is similar to that of intrinsics:
1. Initialization
   - Provide the path of the folder containing the chessboard photos. 
   - Provide the dimensions of the chessboard
2. After providing the necessary information to the application, it runs a chessboard detection algorithm on the whole set of photos.
3. After chessboard detection, the photos in which the chessboard is not detected are rejected.
4. Setting the calibration process.
   - Choose this
   - Choose that
   - Choose this
5. Calibrate!
6. Delete the photos with high reprojection error, until the mean of reprojection error goes down .75 pixels. (0.75 pixels is a the golden standard, this is a *de-facto* standard widely accepted in the Computer Vision society.)
7. Recalibrate!
8. Save the results to a mat file, note the parameters into the `devices.json` file.

---
# Appendix
## Camera Names and Indices
### CEARS
| ID  | Name                                                   |
| --- | ------------------------------------------------------ |
| 0   | `usb-046d_Logitech_Webcam_C930e_3B43517E-video-index0` |
| 1   | `usb-046d_Logitech_Webcam_C930e_3B42507E-video-index0` |
| 2   | `usb-046d_Logitech_Webcam_C930e_64FE757E-video-index0` |
| 3   | `usb-046d_Logitech_Webcam_C930e_7EBB957E-video-index0` |
| 4   | `usb-046d_Logitech_Webcam_C930e_845F417E-video-index0` |
| 5   | `usb-046d_Logitech_Webcam_C930e_8C8B557E-video-index0` |
| 6   | `usb-046d_Logitech_Webcam_C930e_BBFF617E-video-index0` |
| 7   | `usb-046d_Logitech_Webcam_C930e_D047957E-video-index0` |
### Computer Lab
| ID  | Name                                                   |
| --- | ------------------------------------------------------ |
| 0   | `usb-046d_Logitech_Webcam_C930e_8843357E-video-index0` |
| 1   | `usb-046d_Logitech_Webcam_C930e_23C6957E-video-index0` |
| 2   | `usb-046d_Logitech_Webcam_C930e_4191517E-video-index0` |
| 3   | `usb-046d_Logitech_Webcam_C930e_814F417E-video-index0` |
| 4   | `usb-046d_Logitech_Webcam_C930e_BF3E417E-video-index0` |
| 5   | `usb-046d_Logitech_Webcam_C930e_BD2F957E-video-index0` |
| 6   | `usb-046d_Logitech_Webcam_C930e_D3FFA67E-video-index0` |
| 7   | `usb-046d_Logitech_Webcam_C930e_5FD23C5E-video-index0` |

---
