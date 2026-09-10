# ROS2 Collision and Inertial Notes

## 1. Link 中的三类核心信息

一个 Link 可以同时包含：

- visual
- collision
- inertial

可以理解为：

Link
├── visual
├── collision
└── inertial


## 2. Visual

Visual 用于描述机器人外观。

主要给：

RViz

等可视化工具使用。

Visual 可以使用：

- box
- cylinder
- sphere
- mesh


## 3. Collision

Collision 用于描述碰撞检测时机器人占据的空间。

主要给：

- MoveIt2
- 碰撞检测算法
- 规划器

使用。

Visual 和 Collision 不一定相同。

例如：

Visual：
使用精细 CAD Mesh

Collision：
使用简化 Box / Cylinder

这样可以提高碰撞检测效率。


## 4. Inertial

Inertial 描述 Link 的物理属性。

主要包括：

origin

mass

inertia


## 5. Inertial Origin

Inertial 中的 origin 表示：

质心位置以及惯性参考坐标系。

当前教学模型中：

质心
=
几何中心


## 6. Mass

mass 表示质量。

单位：

kg

例如：

base_link = 5 kg

link1 = 2 kg

link2 = 1 kg

Mass 主要影响平移运动中的动力学。


## 7. Inertia

Inertia 表示转动惯量。

单位：

kg·m²

它描述物体绕不同轴旋转时：

有多难改变旋转状态。

主要包括：

Ixx

Iyy

Izz

以及：

Ixy

Ixz

Iyz


## 8. 长方体惯性

对于尺寸：

x = a

y = b

z = c

质量：

m

绕质心的惯量：

Ixx = m / 12 × (b² + c²)

Iyy = m / 12 × (a² + c²)

Izz = m / 12 × (a² + b²)


## 9. 为什么长轴方向惯量较小

例如 link1 沿 Z 方向较长。

它绕 Z 轴旋转时：

大部分质量距离 Z 轴较近。

因此：

Izz 较小。

而绕 X / Y 轴旋转时：

大量质量距离旋转轴较远。

因此：

Ixx 和 Iyy 较大。

核心规律：

质量离旋转轴越远，

转动惯量通常越大。


## 10. 交叉惯量项

当前模型中：

Ixy = 0

Ixz = 0

Iyz = 0

原因是：

- 模型是规则长方体
- 质心位于几何中心
- 坐标轴和物体主轴对齐

因此惯性矩阵可以近似看成：

[ Ixx   0    0  ]
[  0   Iyy   0  ]
[  0    0   Izz ]


## 11. Visual 和 Collision 的区别

Visual：

描述“看起来是什么样”。

Collision：

描述“碰撞时认为它占据什么空间”。

因此：

Visual != Collision

两者可以相同，也可以不同。


## 12. Kinematics

Kinematics：

运动学。

主要研究：

- 关节角
- 位置
- 姿态
- 坐标变换
- Forward Kinematics
- Inverse Kinematics

它不关心需要多大的力。


## 13. Dynamics

Dynamics：

动力学。

主要研究：

- mass
- inertia
- force
- torque
- gravity
- acceleration

它关心：

为什么这样运动，

以及需要多大的力或力矩。


## 14. 为什么没有 Inertial 也能运行 RViz

RViz 和 robot_state_publisher 主要使用运动学信息。

流程：

URDF
+
Joint State
↓
robot_state_publisher
↓
TF
↓
RViz

只要机器人结构和关节状态存在，

就可以计算 Link 的位置和姿态。

因此没有 inertial，

RViz 和 TF 仍然可以正常工作。


## 15. Xacro Macro 的作用

当前 box_link 宏一次生成：

Link
├── visual
├── collision
└── inertial

只需要传入：

- 名称
- 尺寸
- 位置
- 颜色
- mass

Xacro 会自动计算惯性。

因此：

修改一次 Macro

可以同时升级：

base_link

link1

link2


## Day 10 核心总结

Visual
= 外观模型

Collision
= 碰撞检测模型

Inertial
= 物理属性

Mass
= 质量

Inertia
= 转动惯量

Kinematics
= 怎么动、动到哪里

Dynamics
= 需要多大的力、为什么这样动