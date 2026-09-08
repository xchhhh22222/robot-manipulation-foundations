import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # 找到 robot_description 安装后的路径
    package_share = get_package_share_directory(
        'robot_description'
    )

    # URDF 文件路径
    urdf_file = os.path.join(
        package_share,
        'urdf',
        'simple_arm.urdf'
    )

    # 读取 URDF 内容
    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([

        # 根据 URDF + joint_states 发布 TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        # GUI 滑块，发布 /joint_states
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        # 启动 RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2'
        ),

    ])