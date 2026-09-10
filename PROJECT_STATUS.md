# Project Status

## Environment

- Windows 11 + WSL2 Ubuntu 24.04
- ROS2 Jazzy
- Workspace: `ros2_ws`
- Main robot: 2-DOF `simple_arm`

---

## Current Milestone

MoveIt2 collision-aware joint-space motion planning pipeline completed.

Current progress:

ROS2 fundamentals
→ TF2
→ URDF / Xacro
→ Collision / Inertial
→ ros2_control
→ MoveIt2
→ Collision-aware Planning

---

## Completed

### ROS2 Foundations

- Topics / Publisher / Subscriber
- Services
- Custom Actions
- Launch files
- ROS2 Parameters
- TF2 broadcasters and listeners
- Point coordinate transformations

### Robot Description

Package:

`ros2_ws/src/robot_description`

Implemented:

- URDF
- Xacro
- 2-DOF robot arm
- `base_link`
- `joint1`
- `link1`
- `joint2`
- `link2`
- `tool_link`
- Visual geometry
- Collision geometry
- Inertial properties
- Xacro properties and macros

### ros2_control

Implemented:

- `simple_arm.ros2_control.xacro`
- `mock_components/GenericSystem`
- Position command interfaces
- Position / velocity state interfaces
- `joint_state_broadcaster`
- `JointTrajectoryController`
- `arm_controller`

Verified:

- Controllers become ACTIVE
- `/joint_states` is published
- `/arm_controller/follow_joint_trajectory` accepts goals
- Joint trajectories execute successfully

### MoveIt2

Package:

`ros2_ws/src/simple_arm_moveit_config`

Implemented configuration:

- `simple_arm.srdf`
- `kinematics.yaml`
- `joint_limits.yaml`
- `ompl_planning.yaml`
- `ros2_controllers.yaml`
- `moveit_controllers.yaml`
- `moveit_cpp.yaml`

Planning group:

`arm`

Kinematic chain:

`base_link -> tool_link`

Named states:

- `home = [0.0, 0.0]`
- `ready = [-0.6, 0.8]`

Planner:

- MoveIt2
- OMPL
- RRTConnect

### MoveItPy

Implemented:

`moveit_named_target_demo.py`

Pipeline:

MoveItPy
→ OMPL / RRTConnect
→ JointTrajectory
→ arm_controller
→ ros2_control
→ Mock Hardware

Verified:

- Planning succeeds
- Trajectory goal is accepted
- Controller completes execution
- Execution status is SUCCEEDED

### Collision-Aware Planning

Implemented:

`moveit_collision_demo.py`

Planning Scene contains a box collision object.

Test obstacle:

- size: `[0.10, 0.20, 0.10]`
- x: `0.20`
- y: `0.0`
- z: `0.50`

Verified:

- Invalid goal collision can produce `GOAL_STATE_INVALID`
- MoveIt can generate a different collision-free trajectory when an obstacle affects the planning scene

### Experiment Results

Generated:

- `results/no_obstacle.csv`
- `results/with_obstacle.csv`
- `results/trajectory_comparison.png`

The comparison plot represents joint space:

`(joint1, joint2)`

It is NOT an end-effector Cartesian XY trajectory.

---

## Current System Architecture

```text
User Goal
   ↓
MoveItPy
   ↓
Planning Scene
   ↓
Collision Checking
   ↓
OMPL / RRTConnect
   ↓
JointTrajectory
   ↓
FollowJointTrajectory Action
   ↓
arm_controller
   ↓
ros2_control
   ↓
GenericSystem Mock Hardware
   ↓
joint1 / joint2
   ↓
/joint_states
   ↓
robot_state_publisher
   ↓
TF / RViz