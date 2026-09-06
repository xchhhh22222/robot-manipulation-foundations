# ROS2 TF2 Coordinate Transform Notes

## Frame

Frame 表示一个坐标系。

例如：

- base_link：机器人底座坐标系
- camera_link：相机坐标系
- tool_link：机械臂末端工具坐标系
- object_frame：物体坐标系

同一个 XYZ 数值放在不同 Frame 中，代表的位置可能完全不同。


## Transform

Transform 表示两个 Frame 之间的位姿关系。

它包含：

Translation
= 平移 x、y、z

Rotation
= 旋转姿态

因此：

base_link → camera_link

camera_link → object_frame

base_link → tool_link

都可以表示为 Transform。


## Static TF

Static TF 表示两个 Frame 之间的关系固定不变。

例如固定安装的相机：

base_link
↓
camera_link

如果安装位置不变化，这个 Transform 就可以使用 Static TF。


## Dynamic TF

Dynamic TF 表示两个 Frame 之间的位置或姿态会随时间变化。

例如：

base_link
↓
tool_link

机械臂运动时，tool_link 相对于 base_link 的位置和旋转会不断改变。


## TF Broadcaster

Broadcaster 用于发布 Transform。

动态 TF 中可以使用：

TransformBroadcaster

真正发布坐标关系：

sendTransform()


## TF Listener 和 Buffer

TransformListener：

负责接收 TF 数据。

Buffer：

保存收到的 Transform，供程序查询。

基本关系：

Broadcaster
↓
TF
↓
Listener
↓
Buffer
↓
lookup_transform()


## lookup_transform()

例如：

lookup_transform(
    'base_link',
    'tool_link',
    Time()
)

表示查询：

tool_link 相对于 base_link 的 Transform。

Time() 表示查询最新可用的 Transform。


## TransformException

当所需坐标系暂时不存在，或者 TF 链还没有建立完成时，

lookup_transform() 可能抛出 TransformException。

通过 try / except 捕获异常，可以让程序继续运行，而不是直接崩溃。


## 链式坐标变换

TF2 可以自动组合多段坐标关系。

例如：

base_link
↓
camera_link
↓
object_frame

只要两段 Transform 都存在，

就可以直接查询：

base_link → object_frame

而不需要人工逐段计算。


## 平移与旋转

如果两个坐标系只有平移、没有旋转，

可以直观理解为 XYZ 平移量相加。

但存在旋转以后，不能再直接对 XYZ 做简单加法。

原因是子坐标系的 X、Y、Z 轴方向已经发生变化。

坐标转换本质上是：

p_parent = R × p_child + t

其中：

R = Rotation

t = Translation


## PointStamped 坐标转换

实际视觉系统中，不一定需要给每个检测物体创建一个 TF Frame。

可以直接创建：

PointStamped

例如：

物体在 tool_link 下：

(1.0, 0.0, 0.0)

然后查询：

base_link ← tool_link

的 Transform。

最后使用：

do_transform_point()

把物体坐标转换成 base_link 坐标。


## 与视觉抓取的关系

真实视觉抓取流程可以理解为：

相机检测物体
↓
得到物体在 camera_link 下的位置
↓
手眼标定提供 camera 与机器人之间的 Transform
↓
TF2 保存和组合坐标关系
↓
把物体位置转换到 base_link
↓
机械臂根据 base 坐标执行抓取


## 手眼标定与 TF2

手眼标定：

负责求出相机坐标系和机器人坐标系之间的 Transform。

TF2：

负责保存、查询、组合和使用这些 Transform。

两者不是同一个东西。


## Day 7 核心总结

Frame
= 坐标系

Transform
= 两个 Frame 之间的平移 + 旋转

Broadcaster
= 发布 Transform

Listener
= 接收 Transform

Buffer
= 保存 Transform

lookup_transform()
= 查询 Transform

TF2
= 管理和组合机器人系统中的坐标关系