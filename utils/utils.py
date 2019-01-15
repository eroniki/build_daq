
from glob import glob
import os
from datetime import datetime
from pytz import timezone

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

if __name__ == '__main__':
    pass
