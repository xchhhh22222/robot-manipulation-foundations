# ROS2 Topic Communication Notes

## Node 是什么

Node 是 ROS2 中实际运行的“节点程序”。

一个 Node 可以拥有 Publisher、Subscriber、Timer、Service 等功能。

例如：

robot_status_publisher

就是一个 ROS2 Node，它负责发布机器人状态。


## Topic 是什么

Topic 是 ROS2 中用于消息通信的“频道名”或“逻辑管道”。

例如：

/robot_status

表示机器人状态通信使用的 Topic。

Topic 本身不是 Node，也不是一个独立运行的中转程序。


## Message 是什么

Message 是 Node 之间实际传输的数据。

例如：

std_msgs/msg/String

是消息类型。

其中：

IDLE
MOVING
GRASPING

是实际发送的消息内容。


## Publisher / Subscriber 如何通信

Publisher 负责发布消息。

Subscriber 负责接收消息。

二者通过相同的 Topic 建立通信。

例如：

robot_status_publisher
        ↓
   /robot_status
        ↓
robot_status_monitor


## Timer / Callback 如何工作

Timer 用来规定“什么时候执行某个函数”。

例如：

self.create_timer(
    1.0,
    self.timer_callback
)

表示：

每隔 1 秒调用一次 timer_callback()。

Callback 是事件发生后由 ROS2 自动调用的函数。

Publisher 中：

Timer 到时间
→ 调用 timer_callback()
→ 发布消息

Subscriber 中：

收到消息
→ 自动调用 status_callback(msg)

注意：

create_publisher(..., 10)

和：

create_subscription(..., 10)

里面的 10 才是 QoS 队列深度。

它不是 Timer。


## setup.py 为什么需要

setup.py 用于描述 Python ROS2 Package 如何安装。

其中 entry_points 可以告诉 ROS2：

某个 ros2 run 命令应该执行哪个 Python 模块中的哪个函数。

例如：

robot_status_publisher =
robot_status_demo.robot_status_publisher:main

表示：

运行 robot_status_publisher
→ 找到 robot_status_publisher.py
→ 调用其中的 main()。


## colcon build 的作用

colcon build 用来构建 ROS2 Workspace。

它会读取 src/ 中的 Package，并产生：

build/
install/
log/

其中：

src/
是我们真正编写的源码。

build/
是构建过程中产生的中间文件。

install/
是构建完成后的安装结果，ROS2 从这里发现我们自己的 Package。


## source 的作用

source install/setup.bash

不是“更新全局文件”。

它的作用是：

把当前 Workspace 的环境信息加载到“当前终端”。

这样当前终端才能找到：

robot_status_demo

以及我们注册的 executable。

因此新开一个 Terminal 后，通常需要重新 source。


## FSM 为什么要验证状态转换

FSM 用来规定机器人允许怎样从一个状态进入另一个状态。

例如：

IDLE → MOVING → GRASPING → IDLE

是合法流程。

而：

IDLE → GRASPING

可以被规定为非法流程。

验证状态转换可以防止机器人收到错误状态后直接执行不合理或危险的动作。

非法状态应该：

检测
→ 警告
→ 拒绝更新 current_status
→ 不执行对应动作