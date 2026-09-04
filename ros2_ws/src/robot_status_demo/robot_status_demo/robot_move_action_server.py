import time
import rclpy

from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from robot_interfaces.action import MoveRobot


class RobotMoveActionServer(Node):

    def __init__(self):
        super().__init__('robot_move_action_server')

        self.action_callback_group = ReentrantCallbackGroup()

        self.action_server = ActionServer(
            self,
            MoveRobot,
            '/move_robot',
            self.execute_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.action_callback_group
        )

    def cancel_callback(self, cancel_request):
        self.get_logger().info('Received cancel request.')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):

        target_x = goal_handle.request.target_x
        target_y = goal_handle.request.target_y
        target_z = goal_handle.request.target_z

        self.get_logger().info(
            f'Moving robot to x={target_x}, '
            f'y={target_y}, z={target_z}'
        )

        feedback_msg = MoveRobot.Feedback()
        total_steps = 5

        for step in range(1, total_steps + 1):

            if goal_handle.is_cancel_requested:
                self.get_logger().info('Goal canceled.')

                goal_handle.canceled()

                result = MoveRobot.Result()
                result.success = False
                result.message = 'Movement canceled.'

                return result

            progress = step / total_steps

            feedback_msg.progress = float(progress)

            if progress < 1.0:
                feedback_msg.state = 'MOVING'
            else:
                feedback_msg.state = 'ARRIVED'

            goal_handle.publish_feedback(feedback_msg)

            time.sleep(1.0)

        goal_handle.succeed()

        result = MoveRobot.Result()
        result.success = True
        result.message = 'Target reached.'

        return result


def main(args=None):
    rclpy.init(args=args)

    node = RobotMoveActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()