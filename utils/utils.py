
from glob import glob
import os
from datetime import datetime
from pytz import timezone
import json
import hashlib
import shutil
import subprocess


class misc(object):
    """docstring for utils."""

    def __init__(self):
        super(misc, self).__init__()

    @staticmethod
    def list_subfolders(folder):
        return glob(folder)

    @staticmethod
    def list_experiments(folders):
        experiments = list()

        for f in folders:
            experiments.append(os.path.basename(os.path.normpath(f)))

        experiments.sort()

        return experiments

    @staticmethod
    def delete_folder(folder):
        if misc.check_folder_exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(folder)

    @staticmethod
    def delete_file(file):
        if os.path.exists(file):
            os.remove(file)
            return "Success"
        else:
            return "The file does not exist"

    @staticmethod
    def experiment_path(exp_id):
        return os.path.join("data", exp_id, "")

    @staticmethod
    def check_folder_exists(folder):
        return os.path.isdir(folder)

    @staticmethod
    def check_file_exists(file):
        return os.path.exists(file)

    @staticmethod
    def timestamp_to_date(ts):
        tz = timezone('EST')
        unaware = datetime.fromtimestamp(ts)
        return unaware.replace(tzinfo=tz).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def read_json(fname):
        data = None
        try:
            with open(fname) as file_handler:
                data = json.load(file_handler)
        except Exception as e:
            return None
        return data

    @staticmethod
    def dump_json(fname, data, pretty):
        with open(fname, 'w') as outfile:
            if pretty:
                json.dump(data, outfile, indent=4, sort_keys=True)
            else:
                json.dump(data, outfile)

    @staticmethod
    def get_md5hash(foo):
        return hashlib.md5(foo).hexdigest().upper()

    @staticmethod
    def parse_rooms(json_data):
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
        os.makedirs(fname)

    @staticmethod
    def find_images(folder, ext=".png"):
        return glob.glob(folder + ext)

    @staticmethod
    def compress_folder(source, destination):
        try:
            base = os.path.basename(destination)
            name = base.split('.')[0]
            format = base.split('.')[1]
            archive_from = os.path.dirname(source)
            archive_to = os.path.basename(source.strip(os.sep))
            shutil.make_archive(name, format, archive_from, archive_to)
            shutil.move('%s.%s' % (name, format), destination)
            return True
        except Exception as e:
            return False

    @staticmethod
    def run_process(cmd):
        result = subprocess.Popen(cmd)
        return result.poll()


if __name__ == '__main__':
    pass
