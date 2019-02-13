"""
This module contains a class which contains the metadata of the experiments.

The experiment class contains all the functions and utilities needed for
containing experiment metadata.
"""
import os
import json
import time
from utils import utils


class experiment(object):
    """
    This module contains a class providing the metadata of the experiments.

    The experiment class contains all the functions and utilities needed for
    containing experiment metadata.
    """

    def __init__(self, new_experiment=True, **kwargs):
        """
        Initialize a metadata from the saved metadata or create a new one.

        This function creates a new metadata file if the _new_experiment_ is
        set to true with default values.
        If _new_experiment_ is set to false, the metadata for the experiment is
        read from the file.
        """
        super(experiment, self).__init__()
        self.um = utils.misc()
        self.subfolders = ["raw",
                           "output/pose/img",
                           "output/pose/pose",
                           "output/thumbnails",
                           "output/features",
                           "output/triangulation",
                           "output/state_estimation",
                           "output/events"]

        if new_experiment:
            self.ts = int(time.time()*1000)
            json_loc = os.path.join("data/", str(self.ts), "experiment.json")
            camera_names = kwargs["camera_names"]
            room = kwargs["room"]
            self.create_folders(ts=self.ts)
            print "Folders created!"
            self.metadata = self.create_metadata(ts=self.ts,
                                                 camera_names=camera_names,
                                                 room=room)
            print "Metadata created!"
            metadata_json = json.dumps(self.metadata)
            print json_loc
            print self.metadata
            print type(self.metadata)
            print metadata_json
            self.um.dump_json(fname=json_loc, data=self.metadata, pretty=True)

        else:
            self.ts = kwargs["ts"]
            self.metadata = self.load_experiment(self.ts)
            print self.metadata

    def update_metadata(self, **kwargs):
        """Update metadata with the given keyword arguments."""
        if "change_image_number" in kwargs:
            data = kwargs["n_images"]
            self.metadata["number_of_images"] = data
            # for cam_id, cam in enumerate(data):
            #     self.metadata["number_of_images"][cam] =  data

        if "change_label" in kwargs:
            label = kwargs["label"]
            self.metadata["label"] = label

        if "change_pd" in kwargs:
            data = kwargs["pd"]
            self.metadata["pose_detection"].update(data)

        if "change_triangulate" in kwargs:
            data = kwargs["triangulate"]
            self.metadata["triangulate"] = data

        if "change_feature_extraction" in kwargs:
            data = kwargs["feature_extraction"]
            self.metadata["feature_extraction"] = data

        if "change_feature_extraction" in kwargs:
            data = kwargs["feature_extraction"]
            self.metadata["feature_extraction"] = data

        json_loc = os.path.join("data/", str(self.ts), "experiment.json")
        self.um.dump_json(fname=json_loc, data=self.metadata, pretty=True)

    def load_experiment(self, ts):
        """Load metadata from the the json file."""
        json_loc = os.path.join("data/", str(ts), "experiment.json")
        metadata = self.um.read_json(json_loc)
        return metadata

    def create_folders(self, ts):
        """Create necessary folders needed for each experiment."""

        # Create folder list for the experiment
        folders = list()
        for subfolder in self.subfolders:
            folders.append(os.path.join("data/", str(ts), subfolder))

        # Check if they exist, if they don't create them one by one
        for folder in folders:
            exists = self.um.check_folder_exists(folder)
            if exists is False:
                self.um.create_folder(folder)

    def create_metadata(self, ts, camera_names, room):
        """Create a metadata with default values."""
        json_loc = os.path.join("data/", str(ts), "experiment.json")

        ncamera = len(camera_names)
        number_of_images = dict()
        pose_detection = dict()

        for camera in camera_names:
            number_of_images[camera] = 0
            pose_detection[camera] = 0

        metadata = {"id": ts,
                    "start_time": str(self.um.timestamp_to_date(ts/1000)),
                    "room": room,
                    "number_of_cameras": ncamera,
                    "number_of_images": number_of_images,
                    "pose_detection": pose_detection,
                    "thumbnails": False,
                    "feature_extraction": False,
                    "feature_matching": False,
                    "triangulation": False,
                    "state_estimation": False,
                    "label": None}

        return metadata
