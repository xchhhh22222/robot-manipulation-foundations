import rclpy

from rclpy.node import Node
from rclpy.time import Time

from geometry_msgs.msg import PointStamped

from tf2_ros import Buffer
from tf2_ros import TransformListener
from tf2_ros import TransformException

from tf2_geometry_msgs import do_transform_point


class PointTransformDemo(Node):

    def __init__(self):
        super().__init__('point_transform_demo')

        self.tf_buffer = Buffer()

        self.tf_listener = TransformListener(
            self.tf_buffer,
            self
        )

        self.timer = self.create_timer(
            0.5,
            self.transform_point
        )

    def transform_point(self):

        # 模拟“视觉检测到的物体位置”
        point_tool = PointStamped()

        point_tool.header.frame_id = 'tool_link'

        point_tool.point.x = 1.0
        point_tool.point.y = 0.0
        point_tool.point.z = 0.0

        try:
            # 查询 tool_link → base_link 的坐标变换
            transform = self.tf_buffer.lookup_transform(
                'base_link',
                'tool_link',
                Time()
            )

            # 真正执行坐标转换
            point_base = do_transform_point(
                point_tool,
                transform
            )

            self.get_logger().info(
                f'tool point: '
                f'({point_tool.point.x:.2f}, '
                f'{point_tool.point.y:.2f}, '
                f'{point_tool.point.z:.2f}) '
                f'-> base point: '
                f'({point_base.point.x:.2f}, '
                f'{point_base.point.y:.2f}, '
                f'{point_base.point.z:.2f})'
            )

        except TransformException as ex:
            self.get_logger().warn(
                f'Could not transform point: {ex}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = PointTransformDemo()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()