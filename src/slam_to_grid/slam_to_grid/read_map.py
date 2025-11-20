import yaml
import numpy as np
import matplotlib.pyplot as plt
import os

#Defining where the yaml files are
pkg_dir = os.path.expanduser(__file__)
yaml_path = os.path.join(pkg_dir, "my_robot_map_real.yaml")

# Reading the YAML data

with open(yaml_path, "r") as f:
    data = yaml.safe_load(f)

# Image path
image_path = os.path.join(os.path.dirname(yaml_path), data["image"])

# Getting the yaml data
resolution = data["resolution"]
occ_t = data["occupied_thresh"]
free_t = data["free_thresh"]

# Load the PGM map image
gray = plt.imread(image_path).astype(float)