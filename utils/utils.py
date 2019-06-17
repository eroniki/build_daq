"""
This module contains a class which is used for miscellaneous purposes.

The misc class contains all the functions and utilities needed for the other
packages and classes, such as providing low-level OS interactions, creating
timestamps etc.
"""
import glob
import os
from datetime import datetime
from pytz import timezone
import json
import hashlib
import shutil
import subprocess
import zipfile
from collections import OrderedDict


class misc(object):
    """Provide miscellaneous tools and functions."""

    def __init__(self):
        super(misc, self).__init__()

    @staticmethod
    def list_subfolders(folder):
        """List subfolders of a given folder."""
        return glob.glob(folder)

    @staticmethod
    def list_experiments(folders):
        """Given a folder list experiments in it."""
        experiments = list()

        for f in folders:
            experiments.append(os.path.basename(os.path.normpath(f)))

        experiments.sort()

        return experiments

    @staticmethod
    def delete_folder(folder):
        """Delete a folder provided in the argument."""
        if misc.check_folder_exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(folder)

    @staticmethod
    def delete_file(file):
        """Delete the file provided in the argument."""
        if os.path.exists(file):
            os.remove(file)
            return "Success"
        else:
            return "The file does not exist"

    @staticmethod
    def experiment_path(exp_id):
        """Contruct the experiment path given the experiment id."""
        return os.path.join("data", exp_id, "")

    @staticmethod
    def check_folder_exists(folder):
        """Check if folder given in the argument exists or not."""
        return os.path.isdir(folder)

    @staticmethod
    def check_file_exists(file):
        """Check if file given in the argument exists or not."""
        return os.path.exists(file)

    @staticmethod
    def timestamp_to_date(ts):
        """Convert timestamps to time strings represented in EST time zone."""
        tz = timezone('EST')
        unaware = datetime.fromtimestamp(ts)
        return unaware.replace(tzinfo=tz).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def read_json(fname):
        """Read json file and returns the data as a dict."""
        data = None
        try:
            with open(fname) as file_handler:
                data = json.load(file_handler, object_pairs_hook=OrderedDict)
        except Exception as e:
            return None
        return data

    @staticmethod
    def dump_json(fname, data, pretty):
        """
        Save the data to a json file.

        Please note that data type should be json serializable, most primitive
        Python data structure conforms this requirement.
        """
        with open(fname, 'w') as outfile:
            if pretty:
                json.dump(data, outfile, indent=4, sort_keys=True)
            else:
                json.dump(data, outfile)

    @staticmethod
    def get_md5hash(foo):
        """Create an MD5 hash of a string."""
        return hashlib.md5(foo).hexdigest().upper()

    @staticmethod
    def parse_rooms(json_data):
        """Parse the room data from the devices.json file."""
        dev_path = json_data["dev_path"]
        rooms = list()

        for room_id, room in enumerate(json_data["rooms"]):
            dev_list = list()
            for dev in room["device_list"]:
                dev_ = os.path.join(dev_path, dev)
                dev_list.append(dev_)
            rooms.append({"name": room["name"],
                          "devices": dev_list
                          })
        return rooms

    @staticmethod
    def create_folder(fname):
        """Create an empty folder."""
        os.makedirs(fname)

    @staticmethod
    def find_images(folder, ext="*.png"):
        """
        Find images in a folder with a given extension.

        If the extension of the images are not provided, it is assumed to
        be .png
        """
        return glob.glob(folder + ext)

    @staticmethod
    def compress_folder(source, destination):
        """Compress a folder with all subdirectories."""
        try:
            base = os.path.basename(destination)
            name = base.split('.')[0]
            format = base.split('.')[1]
            archive_from = os.path.dirname(source)
            archive_to = os.path.basename(source.strip(os.sep))
            shutil.make_archive(name, format, archive_from, archive_to)
            print '%s.%s' % (name, format), destination
            shutil.move('%s.%s' % (name, format), destination)
            return True
        except Exception as e:
            print e
            return False

    @staticmethod
    def compress_folder_zip(source, destination):
        """Compress a folder with all subdirectories with Zip64 format."""
        print source, destination
        zf = zipfile.ZipFile(destination, "w", allowZip64=True)
        for dirname, subdirs, files in os.walk(source):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()

        return True

    @staticmethod
    def run_process(cmd):
        """Run a process and receives its return value."""
        result = subprocess.Popen(cmd)
        return result.poll()


if __name__ == '__main__':
    pass
