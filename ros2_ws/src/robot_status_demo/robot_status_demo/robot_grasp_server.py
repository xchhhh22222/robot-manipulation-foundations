import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class RobotGraspServer(Node):

    def __init__(self):
        super().__init__('robot_grasp_server')

        self.service_ = self.create_service(
            Trigger,
            '/trigger_grasp',
            self.handle_grasp
        )

    def handle_grasp(self, request, response):
        self.get_logger().info(
            'Received grasp request.'
        )

        response.success = True
        response.message = 'Grasp request accepted.'

        return response


def main(args=None):
    rclpy.init(args=args)

    node = RobotGraspServer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()