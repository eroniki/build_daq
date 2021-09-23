import numpy as np
from collections import namedtuple


class TFTree(object):
    def __init__(self):
        self.nodes = {}

    def to_dict(self):
        return [v.to_dict() for k, v in self.nodes.items()]

    @classmethod
    def from_dict(cls, inlist):
        out = cls()
        for v in inlist:
            n = TFNode.from_dict(v)
            if not n.parent:  # root encountered
                continue
            out.add_transform(n.parent.name, n.name, n.transform)
        return out

    def add_transform(self, parent, child, xform):
        if parent not in self.nodes:
            self.nodes[parent] = TFNode(parent, None, None)

        if child not in self.nodes:
            self.nodes[child] = TFNode(child, self.nodes[parent], xform)
        else:
            node = self.nodes[child]
            node.parent = self.nodes[parent]
            node.transform = xform

    def get_parent(self):
        parent_nodes = []

        for name, node in self.nodes.items():
            if not node.parent:
                parent_nodes.append(node)

        if len(parent_nodes) > 1:
            raise Exception(
                "More than one tree found, this case is unsupported")
        if len(parent_nodes) == 0:
            raise Exception(
                "No parent node found, there are probably cycles in the tree")

        return parent_nodes[0]

    def lookup_transform(self, frame, target):
        if target not in self.nodes:
            raise Exception("target is not part of the tf tree")
        if frame not in self.nodes:
            raise Exception("frame is not part of the tf tree")
        if target == frame:
            return np.eye(4)

        parent_node = self.get_parent()

        frame_path_to_parent = self._get_path_to_parent(parent_node, target)
        target_path_to_parent = self._get_path_to_parent(parent_node, frame)

        while True and len(frame_path_to_parent) > 0 and len(target_path_to_parent) > 0:
            if frame_path_to_parent[-1] == target_path_to_parent[-1]:
                frame_path_to_parent.pop()
                target_path_to_parent.pop()
            else:
                break

        # Note: I do not understand why the part below works

        def get_inverse_xform_for_path(path):
            transform_to_parent = np.identity(4)
            for node in path:
                transform_to_parent = np.dot(
                    node.transformation_matrix, transform_to_parent)
            return transform_to_parent

        frame_transform_to_common_parent = get_inverse_xform_for_path(
            frame_path_to_parent)
        target_transform_to_common_parent = get_inverse_xform_for_path(
            target_path_to_parent)

        final_xform = np.dot(np.linalg.inv(
            target_transform_to_common_parent), frame_transform_to_common_parent)

        return np.linalg.inv(final_xform)

    def _get_path_to_parent(self, parent_node, node_name):
        if node_name == parent_node.name:
            return []

        node = self.nodes[node_name]
        traversed_nodes = {}
        path = []
        while True:
            if node in traversed_nodes:
                raise Exception("Cycle detected, this case is unsupported")
            traversed_nodes[node] = True
            path.append(node)
            node = node.parent
            if node == parent_node:
                break

        return path

    def transform_point(self, x, y, z, target, base):
        t = self.lookup_transform(base, target)
        return np.dot(t, np.array([x, y, z, 1]))[0:3]


class TFNode(object):
    def __init__(self, name, parent, transform):
        self.parent = parent
        self.name = name
        self.transform = transform

    def to_dict(self):
        return {'parent': self.parent.name if self.parent else self.parent,
                'name': self.name,
                'transform': self.transform if hasattr(self.transform, 'shape') else None}

    @classmethod
    def from_dict(cls, indict):
        parent, xform = indict['parent'], indict['transform']
        parent = TFNode(parent, None, None) if parent else None
        # xform = Transform.from_dict(xform) if xform else None
        return cls(indict['name'], parent, xform)

    @property
    def transformation_matrix(self):
        if self.transform is None:
            return np.identity(4)
        return self.transform
