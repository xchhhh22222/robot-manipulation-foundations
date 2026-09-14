import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node


from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory(
        "simple_6dof_description"
    )

    xacro_file = os.path.join(
        pkg_path,
        "urdf",
        "simple_6dof_arm.urdf.xacro"
    )


    robot_description = Command(
        [
            "xacro ",
            xacro_file
        ]
    )


    return LaunchDescription([


        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
           parameters=[
    {
        "robot_description":
        ParameterValue(
            robot_description,
            value_type=str
        )
    }
        ],
            output="screen"
        ),


        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen"
        )

    ])