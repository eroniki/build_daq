
self.xform_tree = TFTree()
self.extrinsic_dict = self.load_extrinsics()
self.K, self.d = self.load_intrinsics()

for elem in self.extrinsic_dict["extrinsic_params"]:
    self.xform_tree.add_transform(parent=elem["left"],
                                    child=elem["right"],
                                    xform=elem["matrix"])


def load_extrinsics(self):
        """Load extrinsic matrices from a json file."""
        return self.um.read_json("extrinsics.json")

def load_intrinsics(self):
    """Load intrinsic parameters from a json file."""
    data = self.um.read_json("intrinsics.json")
    K = np.asarray(data["K"])
    d = np.asarray(data["dist"])
    return K, d
