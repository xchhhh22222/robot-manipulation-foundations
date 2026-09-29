# CURRENT HANDOFF — 2026-09-29 — Day25 End

> This is the current cross-chat handoff for `xchhhh22222/robot-manipulation-foundations`.
>
> A new GPT must **first read** `docs/EMBODIED_AI_MASTER_PLAN.md`, then read the latest `main` code from GitHub, then read this file. Do not treat this handoff as a substitute for the real repository state.

## 1. User / teaching mode

Environment:

- Windows 11 + WSL2 Ubuntu 24.04
- ROS2 Jazzy
- Workspace: `~/robotics/robot-manipulation-foundations/ros2_ws`
- Main repo: `xchhhh22222/robot-manipulation-foundations`
- Main branch: `main`
- Local GPU: Radeon 780M; no local CUDA
- Heavy Robot Learning training should use cloud GPU later

User goal:

- Build a complete Embodied AI / robot manipulation skill chain for internships and later recruiting.
- Do not optimize for “knowing many frameworks”; optimize for a reproducible, explainable robot manipulation system with measurable failure analysis.

Teaching constraints:

- One hypothesis → one verification → one modification.
- Do not dump many changes at once.
- Explain Git commands before asking the user to run them.
- Prefer VS Code with absolute path for edits.
- Diagnose from logs before guessing.
- The user wants to understand the code, especially the core data flow and system logic.
- For large source edits, prefer giving a complete replacement file plus explanation of the core logic, rather than many fragile patch snippets.

## 2. Long-term roadmap

The current master sequence is:

```text
ROS2
→ TF2 / SE(3)
→ URDF / Xacro
→ ros2_control
→ MoveIt2
→ IK / planning / execution
→ Planning Scene / collision semantics
→ gripper
→ attach / detach
→ Pick & Place
→ Failure Handling / Task State
→ Pose-driven manipulation
→ camera / TF / calibration
→ MuJoCo
→ Robot Data / Benchmark
→ LeRobot
→ ACT
→ Diffusion Policy
→ LIBERO / robustness
→ VLA
```

Do not jump directly to VLA or heavy learning before the robot-system foundation is stable.

## 3. Day24 baseline already completed

Current Pick & Place task sequence:

```text
OPEN
→ PREGRASP
→ GRASP
→ CLOSE
→ ATTACH
→ LIFT
→ PREPLACE
→ PLACE
→ OPEN
→ DETACH
→ RETREAT
```

Important scene semantics:

- Table center z = 0.20, height = 0.05, so top z = 0.225.
- Pick object center z = 0.275, height = 0.10, so its bottom is exactly z = 0.225.
- Therefore the object initially has zero-gap support contact with the table.
- A real failure occurred at LIFT because MoveIt detected `pick_object - table` collision after ATTACH.
- Correct fix: temporarily allow `pick_object <-> table` during initial LIFT, then restore collision checking after the lift.
- Do not “fix” this primarily by moving the object upward by an arbitrary epsilon.
- `touch_links` already handles expected object/finger contact.

Current backend is mock `ros2_control GenericSystem`.

## 4. Day25 work completed today

### 4.1 Support-contact collision semantics

The current code contains `set_allowed_collision(...)` using MoveIt's Planning Scene Monitor / Allowed Collision Matrix.

The intended sequence is:

```text
ATTACH
→ pick_object <-> table = ALLOWED
→ LIFT
→ pick_object <-> table = NOT ALLOWED
```

This behavior was previously runtime-verified on the Day24 implementation.

### 4.2 Structured stage result foundation

The source now defines:

```python
@dataclass
class StageResult:
    success: bool
    stage: str
    failure_type: str
    detail: str
```

Purpose: arm stages should return structured information instead of only killing the process or returning an ambiguous boolean.

Current planned failure types include:

- `PLAN_FAILED`
- `EXECUTION_FAILED`
- later: gripper / scene / startup / recovery categories

### 4.3 Common arm-stage function

The source now defines `run_arm_stage(...)`.

Its responsibility is:

```text
joint target
→ RobotState
→ current start state
→ set goal
→ MoveIt planning
→ execute trajectory
→ inspect execution status
→ return StageResult
```

Conceptual split that the user now understands:

- `joint_positions` = **where the robot should go** in joint space.
- `run_arm_stage()` = **how MoveIt plans and executes the move, plus result checking**.

Also distinguish:

- Joint goal = six joint angles.
- Pose goal = end-effector position/orientation.
- Current Pick & Place still primarily uses hard-coded Joint Goals.
- Pose-driven manipulation is a later mainline step.

### 4.4 Exact end-of-day source state — IMPORTANT

Do not assume all six arm stages are refactored.

The exact source uploaded at the end of Day25 has:

