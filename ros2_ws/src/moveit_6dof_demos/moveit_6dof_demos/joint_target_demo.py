import os
import time

import rclpy

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState


def move_to(moveit, arm, joint_positions, name):
    print(f"\n准备前往：{name}", flush=True)

    robot_model = moveit.get_robot_model()
    goal_state = RobotState(robot_model)

    goal_state.joint_positions = joint_positions

    arm.set_start_state_to_current_state()
    arm.set_goal_state(robot_state=goal_state)

    print(f"开始规划：{name}", flush=True)

    plan_result = arm.plan()

    if not plan_result:
        print(f"规划失败：{name}", flush=True)
        return False

    print(f"规划成功，开始执行：{name}", flush=True)

    moveit.execute(
        plan_result.trajectory,
        controllers=[]
    )

    print(f"执行完成：{name}", flush=True)

    time.sleep(1.0)

    return True


def main():
    rclpy.init()

    print("正在启动 MoveItPy...", flush=True)

    moveit = MoveItPy(
        node_name="moveit_6dof_python"
    )

    arm = moveit.get_planning_component("arm")

    print("MoveItPy 启动成功", flush=True)

    time.sleep(1.0)

    home = {
        "joint1": 0.0,
        "joint2": 0.0,
        "joint3": 0.0,
        "joint4": 0.0,
        "joint5": 0.0,
        "joint6": 0.0,
    }

    ready = {
        "joint1": 0.20,
        "joint2": -0.40,
        "joint3": 0.80,
        "joint4": 0.00,
        "joint5": -0.40,
        "joint6": 0.00,
    }

    if not move_to(moveit, arm, home, "HOME"):
        os._exit(1)

    if not move_to(moveit, arm, ready, "READY"):
        os._exit(1)

    if not move_to(moveit, arm, home, "HOME"):
        os._exit(1)

    print("\nHome → Ready → Home 全部完成", flush=True)

    time.sleep(1.0)

    # Jazzy MoveItPy 析构阶段临时 workaround
    os._exit(0)


if __name__ == "__main__":
    main()