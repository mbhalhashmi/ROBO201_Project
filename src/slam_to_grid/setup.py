from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'slam_to_grid'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/maps',
         [os.path.join(maps_dir, f) for f in os.listdir(maps_dir)
          if os.path.isfile(os.path.join(maps_dir, f))]),
    ],
    install_requires=['setuptools', 'numpy', 'matplotlib', 'PyYAML', 'ament_index_python'],
    zip_safe=True,
    maintainer='mohamed',
    maintainer_email='mbh.alhashmi@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'read_map = slam_to_grid.read_map:main',
        ],
    },
)
