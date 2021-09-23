"""This class implements tools needed for visualization."""
from __future__ import division
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class visualization(object):
    """docstring for visualization."""

    def __init__(self):
        """Creates a figure in which detected skeletons are drawn."""
        super(visualization, self).__init__()

    @staticmethod
    def draw_matchsticks(people, fname, frame_width=640, frame_height=480):
        f = plt.figure(figsize=plt.figaspect(1))
        ax = f.add_subplot(1, 1, 1)
        f.set_figwidth(8)
        f.set_figheight(6)
        ax.set_xlim([0, frame_width])
        ax.set_ylim([0, frame_height])
        ax.set_xlabel("X [pixels]")
        ax.set_ylabel("Y [pixels]")
        ax.invert_yaxis()
        
        if len(people.list)>0:
            ax.set_title("Person Localization Frame: "+str(people.list[0].frame))

        for person in people.list:
            for bone_id, bone in enumerate(person.bone_list):
                color = person.bone_colors[bone_id].ravel()

                if not np.any(person.joint_locs[bone] == 0):
                    ax.plot([person.joint_locs[bone[0], 0],
                             person.joint_locs[bone[1], 0]],
                            [person.joint_locs[bone[0], 1],
                             person.joint_locs[bone[1], 1]],
                            color=color)

        f.savefig(fname)
        plt.close()
