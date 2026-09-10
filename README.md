# Robot Manipulation Foundations

A hands-on robotics project focused on embodied AI, robot manipulation, and ROS2 development.

## Goal

Build a complete robot manipulation pipeline from:

- ROS2
- Robot communication
- Robot kinematics
- Motion planning
- Simulation
- Robot learning
- Vision-Language-Action models


## Roadmap

- [x] Development environment
- [ ] ROS2 communication
- [ ] TF2
- [ ] URDF
- [ ] Robot kinematics
- [ ] MoveIt2
- [ ] MuJoCo simulation
- [ ] Pick and Place
- [ ] Imitation Learning
- [ ] Vision Language Action


## Environment

- Ubuntu 24.04
- ROS2 Jazzy
- Python 3
- C++
## MoveIt2 Collision-Aware Motion Planning

A 2-DOF robot arm is planned from the same `home` configuration
to the same `ready` configuration under two different planning scenes:

- No obstacle
- A box collision object added to the MoveIt Planning Scene

The robot uses:

- MoveIt2
- MoveItPy
- OMPL / RRTConnect
- ros2_control
- JointTrajectoryController
- Mock Hardware

### Planning pipeline

```text
MoveItPy
→ Planning Scene
→ OMPL / RRTConnect
→ FollowJointTrajectory
→ arm_controller
→ ros2_control
→ Mock Hardware