import os
from setuptools import setup
from glob import glob

package_name = 'coupe'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name),glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rir',
    maintainer_email='leo.mourgues@gmail.com',
    description='packet completpour CDFR2023',
    license='LRM',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'master = coupe.master:main',
        	'moteur = coupe.odrive_srv:main',
        	'Lidar = coupe.lidar_pub:main',
        	'actionneur = coupe.arduino_com:main',
        ],
    },
)
