# BUILD_DAQ: A data acquisition system for multi-room, multi camera setup
Maintainer: [Murat Ambarkutuk](http://murat.ambarkutuk.com)

Email: murata@vt.edu

VAST Lab, Mechanical Engineering Department,

Virginia Tech, Blacksburg, VA

# Summary:
This repository contains the necessary tools and packages needed for Steelcase funded project called BUILD. 
This project involves with human pose detection in 3D with multiple cameras placed in different room located in Cheatham Hall, Virginia Tech. 
In this repository, one can find a various python modules and classes to create a RESTful API to interact with the Image Acquisition system as well as processing the collected images.

# Installation
## Dependencies:
OpenPose is needed to extract poses from the collected images. Please make sure OpenPose is installed correctly (with Python bindings). 
You can follow [this link](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md) to obtain a comprehensive guide to install Openpose.
## Obtaining the Repository
1. Open a new terminal window with _CTRL+ALT+T_
1. Run the commands sequentially:
Clone the repository:
```
git clone https://github.com/eroniki/build_daq.git
```
Enter to the repository folder:
```
cd build_daq
```
Install the dependencies:
```
sudo -H pip install -r requirements.txt
```
Reboot the system:
```
sudo reboot now
```
# Usage:
Upon completion of the installation, the system can be started directly with 
```
python main.py
```
This script creates the REST API and starts serving a WEB-interface with which the system can be manipulated.

One can find the served with interface (locally):
```
http://0.0.0.0:5000
```

or if you'd like to access the system remotely, you can use a link similar to the one in below where _THE_IP_ADRESS_OF_THE_LOCAL_MACHINE_ is the global IP address of the computer serving the system.

```
http://THE_IP_ADRESS_OF_THE_LOCAL_MACHINE:5000
```


# Documentation
## Main Code
The main controller of the code lay in __main.py__ file. This python script creates and initializes all the classes needed in the project.

## Flask App
The basic User Interface is created by using Flask, a web development tool for Python. 

All the necessary tools and classes were implemeted in this class, which reside in __app.py__ module.
The documentation of the computer_vision class is automatically generated from the docstrings of the classes and the functions in it.
The documentation is located [here](docs/app.md).
## Utility Class
The documentation of the utility class is automatically generated from the docstrings of the classes and the functions in it.
The documentation is located [here](docs/utils.md).
## Experiment Class
The documentation of the experiment class is automatically generated from the docstrings of the classes and the functions in it.
The documentation is located [here](docs/experiment.md).
## Computer Vision Class
The documentation of the computer_vision class is automatically generated from the docstrings of the classes and the functions in it.
The documentation is located [here](docs/computer_vision.md).
## Pose Detection Class

## Camera Class
The documentation of the camera module and its contents are automatically generated from the docstrings of the classes and the functions in it.
The documentation is located [here](docs/camera.md).

## Calibration Process
This calibration process is provided [here](docs/calibration_process.md)
# Contribution
If you would like to contribute to this project, please make sure you read and understand the contribution workflow.
