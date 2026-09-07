import math
import rclpy

from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class MovingTFBroadcaster(Node):

    def __init__(self):
        super().__init__('moving_tf_broadcaster')

        # 创建动态 TF 广播器
        self.tf_broadcaster = TransformBroadcaster(self)

        # 模拟 tool_link 的初始位置
        self.x_position = 0.0

        # 模拟绕 Z 轴旋转的角度
        self.yaw = 0.0

        # 每 0.5 秒更新一次 TF
        self.timer = self.create_timer(
            0.5,
            self.broadcast_transform
        )

    def broadcast_transform(self):

        transform = TransformStamped()

        # 当前时间
        transform.header.stamp = (
            self.get_clock().now().to_msg()
        )

        # 父坐标系
        transform.header.frame_id = 'base_link'

        # 子坐标系
        transform.child_frame_id = 'tool_link'

        # 模拟 tool_link 相对于 base_link 的平移
        transform.transform.translation.x = self.x_position
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.5

        # 模拟 tool_link 绕 Z 轴旋转
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = math.sin(
            self.yaw / 2.0
        )
        transform.transform.rotation.w = math.cos(
            self.yaw / 2.0
        )

        # 发布 TF
        self.tf_broadcaster.sendTransform(
            transform
        )

        # 打印当前状态
        self.get_logger().info(
            f'base_link -> tool_link: '
            f'x={self.x_position:.2f}, '
            f'yaw={math.degrees(self.yaw):.0f} deg'
        )

        # 模拟沿 X 轴移动
        self.x_position += 0.05

        # X 超过 1 米后重新开始
        if self.x_position > 1.0:
            self.x_position = 0.0

        # 每次绕 Z 轴增加 10 度
        self.yaw += math.radians(10.0)

        # 转满 360 度后重新开始
        if self.yaw >= 2.0 * math.pi:
            self.yaw = 0.0


def main(args=None):
    rclpy.init(args=args)

    node = MovingTFBroadcaster()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()