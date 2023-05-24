from setuptools import setup

package_name = 'action_odrive'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rir',
    maintainer_email='leo.mourgues@gmail.com',
    description='commande de la carte odrive',
    license='LRM',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'serveur = action_odrive.odrive_srv:main',
        	'client = action_odrive.client_odrive:main',
        	'Lidar = action_odrive.lidar_pub:main',
        ],
    },
)
