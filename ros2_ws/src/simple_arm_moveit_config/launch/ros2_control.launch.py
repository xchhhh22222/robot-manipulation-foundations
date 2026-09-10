import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import xacro


def generate_launch_description():

    # -------------------------
    # 1. 找到机器人描述包
    # -------------------------
    robot_description_share = get_package_share_directory(
        'robot_description'
    )

    # -------------------------
    # 2. 找到 MoveIt 配置包
    # -------------------------
    moveit_config_share = get_package_share_directory(
        'simple_arm_moveit_config'
    )

    # -------------------------
    # 3. Xacro 文件
    # -------------------------
    xacro_file = os.path.join(
        robot_description_share,
        'urdf',
        'simple_arm.urdf.xacro'
    )

    # -------------------------
    # 4. ros2_control 控制器配置
    # -------------------------
    controllers_file = os.path.join(
        moveit_config_share,
        'config',
        'ros2_controllers.yaml'
    )

    # -------------------------
    # 5. Xacro -> URDF
    # -------------------------
    robot_description_config = xacro.process_file(
        xacro_file
    )

    robot_description = {
        'robot_description':
            robot_description_config.toxml()
    }

    # -------------------------
    # 6. robot_state_publisher
    # -------------------------
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            robot_description
        ]
    )

    # -------------------------
    # 7. ros2_control
    # -------------------------
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[
            controllers_file
        ]
    )

    # -------------------------
    # 8. joint_state_broadcaster
    # -------------------------
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    # -------------------------
    # 9. arm_controller
    # -------------------------
    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
    ])