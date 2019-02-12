# BUILD_DAQ: A data acquisition system for multi-room, multi camera setup
Maintainer: [Murat Ambarkutuk](http://murat.ambarkutuk.com)

## Installation
### Dependencies:
OpenPose is needed to extract poses from the collected images. Please make sure OpenPose is installed correctly (with Python bindings).
### Obtaining the Repository
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
## Documentation
### Main Code
The main controller of the code lay in __main.py__ file. This python script creates and initializes all the classes needed in the project.

### Flask App
The basic User Interface is created by using Flask, a web development tool for Python. 

All the necessary tools and classes were implemeted in this class, which reside in __app.py__ module.

### Utility Class

### Experiment Class

### Computer Vision Class

### Pose Detection Class

### Camera Class

## Contribution
If you would like to contribute to this project, please make sure you read and understand the contribution workflow.
