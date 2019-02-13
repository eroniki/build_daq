# experiment
```python
experiment(self, new_experiment=True, **kwargs)
```

This module contains a class providing the metadata of the experiments.

The experiment class contains all the functions and utilities needed for
containing experiment metadata.

## update_metadata
```python
experiment.update_metadata(self, **kwargs)
```
Update metadata with the given keyword arguments.
## load_experiment
```python
experiment.load_experiment(self, ts)
```
Load metadata from the the json file.
## create_folders
```python
experiment.create_folders(self, ts)
```
Create necessary folders needed for each experiment.
## create_metadata
```python
experiment.create_metadata(self, ts, camera_names, room)
```
Create a metadata with default values.
