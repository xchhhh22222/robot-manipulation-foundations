from pathlib import Path

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # robot_description 包里的机器人 Xacro
    robot_xacro = (
        Path(get_package_share_directory("robot_description"))
        / "urdf"
        / "simple_arm.urdf.xacro"
    )

    # 把 MoveIt 所需要的各种配置组合起来
    moveit_config = (
        MoveItConfigsBuilder(
            "simple_arm",
            package_name="simple_arm_moveit_config"
        )

        # URDF / Xacro：机器人本体
        .robot_description(
            file_path=robot_xacro
        )

        # SRDF：arm 规划组、home 等语义信息
        .robot_description_semantic(
            file_path="config/simple_arm.srdf"
        )

        # IK 配置
        .robot_description_kinematics(
            file_path="config/kinematics.yaml"
        )

        # 关节速度/加速度限制
        .joint_limits(
            file_path="config/joint_limits.yaml"
        )

        # MoveIt -> arm_controller
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        )

        # OMPL / RRTConnect
        .planning_pipelines(
            pipelines=["ompl"],
            default_planning_pipeline="ompl"
        )

        # 发布 Planning Scene 等信息
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True
        )

        .to_moveit_configs()
    )

    # MoveIt 的核心节点
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict()
        ]
    )

    return LaunchDescription([
        move_group_node
    ])