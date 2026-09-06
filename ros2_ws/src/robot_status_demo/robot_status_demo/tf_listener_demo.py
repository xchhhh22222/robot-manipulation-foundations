import rclpy

from rclpy.node import Node
from rclpy.time import Time

from tf2_ros import Buffer
from tf2_ros import TransformListener
from tf2_ros import TransformException


class TFListenerDemo(Node):

    def __init__(self):
        super().__init__('tf_listener_demo')

        self.tf_buffer = Buffer()

        self.tf_listener = TransformListener(
            self.tf_buffer,
            self
        )

        self.timer = self.create_timer(
            0.5,
            self.lookup_transform
        )

    def lookup_transform(self):

        try:
            transform = self.tf_buffer.lookup_transform(
                'base_link',
                'tool_link',
                Time()
            )

            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z

            self.get_logger().info(
                f'tool_link in base_link: '
                f'x={x:.2f}, y={y:.2f}, z={z:.2f}'
            )

        except TransformException as ex:
            self.get_logger().warn(
                f'Could not get transform: {ex}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = TFListenerDemo()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()