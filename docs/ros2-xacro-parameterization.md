# ROS2 Xacro Parameterization Notes

## 1. Xacro 是什么

Xacro 可以理解为：

带变量、表达式、模板和文件复用能力的 URDF。

流程：

Xacro
↓
展开 property / macro / include / arg
↓
生成标准 URDF
↓
robot_state_publisher
↓
TF
↓
RViz


## 2. property

property 用于定义内部变量。

例如：

<xacro:property name="link1_length" value="0.5"/>

后面可以使用：

${link1_length}

也可以参与运算：

${link1_length / 2.0}


## 3. Macro

Macro 可以理解为：

可复用的 XML 模板函数。

例如：

box_link()

用于生成一套标准 Link 结构。

revolute_joint()

用于生成旋转 Joint。

基本思想：

定义一次模板
↓
以后传不同参数
↓
重复生成不同 Link / Joint


## 4. Macro 参数

例如：

<xacro:macro
  name="box_link"
  params="name size_x size_y size_z origin_xyz color">

这些 params 类似函数形参。

调用时：

<xacro:box_link
  name="link1"
  size_x="..."
  ...
/>

相当于向宏传参。


## 5. Include

可以把 Macro 拆到单独文件。

当前结构：

urdf/
├── simple_arm.urdf.xacro
├── common_macros.xacro
└── simple_arm.urdf

主文件通过：

<xacro:include
  filename="$(find robot_description)/urdf/common_macros.xacro"
/>

引入公共宏。

include 可以理解为：

把其他 Xacro 文件中的模板引入当前文件。


## 6. arg

xacro:arg 用于接收外部参数。

例如：

<xacro:arg
  name="link2_length"
  default="0.4"
/>

表示：

如果外部没有传参数，
link2_length 默认使用 0.4m。

命令行可以覆盖：

xacro simple_arm.urdf.xacro link2_length:=0.7


## 7. arg 和 property 的区别

arg：

主要负责从外部接收参数。

property：

主要负责 Xacro 文件内部保存和计算参数。

当前使用方式：

xacro:arg
↓
property
↓
macro
↓
生成 URDF


## 8. 参数化机器人

以前普通 URDF 中可能直接写：

0.4

0.2

0.4

这些数字之间其实存在几何关系。

使用 Xacro 后：

link2_length = 0.4

则可以自动得到：

link2 几何长度
= link2_length

visual 中心
= link2_length / 2

tool_link 位置
= link2_length

因此只修改一个参数，
相关结构都会自动更新。


## 9. Launch 与 Xacro

Launch 可以声明外部参数：

DeclareLaunchArgument(
    'link2_length',
    default_value='0.4'
)

然后：

LaunchConfiguration

读取参数。

再通过：

Command

调用 Xacro。

完整链路：

命令行
↓
LaunchArgument
↓
LaunchConfiguration
↓
Xacro arg
↓
property
↓
macro
↓
URDF
↓
robot_state_publisher
↓
TF
↓
RViz


## 10. 外部切换机器人尺寸

默认：

ros2 launch robot_description display.launch.py

使用：

link2_length = 0.4m

外部覆盖：

ros2 launch robot_description display.launch.py \
  link2_length:=0.7

无需修改机器人模型源文件，
即可生成不同尺寸的机器人。


## 11. Xacro 和 URDF 的关系

robot_state_publisher 并不直接理解：

property

macro

include

xacro:arg

这些是 Xacro 的语法。

Xacro 会先把它们展开成标准 URDF。

然后 robot_state_publisher 再读取最终的：

link

joint

origin

axis

limit


## Day 9 核心总结

property
= 内部变量

${...}
= 表达式

macro
= 可复用 XML 模板函数

params
= 宏参数

include
= 拆文件并引入其他 Xacro

arg
= 从外部接收参数

LaunchArgument
= 从 ros2 launch 命令接收参数

Xacro
= 参数化生成 URDF