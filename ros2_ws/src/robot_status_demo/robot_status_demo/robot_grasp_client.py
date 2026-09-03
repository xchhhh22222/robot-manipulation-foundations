import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class RobotGraspClient(Node):

    def __init__(self):
        super().__init__('robot_grasp_client')

        self.client_ = self.create_client(
            Trigger,
            '/trigger_grasp'
        )

        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Waiting for /trigger_grasp service...'
            )

        self.request_ = Trigger.Request()

    def send_request(self):
        future = self.client_.call_async(self.request_)
        return future


def main(args=None):
    rclpy.init(args=args)

    node = RobotGraspClient()

    future = node.send_request()

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