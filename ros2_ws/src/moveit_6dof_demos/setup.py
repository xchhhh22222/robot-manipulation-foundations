import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'moveit_6dof_demos'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wanxincheng',
    maintainer_email='3324049617@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joint_target_demo = moveit_6dof_demos.joint_target_demo:main',
            'pose_target_demo = moveit_6dof_demos.pose_target_demo:main',
        ],
    },
)
