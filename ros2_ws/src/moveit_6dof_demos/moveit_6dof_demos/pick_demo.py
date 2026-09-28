import os
import time

import rclpy
from rclpy.action import ActionClient

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from geometry_msgs.msg import Pose, PoseStamped

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState

from moveit_msgs.msg import (
    AttachedCollisionObject,
    CollisionObject,
)

from shape_msgs.msg import SolidPrimitive


# ============================================================
# 夹爪控制函数
# ============================================================

def move_gripper(
    node,
    action_client,
    positions,
    name,
):
    """
    使用已经创建好的 gripper ActionClient，
    控制左右两个夹爪关节。

    注意：
    这里不再创建新的 ActionClient。
    OPEN / CLOSED / 后续 Place-OPEN
    都复用 main() 中创建的同一个 ActionClient。
    """

    print(
        f"等待 gripper_controller：{name}...",
        flush=True,
    )

    if not action_client.wait_for_server(
        timeout_sec=5.0
    ):
        print(
            "gripper_controller 不可用 ❌",
            flush=True,
        )
        return False

    goal = FollowJointTrajectory.Goal()

    goal.trajectory.joint_names = [
        "left_finger_joint",
        "right_finger_joint",
    ]

    point = JointTrajectoryPoint()

    point.positions = positions
    point.time_from_start.sec = 1

    goal.trajectory.points = [
        point,
    ]

    print(
        f"开始执行夹爪动作：{name}",
        flush=True,
    )

    goal_future = action_client.send_goal_async(
        goal
    )

    rclpy.spin_until_future_complete(
        node,
        goal_future,
    )

    goal_handle = goal_future.result()

    if goal_handle is None:
        print(
            f"夹爪 Action 未返回 GoalHandle：{name} ❌",
            flush=True,
        )
        return False

    if not goal_handle.accepted:
        print(
            f"夹爪目标被拒绝：{name} ❌",
            flush=True,
        )
        return False

    result_future = (
        goal_handle.get_result_async()
    )

    rclpy.spin_until_future_complete(
        node,
        result_future,
    )

    result_wrapper = result_future.result()

    if result_wrapper is None:
        print(
            f"夹爪 Action 未返回结果：{name} ❌",
            flush=True,
        )
        return False

    result = result_wrapper.result

    if result.error_code != 0:
        print(
            f"夹爪动作失败：{name}，"
            f"error_code={result.error_code}",
            flush=True,
        )
        return False

    print(
        f"夹爪动作完成：{name} ✅",
        flush=True,
    )

    return True


# ============================================================
# 主程序
# ============================================================

