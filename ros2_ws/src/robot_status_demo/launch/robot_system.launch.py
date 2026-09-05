from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
Node(
    package='robot_status_demo',
    executable='robot_status_publisher',
    name='robot_status_publisher',
    parameters=[
        {
            'publish_interval': 0.5
        }
    ]
),

        Node(
            package='robot_status_demo',
            executable='robot_status_monitor',
            name='robot_status_monitor'
        ),

        Node(
            package='robot_status_demo',
            executable='robot_gripper_control_server',
            name='robot_gripper_control_server'
        ),

        Node(
            package='robot_status_demo',
            executable='robot_move_action_server',
            name='robot_move_action_server'
        ),

    ])