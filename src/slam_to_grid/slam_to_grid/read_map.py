import yaml
import numpy as np
import matplotlib.pyplot as plt
import os

#Defining where the yaml files are
home_dir = os.path.expanduser("~")
yaml_path = os.path.join(home_dir, "my_robot_map_real.yaml")

def load_map(yaml_path):
    """ Reads a .yaml and .pgm map and returns a numpy grid
    0 = free
    1 = occupied
    -1 = unknown

    resolution: size of each grid cell in meters (gotten from YAML data)
    """

    #
    with open(yaml_path, 'r') as f:#read yaml file
        pgm_path = meta['image']
        res = meta['resolution']
        occ_t = meta['occupied_thresh']
        free_t = meta['free_thresh']

    # Read the 

