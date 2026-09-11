#!/usr/bin/env python3

import csv
import time
from pathlib import Path

import rclpy
from rclpy.logging import get_logger

from geometry_msgs.msg import PoseStamped

from ament_index_python.packages import get_package_share_directory

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState
from moveit_configs_utils import MoveItConfigsBuilder


# ============================================================
# 保存 MoveIt 规划出来的关节轨迹
# ============================================================
def save_trajectory_csv(plan_result, output_file):

    trajectory_msg = (
        plan_result.trajectory.get_robot_trajectory_msg()
    )

    trajectory = trajectory_msg.joint_trajectory

    # 确保 results 文件夹存在
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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

    # ========================================================
    # 0. 初始化 ROS2
    # ========================================================
    rclpy.init()

    logger = get_logger(
        "moveit_explicit_ik_demo"
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
    # 3. 创建 MoveItPy
    # ========================================================
    robot = MoveItPy(
        node_name="moveit_py_explicit_ik_demo",
        config_dict=moveit_config
    )

    arm = robot.get_planning_component(
        "arm"
    )

    logger.info(
        "MoveItPy initialized"
    )

    logger.info(
        "Waiting for controller action discovery..."
    )

    time.sleep(5.0)

    # ========================================================
    # 4. 创建末端执行器目标 Pose
    # ========================================================
    pose_goal = PoseStamped()

    # 当前机器人没有 virtual joint，
    # model frame 就是 base_link
    pose_goal.header.frame_id = "base_link"

    # 目标姿态
    # 大约绕 Y 轴 21 度
    pose_goal.pose.orientation.x = 0.0
    pose_goal.pose.orientation.y = 0.184
    pose_goal.pose.orientation.z = 0.0
    pose_goal.pose.orientation.w = 0.983

    # 目标位置
    pose_goal.pose.position.x = 0.300
    pose_goal.pose.position.y = 0.0
    pose_goal.pose.position.z = 0.450

    logger.info(
        "Pose target: "
        "tool_link -> "
        "(0.300, 0.000, 0.450)"
    )

    # ========================================================
    # 5. 显式进行 IK 求解
    # ========================================================

    # 获取 MoveIt 内部的 RobotModel
    robot_model = robot.get_robot_model()

    # 创建一个 RobotState
    ik_state = RobotState(
        robot_model
    )

    # 给 IK 一个初始猜测
    # 对我们这个机器人就是接近 home 状态
    ik_state.set_to_default_values()

    logger.info(
        "Solving inverse kinematics..."
    )

    # --------------------------------------------------------
    # 关键：
    #
    # 输入：
    #   tool_link 的目标 Pose
    #
    # 输出：
    #   joint1 / joint2
    #
    # 这一步就是 IK
    # --------------------------------------------------------
    ik_success = ik_state.set_from_ik(
        "arm",
        pose_goal.pose,
        "tool_link",
        1.0
    )

    if not ik_success:

        logger.error(
            "IK failed"
        )

        return

    # 更新机器人状态中的 FK 数据
    ik_state.update()

    # 读取 IK 求出来的关节角
    ik_solution = (
        ik_state.get_joint_group_positions(
            "arm"
        )
    )

    logger.info(
        "IK succeeded"
    )

    logger.info(
        f"IK solution: "
        f"joint1={ik_solution[0]:.6f}, "
        f"joint2={ik_solution[1]:.6f}"
    )

    # ========================================================
    # 6. 设置 MoveIt 规划起点和目标
    # ========================================================

    # 起点：
    # 当前真实机器人状态
    arm.set_start_state_to_current_state()

    # 目标：
    # 刚刚 IK 求出来的 RobotState
    arm.set_goal_state(
        robot_state=ik_state
    )

    logger.info(
        "Planning current state -> IK solution"
    )

    # ========================================================
    # 7. OMPL 进行路径规划
    # ========================================================
    plan_result = arm.plan()

    if not plan_result:

        logger.error(
            "Planning failed"
        )

        return

    logger.info(
        "Planning succeeded"
    )

    # ========================================================
    # 8. 保存规划轨迹
    # ========================================================
    output_file = (
        Path(__file__).parent.parent
        / "results"
        / "explicit_ik.csv"
    )

    save_trajectory_csv(
        plan_result,
        output_file
    )

    logger.info(
        f"Saved trajectory to {output_file}"
    )

    # ========================================================
    # 9. 执行轨迹
    # ========================================================
    logger.info(
        "Executing trajectory"
    )

    execution_status = robot.execute(
        plan_result.trajectory,
        controllers=["arm_controller"]
    )

    logger.info(
        f"Trajectory execution status: "
        f"{execution_status}"
    )


if __name__ == "__main__":
    main()