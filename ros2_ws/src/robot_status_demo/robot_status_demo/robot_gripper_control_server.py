import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class RobotGripperControlServer(Node):

    def __init__(self):
        super().__init__('robot_gripper_control_server')

        self.service_ = self.create_service(
            SetBool,
            '/command_gripper',
            self.handle_gripper
        )

    def handle_gripper(self, request, response):

        if request.data:
            self.get_logger().info(
                'Closing gripper.'
            )

            response.success = True
            response.message = 'Gripper closed.'

        else:
            self.get_logger().info(
                'Opening gripper.'
            )

            response.success = True
            response.message = 'Gripper opened.'

        return response


def main(args=None):
    rclpy.init(args=args)

    node = RobotGripperControlServer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()