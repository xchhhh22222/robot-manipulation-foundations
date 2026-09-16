import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    moveit_cpp_yaml = os.path.join(
        get_package_share_directory("simple_6dof_moveit_config"),
        "config",
        "moveit_cpp.yaml",
    )

    moveit_config = (
        MoveItConfigsBuilder(
            "simple_6dof_arm",
            package_name="simple_6dof_moveit_config"
        )
        .robot_description(
            file_path="config/simple_6dof_arm.urdf.xacro"
        )
        .robot_description_semantic(
            file_path="config/simple_6dof_arm.srdf"
        )
        .robot_description_kinematics(
            file_path="config/kinematics.yaml"
        )
        .joint_limits(
            file_path="config/joint_limits.yaml"
        )
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        )
        .planning_pipelines(
            pipelines=["ompl"],
            default_planning_pipeline="ompl"
        )
        .moveit_cpp(
            file_path=moveit_cpp_yaml
        )
        .to_moveit_configs()
    )

    moveit_python_node = Node(
        package="moveit_6dof_demos",
        executable="joint_target_demo",
        output="screen",
        parameters=[
            moveit_config.to_dict()
        ],
    )

    return LaunchDescription([
        moveit_python_node
    ])