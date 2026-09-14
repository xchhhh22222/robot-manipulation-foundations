#!/usr/bin/env python3

import csv
from pathlib import Path

import rclpy
from rclpy.logging import get_logger
from rclpy.action import ActionClient

from geometry_msgs.msg import Pose
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState
from moveit_configs_utils import MoveItConfigsBuilder

from ament_index_python.packages import get_package_share_directory


def main():

    rclpy.init()

    logger = get_logger(
        "moveit_cartesian_path_demo"
    )

    # ========================================================
    # 1. 找到机器人 Xacro
    # ========================================================
    robot_xacro = (
        Path(
            get_package_share_directory(
                "robot_description"
            )
        )
        / "urdf"
        / "simple_arm.urdf.xacro"
    )

    # ========================================================
    # 2. 组装 MoveIt 配置
    # ========================================================
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

    # ========================================================
    # 3. 创建 MoveItPy / RobotState
    # ========================================================
    robot = MoveItPy(
        node_name="moveit_py_cartesian_demo",
        config_dict=moveit_config
    )

    robot_model = robot.get_robot_model()

    ik_state = RobotState(
        robot_model
    )

    ik_state.set_to_default_values()

    logger.info(
        "MoveItPy initialized"
    )

    # ========================================================
    # 4. 定义 Cartesian 直线
    # ========================================================
    start_x = 0.400
    start_y = 0.000
    start_z = 0.600

    goal_x = 0.300
    goal_y = 0.000
    goal_z = 0.450

    num_steps = 10

    logger.info(
        "Cartesian line:"
    )

    logger.info(
        f"START = "
        f"({start_x:.3f}, "
        f"{start_y:.3f}, "
        f"{start_z:.3f})"
    )

    logger.info(
        f"GOAL  = "
        f"({goal_x:.3f}, "
        f"{goal_y:.3f}, "
        f"{goal_z:.3f})"
    )

    # ========================================================
    # 5. 逐 waypoint 做 IK
    # ========================================================
    results = []

    joint_waypoints = []

    successful_points = 0

    for i in range(num_steps + 1):

        t = i / num_steps

        # Cartesian interpolation
        x = start_x + t * (
            goal_x - start_x
        )

        y = start_y + t * (
            goal_y - start_y
        )

        z = start_z + t * (
            goal_z - start_z
        )

        waypoint = Pose()

        waypoint.position.x = x
        waypoint.position.y = y
        waypoint.position.z = z

        waypoint.orientation.x = 0.0
        waypoint.orientation.y = 0.0
        waypoint.orientation.z = 0.0
        waypoint.orientation.w = 1.0

        # --------------------------------------------
        # Cartesian waypoint -> IK
        # --------------------------------------------
        ik_success = ik_state.set_from_ik(
            "arm",
            waypoint,
            "tool_link",
            1.0
        )

        if not ik_success:

            logger.error(
                f"P{i:02d} IK FAILED: "
                f"x={x:.3f}, "
                f"y={y:.3f}, "
                f"z={z:.3f}"
            )

            break

        ik_state.update()

        joint_values = (
            ik_state.get_joint_group_positions(
                "arm"
            )
        )

        joint1 = joint_values[0]
        joint2 = joint_values[1]

        successful_points += 1

        results.append([
            i,
            t,
            x,
            y,
            z,
            joint1,
            joint2
        ])

        joint_waypoints.append([
            joint1,
            joint2
        ])

        logger.info(
            f"P{i:02d}: "
            f"xyz=({x:.3f}, "
            f"{y:.3f}, "
            f"{z:.3f}) "
            f"-> "
            f"q=({joint1:.4f}, "
            f"{joint2:.4f})"
        )

    # ========================================================
    # 6. 计算完成比例
    # ========================================================
    total_points = (
        num_steps + 1
    )

    fraction = (
        successful_points
        / total_points
    )

    logger.info(
        f"Cartesian path fraction: "
        f"{fraction:.2f}"
    )

    # 如果路径没有完整生成，就不执行
    if fraction < 1.0:

        logger.error(
            "Cartesian path incomplete. "
            "Trajectory will NOT be executed."
        )

        return

    # ========================================================
    # 7. 保存 waypoint CSV
    # ========================================================
    output_file = (
        Path(__file__).parent.parent
        / "results"
        / "cartesian_waypoints.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "index",
            "t",
            "x",
            "y",
            "z",
            "joint1",
            "joint2"
        ])

        writer.writerows(
            results
        )

    logger.info(
        f"Saved Cartesian waypoints to "
        f"{output_file}"
    )

    # ========================================================
    # 8. 创建 FollowJointTrajectory Action Client
    # ========================================================

    controller_node = rclpy.create_node(
        "cartesian_trajectory_sender"
    )

    action_client = ActionClient(
        controller_node,
        FollowJointTrajectory,
        "/arm_controller/follow_joint_trajectory"
    )

    logger.info(
        "Waiting for arm_controller..."
    )

    if not action_client.wait_for_server(
        timeout_sec=5.0
    ):

        logger.error(
            "arm_controller action server "
            "not available"
        )

        controller_node.destroy_node()
        return

    # ========================================================
    # 9. 把 IK waypoint 变成 JointTrajectory
    # ========================================================

    goal_msg = (
        FollowJointTrajectory.Goal()
    )

    goal_msg.trajectory.joint_names = [
        "joint1",
        "joint2"
    ]

    # 每个 waypoint 相隔 0.4 秒
    time_step = 0.4

    for i, joint_values in enumerate(
        joint_waypoints
    ):

        point = JointTrajectoryPoint()

        point.positions = [
            joint_values[0],
            joint_values[1]
        ]

        time_sec = (
            (i + 1)
            * time_step
        )

        sec = int(time_sec)

        nanosec = int(
            (time_sec - sec)
            * 1e9
        )

        point.time_from_start.sec = sec
        point.time_from_start.nanosec = (
            nanosec
        )

        goal_msg.trajectory.points.append(
            point
        )

    logger.info(
        f"Built trajectory with "
        f"{len(joint_waypoints)} points"
    )

    # ========================================================
    # 10. 发送 trajectory 给 arm_controller
    # ========================================================

    logger.info(
        "Sending Cartesian trajectory..."
    )

    send_goal_future = (
        action_client.send_goal_async(
            goal_msg
        )
    )

    rclpy.spin_until_future_complete(
        controller_node,
        send_goal_future
    )

    goal_handle = (
        send_goal_future.result()
    )

    if not goal_handle.accepted:

        logger.error(
            "Trajectory goal rejected"
        )

        controller_node.destroy_node()
        return

    logger.info(
        "Trajectory goal accepted"
    )

    result_future = (
        goal_handle.get_result_async()
    )

    rclpy.spin_until_future_complete(
        controller_node,
        result_future
    )

    result = (
        result_future.result()
    )

    logger.info(
        f"Trajectory finished. "
        f"status={result.status}"
    )

    logger.info(
        "Cartesian path execution complete"
    )

    controller_node.destroy_node()


if __name__ == "__main__":
    main()