# misc
```python
misc(self)
```
Provide miscellaneous tools and functions.
## list_subfolders
```python
misc.list_subfolders(folder)
```
List subfolders of a given folder.
## list_experiments
```python
misc.list_experiments(folders)
```
Given a folder list experiments in it.
## delete_folder
```python
misc.delete_folder(folder)
```
Delete a folder provided in the argument.
## delete_file
```python
misc.delete_file(file)
```
Delete the file provided in the argument.
## experiment_path
```python
misc.experiment_path(exp_id)
```
Contruct the experiment path given the experiment id.
## check_folder_exists
```python
misc.check_folder_exists(folder)
```
Check if folder given in the argument exists or not.
## check_file_exists
```python
misc.check_file_exists(file)
```
Check if file given in the argument exists or not.
## timestamp_to_date
```python
misc.timestamp_to_date(ts)
```
Convert timestamps to time strings represented in EST time zone.
## read_json
```python
misc.read_json(fname)
```
Read json file and returns the data as a dict.
## dump_json
```python
misc.dump_json(fname, data, pretty)
```

Save the data to a json file.

Please note that data type should be json serializable, most primitive
Python data structure conforms this requirement.

## get_md5hash
```python
misc.get_md5hash(foo)
```
Create an MD5 hash of a string.
## parse_rooms
```python
misc.parse_rooms(json_data)
```
Parse the room data from the devices.json file.
## create_folder
```python
misc.create_folder(fname)
```
Create an empty folder.
## find_images
```python
misc.find_images(folder, ext='*.png')
```

Find images in a folder with a given extension.

If the extension of the images are not provided, it is assumed to
be .png

## compress_folder
```python
misc.compress_folder(source, destination)
```
Compress a folder with all subdirectories.
## compress_folder_zip
```python
misc.compress_folder_zip(source, destination)
```
Compress a folder with all subdirectories with Zip64 format.
## run_process
```python
misc.run_process(cmd)
```
Run a process and receives its return value.
