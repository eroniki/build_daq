# flask_app
```python
flask_app(self, key)
```

This module contains a class to create the REST API.

The flask_app class contains all the functions and utilities needed to provide
the REST API.

## load_users
```python
flask_app.load_users(self)
```
Load users for authorization purposes from the json file.
## load_rooms
```python
flask_app.load_rooms(self)
```
Load rooms for authorization purposes from the json file.
## create_endpoints
```python
flask_app.create_endpoints(self)
```
Create API endpoints.
## index
```python
flask_app.index(self)
```
Render the homepage.
## gen
```python
flask_app.gen(self, camera)
```
Camera generator for the actual tests.
## gen_testcamera
```python
flask_app.gen_testcamera(self, camera)
```
Camera generator for the test_camera endpoint.
## compress_experiment
```python
flask_app.compress_experiment(*args, **kwargs)
```
Compress the whole data corresponding to an experiment.
## video
```python
flask_app.video(*args, **kwargs)
```
Render the video page.
## test_camera
```python
flask_app.test_camera(*args, **kwargs)
```
Test the camera and return the image.
## check_experiment
```python
flask_app.check_experiment(*args, **kwargs)
```
Provide details of an experiment.
## video_feed
```python
flask_app.video_feed(*args, **kwargs)
```
Run the cameras in a room.
## list_experiments
```python
flask_app.list_experiments(*args, **kwargs)
```
List all the experiments.
## clone_experiment
```python
flask_app.clone_experiment(*args, **kwargs)
```
Clone experiment to the cloud.
## delete_archive
```python
flask_app.delete_archive(*args, **kwargs)
```
Delete the zip file.
## status_room
```python
flask_app.status_room(*args, **kwargs)
```
Check the status of a room.
## delete_experiment
```python
flask_app.delete_experiment(*args, **kwargs)
```
Delete an experiment with the given id.
## label_experiment
```python
flask_app.label_experiment(*args, **kwargs)
```
Create/Update the label of an experiment.
## status_all_rooms
```python
flask_app.status_all_rooms(*args, **kwargs)
```
Check the status of all rooms.
## protected
```python
flask_app.protected(*args, **kwargs)
```
Show logged username.
## login
```python
flask_app.login(self)
```
Login to the system.
## logout
```python
flask_app.logout(self)
```
Logout from the system.
## user_loader
```python
flask_app.user_loader(self, email)
```
Check if the user in the user.json file.
## request_loader
```python
flask_app.request_loader(self, request)
```
Handle each request.
## unauthorized_handler
```python
flask_app.unauthorized_handler(self)
```
If the user is unauthorized, direct him/her to the login page.
## pose_img
```python
flask_app.pose_img(self, exp_id, camera_id, img_id)
```
Employ pose detection on a single image.
## pose_cam
```python
flask_app.pose_cam(self, exp_id, camera_id)
```

Employ pose_detection on the all images with a given experiment and
the camera id.

## pose_exp
```python
flask_app.pose_exp(self, exp_id)
```

Given an experiment id to employ pose_detection on the whole images
collected from all the cameras.

## match_people
```python
flask_app.match_people(self, exp_id)
```
Match people based on feature matching algorithm.
## make_thumbnails
```python
flask_app.make_thumbnails(self, exp_id)
```
Create a thumbnail from an image, which contains only one person.
## triangulate
```python
flask_app.triangulate(self, exp_id)
```
Triangulate people's locations.
## log
```python
flask_app.log(self)
```
Return the system logs. 10 lines.
## log_n
```python
flask_app.log_n(self, n)
```
Return n number of lines from the system logs.
