"""This class implements stuff about the skeleton data structure."""
from __future__ import division
import numpy as np


class people(object):
    """docstring for people."""
    def __init__(self, json, frame=None):
        super(people, self).__init__()
        self.json = json
        self.json = np.asarray(self.json).reshape(-1, 25, 3)
        self.list = list()
        for person_id, person in enumerate(self.json):
            self.list.append(skeleton(person, person_id=person_id, frame=frame))


class skeleton(object):
    """This class implements stuff about the skeleton data structure."""

    def __init__(self, joint_data, person_id=None, frame=None):
        """Initialize the class."""
        super(skeleton, self).__init__()
        self.n_joint = 25
        self.frame = frame
        self.person_id = person_id
        self.joint_locs = np.array(joint_data)
        self.joint_locs = self.joint_locs.reshape(-1, 3)
        self.bone_list = np.array([[0, 16],
                                   [0, 15],
                                   [1,  0],
                                   [1,  8],
                                   [1,  5],
                                   [1,  2],
                                   [2, 17],
                                   [2,  3],
                                   [3,  4],
                                   [5,  6],
                                   [5, 18],
                                   [6,  7],
                                   [8,  9],
                                   [8, 12],
                                   [9, 10],
                                   [10, 11],
                                   [11, 22],
                                   [11, 24],
                                   [12, 13],
                                   [13, 14],
                                   [14, 19],
                                   [14, 21],
                                   [15, 17],
                                   [16, 18],
                                   [19, 20],
                                   [22, 23]])
        self.bone_colors = np.random.rand(len(self.bone_list), 3, 1)

        self.names = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist",
                      "LShoulder", "LElbow", "LWrist", "MidHip",
                      "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle",
                      "REye", "LEye", "REar", "LEar", "LBigToe",
                      "LSmallToe", "LHeel", "RBigToe", "RSmallToe",
                      "RHeel", "Background"]

        self.nose = joint(joint_id=0, name=self.names[0],
                          loc2d=self.joint_locs[0, 0:2],
                          conf=self.joint_locs[0, 2])
        self.neck = joint(joint_id=1, name=self.names[1],
                          loc2d=self.joint_locs[1, 0:2],
                          conf=self.joint_locs[1, 2])
        self.rshoulder = joint(joint_id=2, name=self.names[2],
                               loc2d=self.joint_locs[2, 0:2],
                               conf=self.joint_locs[2, 2])
        self.relbow = joint(joint_id=3, name=self.names[3],
                            loc2d=self.joint_locs[3, 0:2],
                            conf=self.joint_locs[3, 2])
        self.rwrist = joint(joint_id=4, name=self.names[4],
                            loc2d=self.joint_locs[4, 0:2],
                            conf=self.joint_locs[4, 2])
        self.lshoulder = joint(joint_id=5, name=self.names[5],
                               loc2d=self.joint_locs[5, 0:2],
                               conf=self.joint_locs[5, 2])
        self.lelbow = joint(joint_id=6, name=self.names[6],
                            loc2d=self.joint_locs[6, 0:2],
                            conf=self.joint_locs[6, 2])
        self.lwrist = joint(joint_id=7, name=self.names[7],
                            loc2d=self.joint_locs[7, 0:2],
                            conf=self.joint_locs[7, 2])
        self.midhip = joint(joint_id=8, name=self.names[8],
                            loc2d=self.joint_locs[8, 0:2],
                            conf=self.joint_locs[8, 2])
        self.rhip = joint(joint_id=9, name=self.names[9],
                          loc2d=self.joint_locs[9, 0:2],
                          conf=self.joint_locs[9, 2])
        self.rknee = joint(joint_id=10, name=self.names[10],
                           loc2d=self.joint_locs[10, 0:2],
                           conf=self.joint_locs[10, 2])
        self.rankle = joint(joint_id=11, name=self.names[11],
                            loc2d=self.joint_locs[11, 0:2],
                            conf=self.joint_locs[11, 2])
        self.lhip = joint(joint_id=12, name=self.names[12],
                          loc2d=self.joint_locs[12, 0:2],
                          conf=self.joint_locs[12, 2])
        self.lknee = joint(joint_id=13, name=self.names[13],
                           loc2d=self.joint_locs[13, 0:2],
                           conf=self.joint_locs[13, 2])
        self.lankle = joint(joint_id=14, name=self.names[14],
                            loc2d=self.joint_locs[14, 0:2],
                            conf=self.joint_locs[14, 2])
        self.reye = joint(joint_id=15, name=self.names[15],
                          loc2d=self.joint_locs[15, 0:2],
                          conf=self.joint_locs[15, 2])
        self.leye = joint(joint_id=16, name=self.names[16],
                          loc2d=self.joint_locs[16, 0:2],
                          conf=self.joint_locs[16, 2])
        self.rear = joint(joint_id=17, name=self.names[17],
                          loc2d=self.joint_locs[17, 0:2],
                          conf=self.joint_locs[17, 2])
        self.lear = joint(joint_id=18, name=self.names[18],
                          loc2d=self.joint_locs[18, 0:2],
                          conf=self.joint_locs[18, 2])
        self.lbigtoe = joint(joint_id=19, name=self.names[19],
                             loc2d=self.joint_locs[19, 0:2],
                             conf=self.joint_locs[19, 2])
        self.lsmalltoe = joint(joint_id=20, name=self.names[20],
                               loc2d=self.joint_locs[20, 0:2],
                               conf=self.joint_locs[20, 2])
        self.lheel = joint(joint_id=21, name=self.names[21],
                           loc2d=self.joint_locs[21, 0:2],
                           conf=self.joint_locs[21, 2])
        self.rbigtoe = joint(joint_id=22, name=self.names[22],
                             loc2d=self.joint_locs[22, 0:2],
                             conf=self.joint_locs[22, 2])
        self.rsmalltoe = joint(joint_id=23, name=self.names[23],
                               loc2d=self.joint_locs[23, 0:2],
                               conf=self.joint_locs[23, 2])
        self.rheel = joint(joint_id=24, name=self.names[24],
                           loc2d=self.joint_locs[24, 0:2],
                           conf=self.joint_locs[24, 2])
        # self.background = joint(joint_id=25, name=self.names[25],
        #                         loc2d=self.joint_locs[25, 0:2],
        #                         conf=self.joint_locs[25, 2])


class joint(object):
    """This class implements stuff about the joint data structure."""

    def __init__(self, joint_id, name, loc2d=None, conf=None, loc3d=None):
        """Initialize the class."""
        super(joint, self).__init__()
        self.id = joint_id
        self.name = name
        self.loc2d = loc2d
        self.conf = conf
        self.loc3d = loc3d


if __name__ == '__main__':
    pass
