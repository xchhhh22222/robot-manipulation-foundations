# ROS2 Service Communication Notes

## Service 是什么

Service 是 ROS2 中的一种请求-响应通信方式。

Client 发送 Request，
Server 处理请求并返回 Response。

与 Topic 不同：

Topic 更适合持续发布数据，不要求接收方回复。

Service 更适合一次明确的请求，并需要得到处理结果。


## Server 是什么

Server 提供一个 Service。

当 Client 发来 Request 后，
Server 执行对应的 callback，
然后填写并返回 Response。


## Client 是什么

Client 用来调用 Service。

Client 通过：

- Service 类型
- Service 名

确定自己要调用哪个 Service。

例如：

create_client(
    SetBool,
    '/command_gripper'
)

表示：

调用名为 /command_gripper 的 SetBool Service。


## Request 和 Response

Request：

Client → Server

表示客户端发送给服务端的数据。

Response：

Server → Client

表示服务端处理后返回的数据。


## Trigger

Trigger 的接口：

---
bool success
string message

Request 为空。

因此它适合：

“触发一次操作”

例如：

执行一次抓取。


## SetBool

SetBool 的接口：

bool data
---
bool success
string message

Request 包含：

bool data

例如约定：

True → 关闭夹爪
False → 打开夹爪


## create_service()

create_service() 用来在 Node 上创建 Service Server。

例如：

create_service(
    SetBool,
    '/command_gripper',
    self.handle_gripper
)

表示：

提供 /command_gripper Service，
使用 SetBool 接口，
收到请求后调用 handle_gripper。


## create_client()

create_client() 用来在 Node 上创建 Service Client。

例如：

create_client(
    SetBool,
    '/command_gripper'
)

表示这个 Client 要调用 /command_gripper。


## Callback 为什么不加括号

self.handle_gripper

表示：

把函数本身交给 ROS2，
以后收到请求时由 ROS2 调用。

self.handle_gripper()

表示：

现在立刻执行这个函数。


## Service Client 异步调用

call_async(request)

异步发送 Request。

future

用于跟踪这次请求未来的结果。

spin_until_future_complete(node, future)

让 ROS2 处理通信事件，
直到这次请求完成。

future.result()

取得 Server 最终返回的 Response。


## Topic 和 Service

Topic：

Publisher → Topic → Subscriber

适合：

机器人状态
传感器数据
连续数据流


Service：

Client → Server
Client ← Response

适合：

打开夹爪
重置机器人
设置参数
查询一次结果