- `StageResult`: added.
- `run_arm_stage()`: added.
- PREGRASP: migrated to `run_arm_stage()`.
- GRASP: still legacy inline planning/execution code.
- LIFT: still legacy inline planning/execution code.
- PREPLACE: still legacy inline planning/execution code.
- PLACE: still legacy inline planning/execution code.
- RETREAT: still legacy inline planning/execution code.

PREGRASP still creates a temporary `pregrasp_joint_state` because the old LIFT block currently depends on it.

A later draft of a full six-stage refactor was discussed, but it was **not the user's runtime-verified local state at handoff time**. Do not silently assume that draft is active.

The GitHub update made with this handoff intentionally tracks the user's actual uploaded Day25 source, not an unverified future refactor.

## 5. Benchmark / failure taxonomy work completed

A local runner was built at:

`tools/run_pick_benchmark.py`

Capabilities already tested locally:

- launch one Pick & Place run automatically;
- stream output to terminal and a unique log file;
- classify PASS / FAIL;
- classify historical:
  - LIFT planning failure → `PLAN_FAILED`
  - startup `PackageNotFoundError` → `PACKAGE_ERROR`
  - successful run → PASS
- append one CSV row per run;
- support `--runs N`;
- collect per-run structured results;
- print batch summary.

A formal 3-run smoke test completed:

```text
Runs: 3
PASS: 3
FAIL: 0
Success Rate: 100.0%
```

CSV rows for that batch were confirmed.

Important user decision:

> Do NOT spend time on a 20-run benchmark now. Prioritize the mainline.

The exact local `tools/run_pick_benchmark.py` file was not uploaded in the handoff turn, so it is **not being reconstructed from memory and pushed automatically**. Ask for the exact local file before committing it if it is still absent from GitHub.

## 6. Important failure-handling concepts already taught

Do not teach these incorrectly:

- Planning failure is not equivalent to “software failure”.
- Execution failure is not equivalent to “hardware unreachable”.
- Geometric unreachability / IK failure normally appears on the planning side.
- Controller rejection, tracking, communication, etc. are execution-side failures.
- Robot state problems can influence both.

Current target architecture:

```text
Task stage
→ plan
→ execute
→ structured StageResult
→ task-level policy
   ├── retry
   ├── scene reset
   ├── recovery
   └── abort
```

Low-level motion functions should eventually report failure; task-level logic should decide what to do about it.

## 7. Known environment issue

On this machine, `colcon build --symlink-install` caused a Python package metadata / legacy egg-link issue:

`PackageNotFoundError: No package metadata was found for moveit-6dof-demos`

After cleaning only this package's generated build/install directories and rebuilding with:

```bash
colcon build --packages-select moveit_6dof_demos
```

the direct package metadata was generated correctly.

Do not generalize this into “symlink-install is bad”. It is a local toolchain behavior. For now, use regular `colcon build` for this package; after Python edits, rebuild before launching.

## 8. Day26 / next-session plan

Continue the mainline, not benchmark repetition.

First verify the real repository state and local/remote synchronization.

Then proceed atomically:

1. Migrate GRASP from duplicated inline `set goal → plan → execute` into `run_arm_stage()`.
2. Build / syntax-check / run to verify behavior equivalence.
3. Migrate LIFT carefully. Preserve ACM semantics and ensure temporary `pick_object <-> table = ALLOWED` is restored even when LIFT fails.
4. Migrate PREPLACE.
5. Migrate PLACE.
6. Migrate RETREAT.
7. After the refactor is runtime-stable, remove temporary `pregrasp_joint_state` / `preplace_joint_state` dependencies.
8. Only then change behavior from immediate `os._exit(1)` to task-level failure handling / retry / recovery.
9. After Failure Handling / Task State is stable, advance to Pose-driven manipulation.

Do not combine all steps into one edit unless the user explicitly requests a full replacement file. Even then, explain the core logic and verify runtime behavior before calling it complete.

## 9. Recommended first action for the next GPT

Use the GitHub connector to read:

- `docs/EMBODIED_AI_MASTER_PLAN.md`
- `docs/CURRENT_HANDOFF.md`
- `ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py`
- `ros2_ws/src/moveit_6dof_demos/launch/pick_demo.launch.py`
- `ros2_ws/src/moveit_6dof_demos/config/simple_6dof_arm.srdf`
- `ros2_ws/src/moveit_6dof_demos/config/ros2_controllers.yaml`
- `ros2_ws/src/moveit_6dof_demos/config/moveit_controllers.yaml`
- `ros2_ws/src/moveit_6dof_demos/urdf/simple_6dof_arm.urdf.xacro`

Do not rely only on this document's code summary.

Then tell the user:

- the actual `main` HEAD;
- what is truly implemented;
- the single next atomic step.

The next atomic coding step should normally be **GRASP migration into `run_arm_stage()`**, unless the repository has changed since this handoff.