def main():

    rclpy.init()

    print(
        "正在启动 MoveItPy...",
        flush=True,
    )

    # ========================================================
    # 1. 初始化 MoveIt
    # ========================================================

    moveit = MoveItPy(
        node_name="moveit_6dof_planning_scene_demo"
    )

    robot_model = moveit.get_robot_model()

    arm = moveit.get_planning_component(
        "arm"
    )

    print(
        "MoveItPy 启动成功",
        flush=True,
    )

    # ========================================================
    # 2. 创建辅助 ROS2 Node
    # ========================================================

    scene_node = rclpy.create_node(
        "planning_scene_publisher"
    )

    # ========================================================
    # 3. 只创建一次 Gripper ActionClient
    #
    # 整个 Pick / Place 生命周期都复用它。
    # ========================================================

    gripper_action_client = ActionClient(
        scene_node,
        FollowJointTrajectory,
        "/gripper_controller/follow_joint_trajectory",
    )

    # ========================================================
    # 4. 创建 Publisher
    # ========================================================

    pregrasp_pose_pub = (
        scene_node.create_publisher(
            PoseStamped,
            "/pregrasp_pose",
            10,
        )
    )

    collision_pub = (
        scene_node.create_publisher(
            CollisionObject,
            "/collision_object",
            10,
        )
    )

    attached_collision_pub = (
        scene_node.create_publisher(
            AttachedCollisionObject,
            "/attached_collision_object",
            10,
        )
    )

    print(
        "等待 MoveIt 订阅 Planning Scene topics ...",
        flush=True,
    )

    start_time = time.time()

    while (
        collision_pub.get_subscription_count() == 0
        or
        attached_collision_pub.get_subscription_count()
        == 0
    ):

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1,
        )

        if time.time() - start_time > 5.0:

            print(
                "等待 Planning Scene topics 订阅超时",
                flush=True,
            )

            os._exit(1)

    print(
        f"/collision_object 订阅者数量: "
        f"{collision_pub.get_subscription_count()}",
        flush=True,
    )

    print(
        f"/attached_collision_object 订阅者数量: "
        f"{attached_collision_pub.get_subscription_count()}",
        flush=True,
    )

    # ========================================================
    # 5. 创建工作台
    # ========================================================

    table = CollisionObject()

    table.header.frame_id = "base_link"
    table.id = "table"

    table_shape = SolidPrimitive()

    table_shape.type = SolidPrimitive.BOX

    table_shape.dimensions = [
        0.60,
        0.80,
        0.05,
    ]

    table_pose = Pose()

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

    # ========================================================
    # 6. 发布工作台
    # ========================================================

    print(
        "正在将 table 加入 Planning Scene...",
        flush=True,
    )

    for _ in range(5):

        table.header.stamp = (
            scene_node
            .get_clock()
            .now()
            .to_msg()
        )

        collision_pub.publish(
            table
        )

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1,
        )

        time.sleep(0.2)

    print(
        "table 已发布到 Planning Scene ✅",
        flush=True,
    )

    # ========================================================
    # 7. 创建待抓取物体
    # ========================================================

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

    # table 中心高度 = 0.20
    # table 高度       = 0.05
    #
    # table 顶面：
    #
    # 0.20 + 0.05 / 2
    # = 0.225
    #
    # object 高度 = 0.10
    #
    # object 中心：
    #
    # 0.225 + 0.10 / 2
    # = 0.275

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

    # ========================================================
    # 8. 发布待抓取物体
    # ========================================================

    print(
        "正在将 pick_object 加入 Planning Scene...",
        flush=True,
    )

    collision_pub.publish(
        pick_object
    )

    rclpy.spin_once(
        scene_node,
        timeout_sec=0.2,
    )

    time.sleep(0.5)

    print(
        "pick_object 已发布到 Planning Scene ✅",
        flush=True,
    )

    # ========================================================
    # 9. 创建 Pre-grasp Pose
    #
    # 当前主要用于 RViz 显示。
    # 实际规划使用 Joint Goal。
    # ========================================================

    pregrasp_pose = PoseStamped()

    pregrasp_pose.header.frame_id = (
        "base_link"
    )

    pregrasp_pose.pose.position.x = 0.45
    pregrasp_pose.pose.position.y = 0.00
    pregrasp_pose.pose.position.z = 0.60

    pregrasp_pose.pose.orientation.x = 0.0
    pregrasp_pose.pose.orientation.y = 0.7071
    pregrasp_pose.pose.orientation.z = 0.0
    pregrasp_pose.pose.orientation.w = 0.7071

    print(
        "正在发布 Pre-grasp Pose 供 RViz 显示...",
        flush=True,
    )

    for _ in range(5):

        pregrasp_pose.header.stamp = (
            scene_node
            .get_clock()
            .now()
            .to_msg()
        )

        pregrasp_pose_pub.publish(
            pregrasp_pose
        )

        rclpy.spin_once(
            scene_node,
            timeout_sec=0.1,
        )

        time.sleep(0.2)

    # ========================================================
    # 10. OPEN
    #
    # 使用 main() 创建的唯一 ActionClient。
    # ========================================================

    if not move_gripper(
        scene_node,
        gripper_action_client,
        [0.04, 0.04],
        "OPEN",
    ):

        print(
            "夹爪 OPEN 失败，停止 Pick ❌",
            flush=True,
        )

        os._exit(1)

    time.sleep(0.5)

    # ========================================================
    # 11. Pre-grasp Joint Goal
    # ========================================================

    pregrasp_joint_state = RobotState(
        robot_model
    )

    pregrasp_joint_state.joint_positions = {
        "joint1": 0.0,
        "joint2": -1.2331146600407434,
        "joint3": 1.787024702765567,
        "joint4": 0.0,
        "joint5": 1.0168862086418036,
        "joint6": 0.0,
    }

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=pregrasp_joint_state
    )

    print(
        "开始规划 Pre-grasp Joint Goal...",
        flush=True,
    )

    pregrasp_plan = arm.plan()

    if not pregrasp_plan:

        print(
            "Pre-grasp Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Pre-grasp Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    pregrasp_execution_status = (
        moveit.execute(
            pregrasp_plan.trajectory,
            controllers=[],
        )
    )

    print(
        f"Pre-grasp 执行状态："
        f"{pregrasp_execution_status.status}",
        flush=True,
    )

    if (
        pregrasp_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Pre-grasp 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Pre-grasp 执行成功 ✅",
        flush=True,
    )

    time.sleep(1.0)

    # ========================================================
    # 12. Grasp Joint Goal
    # ========================================================

    grasp_joint_state = RobotState(
        robot_model
    )

    grasp_joint_state.joint_positions = {
        "joint1": 0.0,
        "joint2": -1.1670343358001434,
        "joint3": 2.002495044675828,
        "joint4": 0.0,
        "joint5": 0.7353355424909426,
        "joint6": 0.0,
    }

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=grasp_joint_state
    )

    print(
        "开始规划 Grasp Joint Goal...",
        flush=True,
    )

    grasp_plan = arm.plan()

    if not grasp_plan:

        print(
            "Grasp Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Grasp Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    grasp_execution_status = (
        moveit.execute(
            grasp_plan.trajectory,
            controllers=[],
        )
    )

    print(
        f"Grasp 执行状态："
        f"{grasp_execution_status.status}",
        flush=True,
    )

    if (
        grasp_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Grasp 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Grasp 执行成功 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 13. CLOSED
    #
    # 仍然复用同一个 gripper_action_client。
    # 不再创建第二个 ActionClient。
    # ========================================================

    if not move_gripper(
        scene_node,
        gripper_action_client,
        [0.0, 0.0],
        "CLOSED",
    ):

        print(
            "夹爪 CLOSED 失败，停止 Pick ❌",
            flush=True,
        )

        os._exit(1)

    time.sleep(0.5)

    print(
        "物体抓取位置夹爪已关闭 ✅",
        flush=True,
    )

    # ========================================================
    # 14. 创建 AttachedCollisionObject
    # ========================================================

    attached_object = (
        AttachedCollisionObject()
    )

    attached_object.link_name = (
        "gripper_base"
    )

    attached_object.object.id = (
        "pick_object"
    )

    attached_object.object.operation = (
        CollisionObject.ADD
    )

    # 抓住以后，允许 pick_object 与左右手指接触。
    #
    # 否则 MoveIt 会把正常的抓取接触
    # 当成碰撞。

    attached_object.touch_links = [
        "left_finger",
        "right_finger",
    ]

    # ========================================================
    # 15. Attach
    # ========================================================

    print(
        "正在将 pick_object attach 到 gripper_base...",
        flush=True,
    )

    attached_collision_pub.publish(
        attached_object
    )

    rclpy.spin_once(
        scene_node,
        timeout_sec=0.2,
    )

    time.sleep(0.5)

    print(
        "pick_object attach 消息已发布 ✅",
        flush=True,
    )

    # 给 Planning Scene 一点时间同步
    time.sleep(0.5)

    # ========================================================
    # 16. Lift
    #
    # Grasp：
    # tool z ≈ 0.50
    #
    # Lift：
    # 回到已经验证过的 Pre-grasp 状态，
    # tool z ≈ 0.60
    #
    # 此时 pick_object 已经 Attached，
    # 所以规划时 MoveIt 会把物体一起参与碰撞检测。
    # ========================================================

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=pregrasp_joint_state
    )

    print(
        "开始规划 Lift Joint Goal...",
        flush=True,
    )

    lift_plan = arm.plan()

    if not lift_plan:

        print(
            "Lift Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Lift Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    lift_execution_status = (
        moveit.execute(
            lift_plan.trajectory,
            controllers=[],
        )
    )

    print(
        f"Lift 执行状态："
        f"{lift_execution_status.status}",
        flush=True,
    )

    if (
        lift_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Lift 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Lift 执行成功 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 17. Pre-place
    #
    # 携带 pick_object 从 Pick 上方
    # 横向移动到 Place 上方。
    #
    # 目标：
    # x = 0.45
    # y = 0.20
    # z = 0.60
    # ========================================================

    preplace_joint_state = RobotState(
        robot_model
    )

    preplace_joint_state.joint_positions = {
        "joint1": 0.4182243279696196,
        "joint2": -1.1047595287565142,
        "joint3": 1.6062046631007914,
        "joint4": -3.58507747285469e-08,
        "joint5": 1.0693511161377374,
        "joint6": 0.4182243450892588,
    }

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=preplace_joint_state
    )

    print(
        "开始规划 Pre-place Joint Goal...",
        flush=True,
    )

    preplace_plan = arm.plan()

    if not preplace_plan:

        print(
            "Pre-place Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Pre-place Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    preplace_execution_status = moveit.execute(
        preplace_plan.trajectory,
        controllers=[],
    )

    print(
        f"Pre-place 执行状态："
        f"{preplace_execution_status.status}",
        flush=True,
    )

    if (
        preplace_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Pre-place 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Pre-place 执行成功 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 18. Place
    #
    # 从目标位置上方下降到放置高度。
    #
    # x = 0.45
    # y = 0.20
    # z = 0.50
    #
    # 此时 pick_object 仍然 Attached。
    # ========================================================

    place_joint_state = RobotState(
        robot_model
    )

    place_joint_state.joint_positions = {
        "joint1": 0.4182212534967785,
        "joint2": -1.0519938354622829,
        "joint3": 1.8307318555930925,
        "joint4": -7.4626154467575395e-06,
        "joint5": 0.7920578924099992,
        "joint6": 0.41823097807435416,
    }

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=place_joint_state
    )

    print(
        "开始规划 Place Joint Goal...",
        flush=True,
    )

    place_plan = arm.plan()

    if not place_plan:

        print(
            "Place Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Place Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    place_execution_status = moveit.execute(
        place_plan.trajectory,
        controllers=[],
    )

    print(
        f"Place 执行状态："
        f"{place_execution_status.status}",
        flush=True,
    )

    if (
        place_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Place 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Place 执行成功 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 19. OPEN
    #
    # 到达放置位置后打开夹爪。
    #
    # 注意：
    # 此时 pick_object 在 Planning Scene 中
    # 仍然还是 Attached。
    # 下一步才进行 Detach。
    # ========================================================

    if not move_gripper(
        scene_node,
        gripper_action_client,
        [0.04, 0.04],
        "PLACE OPEN",
    ):

        print(
            "Place OPEN 失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "放置位置夹爪已打开 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 20. Detach
    #
    # 把 pick_object 从机器人重新交还给 World。
    # ========================================================

    detach_object = AttachedCollisionObject()

    detach_object.link_name = (
        "gripper_base"
    )

    detach_object.object.id = (
        "pick_object"
    )

    detach_object.object.operation = (
        CollisionObject.REMOVE
    )

    print(
        "正在将 pick_object 从 gripper_base detach...",
        flush=True,
    )

    attached_collision_pub.publish(
        detach_object
    )

    rclpy.spin_once(
        scene_node,
        timeout_sec=0.2,
    )

    time.sleep(0.5)

    print(
        "pick_object detach 消息已发布 ✅",
        flush=True,
    )

    time.sleep(0.5)

    # ========================================================
    # 21. Retreat
    #
    # 物体已经留在桌面。
    # 机械臂重新回到 Pre-place 高度。
    # ========================================================

    arm.set_start_state_to_current_state()

    arm.set_goal_state(
        robot_state=preplace_joint_state
    )

    print(
        "开始规划 Retreat Joint Goal...",
        flush=True,
    )

    retreat_plan = arm.plan()

    if not retreat_plan:

        print(
            "Retreat Joint Goal 规划失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Retreat Joint Goal 规划成功，开始执行...",
        flush=True,
    )

    retreat_execution_status = moveit.execute(
        retreat_plan.trajectory,
        controllers=[],
    )

    print(
        f"Retreat 执行状态："
        f"{retreat_execution_status.status}",
        flush=True,
    )

    if (
        retreat_execution_status.status
        != "SUCCEEDED"
    ):

        print(
            "Retreat 执行失败 ❌",
            flush=True,
        )

        os._exit(1)

    print(
        "Retreat 执行成功 ✅",
        flush=True,
    )

    # ========================================================
    # Pick & Place 完成
    #
    # OPEN
    # → Pre-grasp
    # → Grasp
    # → CLOSED
    # → Attach
    # → Lift
    # → Pre-place
    # → Place
    # → OPEN
    # → Detach
    # → Retreat
    # ========================================================

    print(
        "完整 Pick & Place 执行成功 ✅",
        flush=True,
    )

    os._exit(0)