# VideoCamera
```python
VideoCamera(self, devices, room_name)
```

## get_frame
```python
VideoCamera.get_frame(self, cam)
```
Given a cam object, read one image and return it.
## get_all_frames
```python
VideoCamera.get_all_frames(self, img_id)
```

Collect images from all the cameras.

This function's role is 3-folds:
1. Checks if we have at least 1 camera attached to the system.
Otherwise, the system reports the problem.
2. Captures frames from all the cameras and saves it.
3. Creates a montage from the images and returns it to the REST server.

## save_img
```python
VideoCamera.save_img(self, img, cam_id, img_id)
```

Save an image to a file.

1. Checks if the folder exists. If it doesn't exists, creates it.
1. Constructs the image file name from _cam_id_ _img_id_
1. Saves the image to the file.
1. Updates the metadata of the experiment for REST API.

