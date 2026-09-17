import os
import time

import rclpy

from geometry_msgs.msg import Pose
from moveit.core.robot_state import RobotState
from moveit.planning import MoveItPy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive


def publish_obstacle(node, publisher, obstacle):
    """
    将 CollisionObject 多发布几次，
    保证 MoveIt Planning Scene 收到。
    """

    for _ in range(5):

        obstacle.header.stamp = (
            node.get_clock().now().to_msg()
        )

        publisher.publish(obstacle)

        rclpy.spin_once(
            node,
            timeout_sec=0.1
        )

        time.sleep(0.2)


def main():

    rclpy.init()

    print("正在启动 MoveItPy...", flush=True)

    # ============================================================
    # 1. 初始化 MoveIt
    # ============================================================

    moveit = MoveItPy(
        node_name="moveit_6dof_obstacle_demo"
    )

    arm = moveit.get_planning_component("arm")

    print("MoveItPy 启动成功", flush=True)

    # ============================================================
    # 2. 创建 CollisionObject Publisher
    # ============================================================

    scene_node = rclpy.create_node(
        "collision_object_publisher"
    )

    collision_pub = scene_node.create_publisher(
        CollisionObject,
        "/collision_object",
        10
    )

    print(
        "等待 MoveIt 订阅 /collision_object ...",
        flush=True
    )

    start_time = time.time()

    while collision_pub.get_subscription_count() == 0:

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1
        )

        if time.time() - start_time > 5.0:

            print(
                "等待 /collision_object 订阅超时",
                flush=True
            )

            os._exit(1)

    print(
        f"订阅者数量: "
        f"{collision_pub.get_subscription_count()}",
        flush=True
    )

    # ============================================================
    # 3. 创建障碍物
    #
    # 这次不是一堵宽墙，
    # 而是一根竖直障碍柱。
    # ============================================================

    obstacle = CollisionObject()

    obstacle.header.frame_id = "base_link"
    obstacle.id = "sweep_obstacle"

    primitive = SolidPrimitive()
    primitive.type = SolidPrimitive.BOX

    # X / Y 方向比较窄
    # Z 方向比较高
    primitive.dimensions = [
        0.12,
        0.12,
        0.40,
    ]

    obstacle_pose = Pose()

    # 第一阶段：
    # 先放到远处做基准实验
    obstacle_pose.position.x = 0.50
    obstacle_pose.position.y = 1.00
    obstacle_pose.position.z = 0.55

    obstacle_pose.orientation.x = 0.0
    obstacle_pose.orientation.y = 0.0
    obstacle_pose.orientation.z = 0.0
    obstacle_pose.orientation.w = 1.0

    obstacle.primitives.append(
        primitive
    )

    obstacle.primitive_poses.append(
        obstacle_pose
    )

    obstacle.operation = CollisionObject.ADD

    # ============================================================
    # 4. 发布远处障碍物
    # ============================================================

    print(
        "\n========== 实验 A：无障碍基准 ==========",
        flush=True
    )

    print(
        "障碍物暂时放在 y = 1.00",
        flush=True
    )

    publish_obstacle(
        scene_node,
        collision_pub,
        obstacle
    )

    print(
        "远处障碍物已加入 Planning Scene",
        flush=True
    )

    time.sleep(2.0)

    # ============================================================
    # 5. 设置目标关节状态
    #
    # HOME：
    # joint1 = 0
    #
    # Goal：
    # joint1 = 1.20 rad ≈ 68.8°
    #
    # 其他关节保持 0。
    #
    # 这会让整条机械臂绕 Z 轴进行一次明显扫掠。
    # ============================================================

    robot_model = moveit.get_robot_model()

    goal_state = RobotState(
        robot_model
    )

    goal_state.joint_positions = {
        "joint1": 1.20,
        "joint2": 0.00,
        "joint3": 0.00,
        "joint4": 0.00,
        "joint5": 0.00,
        "joint6": 0.00,
    }

    print(
        "目标：joint1 = 1.20 rad，其余关节 = 0",
        flush=True
    )

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=goal_state
    )

    # ============================================================
    # 6. 实验 A：无障碍规划
    # ============================================================

    print(
        "开始实验 A 规划...",
        flush=True
    )

    baseline_plan = arm.plan()

    if not baseline_plan:

        print(
            "实验 A 失败："
            "目标状态或基础规划存在问题。",
            flush=True
        )

        os._exit(1)

    print(
        "实验 A：规划成功 ✅",
        flush=True
    )

    print(
        "说明 HOME → Goal 本身合法。",
        flush=True
    )

    print(
        "请观察 RViz 中的基准轨迹。",
        flush=True
    )

    time.sleep(4.0)

    # ============================================================
    # 7. 实验 B：
    #    只移动障碍物。
    #
    # Start 不变
    # Goal 不变
    # Planner 不变
    #
    # 将障碍物移动到机械臂 joint1
    # 从 0 → 1.2 rad 时的扫掠区域。
    # ============================================================

    print(
        "\n========== 实验 B：加入路径障碍 ==========",
        flush=True
    )

    obstacle.primitive_poses[0].position.x = 0.50
    obstacle.primitive_poses[0].position.y = 0.30
    obstacle.primitive_poses[0].position.z = 0.55

    print(
        "障碍物移动到：",
        flush=True
    )

    print(
        "x = 0.50",
        flush=True
    )

    print(
        "y = 0.30",
        flush=True
    )

    print(
        "z = 0.55",
        flush=True
    )

    publish_obstacle(
        scene_node,
        collision_pub,
        obstacle
    )

    print(
        "路径障碍物已更新",
        flush=True
    )

    # 给 Planning Scene 时间同步
    time.sleep(2.0)

    # ============================================================
    # 8. 同一个 Start + Goal 再规划一次
    # ============================================================

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=goal_state
    )

    print(
        "开始实验 B 避障规划...",
        flush=True
    )

    avoidance_plan = arm.plan()

    if not avoidance_plan:

        print(
            "实验 B 未找到无碰撞路径。",
            flush=True
        )

        print(
            "说明障碍物确实影响了运动，"
            "但当前位置可能阻挡得过强。",
            flush=True
        )

        os._exit(1)

    print(
        "实验 B：避障规划成功 ✅",
        flush=True
    )

    print(
        "Start、Goal 与实验 A 完全相同。",
        flush=True
    )

    print(
        "唯一变化是障碍物进入了扫掠区域。",
        flush=True
    )

    print(
        "请观察 RViz："
        "机械臂应改变关节运动方式绕开绿色障碍物。",
        flush=True
    )

    # 留时间观察规划轨迹
    time.sleep(5.0)

    # ============================================================
    # 9. 执行避障轨迹
    # ============================================================

    print(
        "开始执行实验 B 的避障轨迹...",
        flush=True
    )

    moveit.execute(
        avoidance_plan.trajectory,
        controllers=[]
    )

    print(
        "避障轨迹执行完成 ✅",
        flush=True
    )

    time.sleep(3.0)

    # Jazzy MoveItPy 析构 workaround
    os._exit(0)


if __name__ == "__main__":
    main()