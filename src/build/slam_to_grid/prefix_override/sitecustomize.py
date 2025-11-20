import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mohamed/ROBO201_Project/src/install/slam_to_grid'
