import os
import time

import rclpy

from geometry_msgs.msg import Pose
from moveit.planning import MoveItPy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive


def main():

    rclpy.init()

    print("正在启动 MoveItPy...", flush=True)

    # ============================================================
    # 1. 初始化 MoveIt
    # ============================================================

    moveit = MoveItPy(
        node_name="moveit_6dof_planning_scene_demo"
    )

    # 主动访问一次 RobotModel：
    # 一方面确认 MoveItPy 已正常初始化，
    # 另一方面保持 moveit 对象在整个 main() 生命周期内有效。
    moveit.get_robot_model()

    print("MoveItPy 启动成功", flush=True)

    # ============================================================
    # 2. 创建 Planning Scene Publisher
    # ============================================================

    scene_node = rclpy.create_node(
        "planning_scene_publisher"
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
        f"/collision_object 订阅者数量: "
        f"{collision_pub.get_subscription_count()}",
        flush=True
    )

    # ============================================================
    # 3. 创建工作台 CollisionObject
    # ============================================================

    table = CollisionObject()

    # table 的位姿相对于 base_link 描述
    table.header.frame_id = "base_link"

    # Planning Scene 中的唯一 ID
    table.id = "table"

    table_shape = SolidPrimitive()
    table_shape.type = SolidPrimitive.BOX

    # BOX 尺寸顺序：
    # X 长度 / Y 宽度 / Z 高度
    table_shape.dimensions = [
        0.60,
        0.80,
        0.05,
    ]

    table_pose = Pose()

    # BOX 的 Pose 表示盒子中心
    table_pose.position.x = 0.45
    table_pose.position.y = 0.00
    table_pose.position.z = 0.20

    table_pose.orientation.x = 0.0
    table_pose.orientation.y = 0.0
    table_pose.orientation.z = 0.0
    table_pose.orientation.w = 1.0

    table.primitives.append(
        table_shape
    )

    table.primitive_poses.append(
        table_pose
    )

    table.operation = CollisionObject.ADD

    # ============================================================
    # 4. 将工作台发布到 Planning Scene
    # ============================================================

    print(
        "正在将 table 加入 Planning Scene...",
        flush=True
    )

    for _ in range(5):

        table.header.stamp = (
            scene_node.get_clock().now().to_msg()
        )

        collision_pub.publish(
            table
        )

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1
        )

        time.sleep(0.2)

    print(
        "table 已发布到 Planning Scene ✅",
        flush=True
    )

    # ============================================================
    # 5. 创建待抓取物体
    # ============================================================

    pick_object = CollisionObject()

    pick_object.header.frame_id = "base_link"
    pick_object.id = "pick_object"

    object_shape = SolidPrimitive()
    object_shape.type = SolidPrimitive.BOX

    object_shape.dimensions = [
        0.05,
        0.05,
        0.10,
    ]

    object_pose = Pose()

    object_pose.position.x = 0.45
    object_pose.position.y = 0.00

    # table 顶面高度：
    # 0.20 + 0.05 / 2 = 0.225
    #
    # object 高度为 0.10，
    # 所以 object 中心高度：
    # 0.225 + 0.10 / 2 = 0.275
    object_pose.position.z = 0.275

    object_pose.orientation.x = 0.0
    object_pose.orientation.y = 0.0
    object_pose.orientation.z = 0.0
    object_pose.orientation.w = 1.0

    pick_object.primitives.append(
        object_shape
    )

    pick_object.primitive_poses.append(
        object_pose
    )

    pick_object.operation = CollisionObject.ADD

    # ============================================================
    # 6. 将待抓取物体发布到 Planning Scene
    # ============================================================

    print(
        "正在将 pick_object 加入 Planning Scene...",
        flush=True
    )

    for _ in range(5):

        pick_object.header.stamp = (
            scene_node.get_clock().now().to_msg()
        )

        collision_pub.publish(
            pick_object
        )

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1
        )

        time.sleep(0.2)

    print(
        "pick_object 已发布到 Planning Scene ✅",
        flush=True
    )

    # Jazzy MoveItPy 析构 workaround
    os._exit(0)
    