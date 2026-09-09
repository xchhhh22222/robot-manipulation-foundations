import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_share = get_package_share_directory(
        'robot_description'
    )

    xacro_file = os.path.join(
        package_share,
        'urdf',
        'simple_arm.urdf.xacro'
    )

    rviz_config = os.path.join(
        package_share,
        'rviz',
        'simple_arm.rviz'
    )

    # 获取 launch 外部传入的参数
    link2_length = LaunchConfiguration(
        'link2_length'
    )

    # 运行 xacro，并把 launch 参数传给 xacro
    robot_description = ParameterValue(
        Command([
            'xacro ',
            xacro_file,
            ' link2_length:=',
            link2_length
        ]),
        value_type=str
    )

    return LaunchDescription([

        # 声明 launch 参数
        DeclareLaunchArgument(
            'link2_length',
            default_value='0.4',
            description='Length of link2 in meters'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d',
                rviz_config
            ]
        ),

    ])