import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class RobotGripperControlClient(Node):

    def __init__(self):
        super().__init__('robot_gripper_control_client')

        self.client_ = self.create_client(
            SetBool,
            '/command_gripper'
        )

        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Waiting for /command_gripper service...'
            )

    def send_request(self, close_gripper):
        request = SetBool.Request()
        request.data = close_gripper

        future = self.client_.call_async(request)

        return future


def main(args=None):
    rclpy.init(args=args)

    node = RobotGripperControlClient()

    future = node.send_request(False)

    rclpy.spin_until_future_complete(
        node,
        future
    )

    response = future.result()

    node.get_logger().info(
        f'Success: {response.success}'
    )

    node.get_logger().info(
        f'Message: {response.message}'
    )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()