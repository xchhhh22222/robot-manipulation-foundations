import os
import time

import rclpy

from geometry_msgs.msg import PoseStamped
from moveit.planning import MoveItPy


def main():
    rclpy.init()

    print("正在启动 MoveItPy...", flush=True)

    moveit = MoveItPy(
        node_name="moveit_6dof_pose_demo"
    )

    arm = moveit.get_planning_component("arm")

    print("MoveItPy 启动成功", flush=True)

    time.sleep(1.0)

    # 当前 HOME：
    # x = 0.800
    # y = 0.000
    # z = 0.600
    #
    # 第一次 Pose Target：
    # 让末端向机器人方向收回 10 cm
    target_pose = PoseStamped()

    target_pose.header.frame_id = "base_link"

    target_pose.pose.position.x = 0.70
    target_pose.pose.position.y = 0.00
    target_pose.pose.position.z = 0.60

    # 保持 HOME 时的末端姿态不变
    target_pose.pose.orientation.x = 0.0
    target_pose.pose.orientation.y = 0.0
    target_pose.pose.orientation.z = 0.0
    target_pose.pose.orientation.w = 1.0

    print("目标 Pose:", flush=True)
    print("  x = 0.70", flush=True)
    print("  y = 0.00", flush=True)
    print("  z = 0.60", flush=True)

    # 起点 = 当前机械臂状态
    arm.set_start_state_to_current_state()

    # 注意：
    # 我们没有告诉 MoveIt joint1~joint6 应该是多少。
    # 只告诉它 tool_link 应该到这个 Pose。
    arm.set_goal_state(
        pose_stamped_msg=target_pose,
        pose_link="tool_link"
    )

    print("开始 IK + OMPL 规划...", flush=True)

    plan_result = arm.plan()

    if not plan_result:
        print("Pose 规划失败", flush=True)
        os._exit(1)

    print("规划成功，开始执行...", flush=True)

    moveit.execute(
        plan_result.trajectory,
        controllers=[]
    )

    print("Pose Target 执行完成", flush=True)

    time.sleep(1.0)

    # Jazzy MoveItPy 当前析构 workaround
    os._exit(0)


if __name__ == "__main__":
    main()
