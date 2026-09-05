# ROS2 Action Communication Notes

## Action 是什么

Action 是 ROS2 中适合处理耗时任务的通信方式。

与 Service 相比，Action 不只是得到最终结果，还可以在任务执行过程中持续获得 Feedback，并且支持取消正在执行的 Goal。

可以简单记为：

Topic = 持续数据

Service = Request → Response

Action = Goal → Feedback → Result


## Goal

Goal 表示 Client 希望 Action Server 完成的任务目标。

例如 MoveRobot：

target_x = 0.3
target_y = 0.1
target_z = 0.2

表示要求机器人移动到指定目标位置。


## Feedback

Feedback 是任务执行过程中 Server 返回给 Client 的状态或进度。

例如：

20% MOVING
40% MOVING
60% MOVING
80% MOVING
100% ARRIVED

Server 使用：

goal_handle.publish_feedback(feedback_msg)

发送 Feedback。

Client 使用 feedback_callback() 处理收到的 Feedback。


## Result

Result 是任务结束后 Server 返回的最终结果。

例如：

success = True
message = "Target reached."

Server 最后：

goal_handle.succeed()

然后返回 MoveRobot.Result()。


## Action Client

Action Client 使用 ActionClient 创建。

例如：

ActionClient(
    self,
    MoveRobot,
    '/move_robot'
)

其中：

MoveRobot = Action 接口类型

/move_robot = Action 名


## 发送 Goal

先创建 Goal：

goal_msg = MoveRobot.Goal()

然后填写：

goal_msg.target_x = 0.3
goal_msg.target_y = 0.1
goal_msg.target_z = 0.2

再通过：

send_goal_async()

异步发送 Goal。


## Action Client 的三个主要 Callback

goal_response_callback()

处理 Server 是否接受 Goal。

feedback_callback()

处理任务执行过程中的 Feedback。

get_result_callback()

处理任务最终的 Result。


## Action Server

Action Server 接收到 Goal 后执行 execute_callback()。

执行过程中：

读取 Goal
→ 执行任务
→ publish_feedback()
→ 持续执行
→ succeed()
→ return Result


## Cancel

Client 使用：

goal_handle.cancel_goal_async()

请求取消当前 Goal。

Server 使用：

cancel_callback()

决定接受还是拒绝取消请求。

任务执行过程中可以检查：

goal_handle.is_cancel_requested

如果收到取消请求：

goal_handle.canceled()

然后返回取消后的 Result。


## MultiThreadedExecutor

如果耗时任务和 Cancel 处理共用一个执行线程，执行任务可能长期占用线程，使 Cancel 无法及时处理。

因此本项目使用：

MultiThreadedExecutor

配合：

ReentrantCallbackGroup

使 Action 执行和 Cancel 等回调可以并发得到处理。


## 自定义 MoveRobot Action

接口文件：

robot_interfaces/action/MoveRobot.action

定义：

float64 target_x
float64 target_y
float64 target_z
---
bool success
string message
---
float32 progress
string state

Goal：

目标位置。

Result：

最终成功状态和说明。

Feedback：

执行进度和当前状态。


## Topic / Service / Action

Topic：

适合持续发布的数据，例如机器人状态、相机图像和关节状态。

Service：

适合短时间的一次请求和一次响应，例如打开夹爪、复位设备。

Action：

适合耗时、需要过程反馈、并可能中途取消的任务，例如机械臂移动到目标位姿。