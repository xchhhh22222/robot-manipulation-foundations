from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def generate_launch_description():

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
        .joint_limits(
            file_path="config/joint_limits.yaml"
        )
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        )
        .to_moveit_configs()
    )

    return generate_move_group_launch(moveit_config)