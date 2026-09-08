# ROS2 URDF and RViz Notes

## 1. URDF 是什么

URDF：

Unified Robot Description Format

用于描述机器人的结构，包括：

- Link
- Joint
- Visual
- Collision
- Inertial

当前 Day 8 主要关注：

Link + Joint + Visual


## 2. Link

Link 表示机器人中的刚性部件。

例如：

base_link

link1

link2

tool_link

可以理解为机器人的底座、连杆、末端等刚体。


## 3. Joint

Joint 用于连接两个 Link。

一个 Joint 通常包含：

parent

child

origin

axis

limit

例如：

base_link
↓
joint1
↓
link1


## 4. Joint Origin

例如：

<origin xyz="0 0 0.1" rpy="0 0 0"/>

表示子 Link 坐标系相对于父 Link 坐标系的位置和姿态。

Joint 的 origin 决定：

“子坐标系在哪里”。


## 5. Visual Origin

Visual 中也可以有 origin：

<visual>
  <origin xyz="0 0 0.25" rpy="0 0 0"/>
</visual>

它表示：

几何模型相对于当前 Link 坐标系的位置。

因此：

Joint origin

和

Visual origin

不是同一个概念。


## 6. Joint Type

fixed：

固定关节，不允许运动。

revolute：

旋转关节，有角度范围。

当前模型中：

joint1

joint2

都使用 revolute。


## 7. Joint Axis

例如：

<axis xyz="0 1 0"/>

表示关节绕 Y 轴旋转。

因此当前机械臂主要在 X-Z 平面运动。


## 8. Joint Limit

例如：

<limit
  lower="-1.57"
  upper="1.57"
  effort="10.0"
  velocity="1.0"
/>

其中：

lower / upper

控制关节角度范围。

-1.57 到 +1.57 rad

大约对应：

-90° 到 +90°


## 9. robot_state_publisher

robot_state_publisher 读取：

URDF

+

/joint_states

然后计算机器人各个 Link 之间的 TF。

基本流程：

URDF
+
Joint States
↓
robot_state_publisher
↓
TF Tree


## 10. joint_state_publisher_gui

joint_state_publisher_gui 提供滑块。

通过调整：

joint1

joint2

可以改变关节角度。

它发布：

/joint_states

robot_state_publisher 再根据这些关节状态计算 TF。


## 11. RViz

RViz 用于可视化机器人。

当前显示：

RobotModel

TF

Fixed Frame 设置为：

base_link

RViz 本身主要负责显示。

关节角度通过：

joint_state_publisher_gui

进行修改。


## 12. Kinematic Chain

当前机械臂结构：

base_link
↓
joint1
↓
link1
↓
joint2
↓
link2
↓
tool_joint
↓
tool_link

父关节运动会影响后面的所有子 Link。

例如：

joint1 运动

会影响：

link1
joint2
link2
tool_link

而 joint2 运动不会反过来影响 link1。


## 13. Forward Kinematics

FK：

Forward Kinematics

表示：

已知关节角

计算机械臂末端的位置和姿态。

例如：

joint1 = q1

joint2 = q2

↓

FK

↓

tool_link：

x
y
z
orientation


当前模型零位时：

joint1 = 0

joint2 = 0

得到：

tool_link ≈

(0.4, 0.0, 0.6)


该结果与：

tf2_echo base_link tool_link

输出一致。


## 14. FK 与 TF2

TF2 可以把机器人运动链中的 Transform 自动组合：

base_link → link1

×

link1 → link2

×

link2 → tool_link

=

base_link → tool_link

因此：

URDF 定义机器人结构

Joint State 提供关节角

robot_state_publisher 计算每段 TF

TF2 组合完整坐标链


## 15. RViz Config

RViz 配置保存在：

rviz/simple_arm.rviz

其中保存：

Fixed Frame = base_link

RobotModel

TF

因此以后启动 RViz 时可以自动加载这些配置。


## 16. Launch

display.launch.py 一次启动：

robot_state_publisher

joint_state_publisher_gui

rviz2

并自动加载：

simple_arm.urdf

simple_arm.rviz

最终可以通过：

ros2 launch robot_description display.launch.py

一条命令启动整个机器人可视化系统。


## Day 8 核心总结

URDF
= 描述机器人结构

Link
= 刚性部件

Joint
= Link 之间的连接和运动关系

Joint State
= 当前关节角度

robot_state_publisher
= URDF + Joint State → TF

TF2
= 管理和组合坐标变换

RViz
= 可视化机器人和 TF

FK
= 关节角 → 末端位姿