#!/usr/bin/env python3
import time
import csv
from pathlib import Path
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.logging import get_logger

from ament_index_python.packages import get_package_share_directory
from moveit.planning import MoveItPy
from moveit_configs_utils import MoveItConfigsBuilder


def main():

    def save_trajectory_csv(plan_result, output_file):

        trajectory_msg = (
            plan_result.trajectory.get_robot_trajectory_msg()
        )

        trajectory = trajectory_msg.joint_trajectory

        with open(output_file, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "time_sec",
                "joint1",
                "joint2"
            ])

            for point in trajectory.points:

                time_sec = (
                    point.time_from_start.sec
                    + point.time_from_start.nanosec / 1e9
                )

                writer.writerow([
                    time_sec,
                    point.positions[0],
                    point.positions[1]
                ])
    # rclpy 这里主要用于日志
    rclpy.init()

    logger = get_logger("moveit_pose_target_demo")

    # -----------------------------
    # 1. 找到机器人 Xacro
    # -----------------------------
    robot_xacro = (
        Path(get_package_share_directory("robot_description"))
        / "urdf"
        / "simple_arm.urdf.xacro"
    )

    # -----------------------------
    # 2. 组装 MoveIt 配置
    # -----------------------------
    moveit_config = (
        MoveItConfigsBuilder(
            "simple_arm",
            package_name="simple_arm_moveit_config"
        )

        .robot_description(
            file_path=robot_xacro
        )

        .robot_description_semantic(
            file_path="config/simple_arm.srdf"
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
            file_path="config/moveit_cpp.yaml"
        )

        .to_moveit_configs()
        .to_dict()
    )

    # -----------------------------
    # 3. 创建 MoveItPy
    # -----------------------------
    robot = MoveItPy(
        node_name="moveit_py_demo",
        config_dict=moveit_config
    )

    # SRDF 中定义的 arm group
    arm = robot.get_planning_component("arm")

    logger.info("MoveItPy initialized")
    logger.info("Waiting for controller action discovery...")
    time.sleep(5.0)
    # -----------------------------
    # 4. 起点 = 当前真实关节状态
    # -----------------------------
    arm.set_start_state_to_current_state()

    # -----------------------------
    # 5. 目标 = SRDF 中的 ready
    # -----------------------------


    # -----------------------------
    # 5. 设置末端执行器目标位置
    # -----------------------------
    pose_goal = PoseStamped()

    # 目标位置是相对于 base_link 描述的
    pose_goal.header.frame_id = "base_link"

    # 必须给一个合法四元数
    # 因为我们开启了 position_only_ik，
    # KDL 主要考虑位置，不要求机械臂满足这个姿态
    pose_goal.pose.orientation.x = 0.0
    pose_goal.pose.orientation.y = 0.184
    pose_goal.pose.orientation.z = 0.0
    pose_goal.pose.orientation.w = 0.983

    # 我们刚才通过 FK 验证过的位置
    pose_goal.pose.position.x = 0.300
    pose_goal.pose.position.y = 0.0
    pose_goal.pose.position.z = 0.450

    arm.set_goal_state(
        pose_stamped_msg=pose_goal,
        pose_link="tool_link"
    )

    logger.info(
        "Pose target: tool_link -> "
        "(0.300, 0.000, 0.450)"
    )



    logger.info("Planning current state -> pose target")

    # -----------------------------
    # 6. MoveIt 自动规划
    # -----------------------------
    plan_result = arm.plan()

    if not plan_result:
        logger.error("Planning failed")
        return

    logger.info("Planning succeeded")

    output_file = (
        Path(__file__).parent.parent
        / "results"
        / "pose_target.csv"
    )

    save_trajectory_csv(
        plan_result,
        output_file
    )

    logger.info(
        f"Saved trajectory to {output_file}"
    )


    # -----------------------------
    # 7. 执行规划轨迹
    # -----------------------------
    logger.info("Executing trajectory")

    execution_status = robot.execute(
        plan_result.trajectory,
        controllers=["arm_controller"]
    )

    logger.info(
        f"Trajectory execution status: {execution_status}"
    )


if __name__ == "__main__":
    main()