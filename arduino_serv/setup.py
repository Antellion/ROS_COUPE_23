from setuptools import setup

package_name = 'arduino_serv'

setup(
    name=package_name,
    version='0.0.0',
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
    description='test de la comm avec arduino',
    license='LRM',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'serveur = arduino_serv.arduino_com:main',
        	'client = arduino_serv.test_client:main',
        ],
    },
)
