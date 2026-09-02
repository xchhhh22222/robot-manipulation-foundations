import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotStatusMonitor(Node):

    def __init__(self):
        super().__init__('robot_status_monitor')

        self.current_status = None
        self.allowed_transitions = {
            None: ['IDLE', 'MOVING', 'GRASPING'],
            'IDLE': ['MOVING'],
            'MOVING': ['GRASPING'],
            'GRASPING': ['IDLE']
        }
        self.subscription_ = self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):
        new_status = msg.data

        if new_status == self.current_status:
            return

        allowed_states = self.allowed_transitions.get(
            self.current_status,
            []
        )

        if new_status not in allowed_states:
            self.get_logger().warn(
                f'Invalid state transition: '
                f'{self.current_status} -> {new_status}'
            )
            return

        self.get_logger().info(
            f'State transition: '
            f'{self.current_status} -> {new_status}'
        )

        self.current_status = new_status

        if new_status == 'IDLE':
            self.handle_idle()

        elif new_status == 'MOVING':
            self.handle_moving()

        elif new_status == 'GRASPING':
            self.handle_grasping()

    def handle_idle(self):
        self.get_logger().info(
            'Robot is waiting.'
        )

    def handle_moving(self):
        self.get_logger().info(
            'Robot is moving to target.'
        )

    def handle_grasping(self):
        self.get_logger().info(
            'Robot is grasping object.'
        )


def main(args=None):
    rclpy.init(args=args)

    node = RobotStatusMonitor()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()