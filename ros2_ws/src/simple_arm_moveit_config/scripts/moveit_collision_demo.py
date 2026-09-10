#!/usr/bin/env python3

import csv
import time
from pathlib import Path

import rclpy
from rclpy.logging import get_logger

from geometry_msgs.msg import Pose
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive

from ament_index_python.packages import get_package_share_directory
from moveit.planning import MoveItPy
from moveit_configs_utils import MoveItConfigsBuilder


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


def main():


    # -----------------------------
    # 0. 初始化 ROS2
    # -----------------------------
    rclpy.init()

    logger = get_logger("moveit_collision_demo")

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
        node_name="moveit_py_collision_demo",
        config_dict=moveit_config
    )

    # SRDF 中定义的 arm group
    arm = robot.get_planning_component("arm")

    logger.info("MoveItPy initialized")

    # -----------------------------
    # 4. 添加 Planning Scene 障碍物
    # -----------------------------
    planning_scene_monitor = robot.get_planning_scene_monitor()

    with planning_scene_monitor.read_write() as scene:

        collision_object = CollisionObject()

        # 障碍物使用 base_link 坐标系
        collision_object.header.frame_id = "base_link"

        # 障碍物名称
        collision_object.id = "obstacle_box"

        # 创建长方体
        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX

        # x, y, z 尺寸，单位 m
        box.dimensions = [
            0.10,
            0.20,
            0.10
        ]

        # 障碍物中心位置
        box_pose = Pose()
        box_pose.position.x = 0.20
        box_pose.position.y = 0.0
        box_pose.position.z = 0.50

        # 单位四元数，不旋转
        box_pose.orientation.w = 1.0

        collision_object.primitives.append(box)
        collision_object.primitive_poses.append(box_pose)

        collision_object.operation = CollisionObject.ADD

        scene.apply_collision_object(
            collision_object
        )

        scene.current_state.update()

    # 注意：这里已经退出 with
    logger.info("Added obstacle_box to planning scene")

    # -----------------------------
    # 5. 等待 Controller Action 发现
    # -----------------------------
    logger.info("Waiting for controller action discovery...")
    time.sleep(5.0)

    # -----------------------------
    # 6. 起点 = 当前真实关节状态
    # -----------------------------
    arm.set_start_state_to_current_state()

    # -----------------------------
    # 7. 目标 = ready
    # -----------------------------
    arm.set_goal_state(
        configuration_name="ready"
    )

    logger.info("Planning current state -> ready")

    # -----------------------------
    # 8. MoveIt 自动规划
    # -----------------------------
    plan_result = arm.plan()

    if not plan_result:
        logger.error("Planning failed")
        return

    logger.info("Planning succeeded")

    output_file = (
        Path(__file__).parent.parent
        / "results"
        / "with_obstacle.csv"
    )

    save_trajectory_csv(
        plan_result,
        output_file
    )

    logger.info(
        f"Saved trajectory to {output_file}"
    )



    trajectory_msg = plan_result.trajectory.get_robot_trajectory_msg()
    trajectory = trajectory_msg.joint_trajectory

    logger.info("Planned joint trajectory:")

    for i, point in enumerate(trajectory.points):
        logger.info(
            f"Point {i}: "
            f"positions={list(point.positions)}, "
            f"time={point.time_from_start.sec}."
            f"{point.time_from_start.nanosec:09d}s"
        )



    # -----------------------------
    # 9. 执行规划轨迹
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