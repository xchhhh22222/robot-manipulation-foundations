import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from robot_interfaces.action import MoveRobot


class RobotMoveActionClient(Node):

    def __init__(self):
        super().__init__('robot_move_action_client')

        self.action_client = ActionClient(
            self,
            MoveRobot,
            '/move_robot'
        )

        self.goal_handle = None
        self.cancel_sent = False

    def send_goal(self, target_x, target_y, target_z):

        goal_msg = MoveRobot.Goal()

        goal_msg.target_x = target_x
        goal_msg.target_y = target_y
        goal_msg.target_z = target_z

        self.action_client.wait_for_server()

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self.send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.')
            return

        self.get_logger().info('Goal accepted.')

        self.goal_handle = goal_handle

        self.get_result_future = goal_handle.get_result_async()

        self.get_result_future.add_done_callback(
            self.get_result_callback
        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Progress: {feedback.progress * 100:.0f}% '
            f'State: {feedback.state}'
        )

        if (
            feedback.progress >= 0.4
            and not self.cancel_sent
            and self.goal_handle is not None
        ):
            self.cancel_sent = True

            self.get_logger().info(
                'Requesting goal cancel.'
            )

            self.cancel_future = (
                self.goal_handle.cancel_goal_async()
            )

            self.cancel_future.add_done_callback(
                self.cancel_done_callback
            )

    def cancel_done_callback(self, future):

        cancel_response = future.result()

        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info(
                'Cancel request accepted.'
            )
        else:
            self.get_logger().info(
                'Cancel request rejected.'
            )

    def get_result_callback(self, future):

        result = future.result().result

        self.get_logger().info(
            f'Success: {result.success}'
        )

        self.get_logger().info(
            f'Message: {result.message}'
        )

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = RobotMoveActionClient()

    node.send_goal(
        0.3,
        0.1,
        0.2
    )

    rclpy.spin(node)


if __name__ == '__main__':
    main()