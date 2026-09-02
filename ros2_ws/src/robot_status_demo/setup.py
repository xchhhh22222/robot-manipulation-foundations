from setuptools import find_packages, setup

package_name = 'robot_status_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wanxincheng',
    maintainer_email='3324049617@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [ 'robot_status_publisher = robot_status_demo.robot_status_publisher:main',
        'robot_status_monitor = robot_status_demo.robot_status_monitor:main',
        ],
    },
)
