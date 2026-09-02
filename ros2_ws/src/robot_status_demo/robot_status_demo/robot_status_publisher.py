import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class RobotStatusPublisher(Node):

    def __init__(self):
        super().__init__('robot_status_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/robot_status',
            10
        )

        self.status_list = [
            'IDLE',
            'MOVING',
            'GRASPING'
        ]

        self.status_index = 0

        self.timer_ = self.create_timer(
            1.0,
            self.timer_callback
        )
    def timer_callback(self):
        msg = String()

        msg.data = self.status_list[self.status_index]

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing robot status: {msg.data}'
        )

        self.status_index = (
            self.status_index + 1
        ) % len(self.status_list)
    
def main(args=None):
    rclpy.init(args=args)

    node = RobotStatusPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
