# computer_vision
```python
computer_vision(self)
```

This module contains a class for primitive computer vision operations.

The computer_vision class contains all the functions and utilities needed
for the provide primitive computer vision operations.

## triangulate
```python
computer_vision.triangulate(P1, P2, points1, point2)
```
Triangulate corresponding points with given projection matrices.
## extract_features
```python
computer_vision.extract_features(img, thr=0.005)
```
Extract features from an image, return keypoints and descriptors.
## match_meaturs
```python
computer_vision.match_meaturs(desc1, desc2)
```
Match extracted descriptors, return good matching ones.
## extract_thumbnail
```python
computer_vision.extract_thumbnail(img, joints)
```
Extract a thumbnail from an image, containing only one person.
## undistort_points
```python
computer_vision.undistort_points(points, K, dist)
```
Undistort points to eliminate the lens distortion.
