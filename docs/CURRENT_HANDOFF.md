# CURRENT HANDOFF — 2026-09-30 — Day26 End

> Repository: `xchhhh22222/robot-manipulation-foundations`
>
> This is the current cross-chat handoff after Day26.
>
> A new GPT must **first read** `docs/EMBODIED_AI_MASTER_PLAN.md`, then verify the actual latest `main` state and read the latest `pick_demo.py`. Do not treat this handoff as a substitute for the real repository state.

---

## 0. New GPT: start here

The user is learning Embodied AI / robot manipulation deeply. The goal is not merely to make code run; the user must understand the system layers, data flow, failure semantics, and engineering tradeoffs.

Before changing code:

1. Read `docs/EMBODIED_AI_MASTER_PLAN.md`.
2. Read this handoff completely.
3. Verify Git state:
   ```bash
   git status -sb
   git log --oneline --decorate --graph -6
   git log origin/main..HEAD --oneline
   ```
4. Read the actual latest:
   - `ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py`
   - `ros2_ws/src/moveit_6dof_demos/launch/pick_demo.launch.py`
   - relevant MoveIt / ros2_control configs when needed.
5. Tell the user:
   - actual local HEAD;
   - actual remote `origin/main` HEAD;
   - whether they differ;
   - the current milestone;
   - the **single next atomic step**.

Do not jump to Pose-driven manipulation yet.

The immediate next milestone is:

```text
StageResult
→ task-level failure policy
→ retry / recovery / reset / abort
```

---

## 1. Repository / environment

Environment:

- Windows 11
- WSL2 Ubuntu 24.04
- ROS2 Jazzy
- Workspace: `~/robotics/robot-manipulation-foundations/ros2_ws`
- Repository: `xchhhh22222/robot-manipulation-foundations`
- Main branch: `main`
- Local GPU: Radeon 780M, no local CUDA
- Heavy Robot Learning training should use cloud GPU later
- Current robot backend: mock `ros2_control GenericSystem` / mock hardware behavior

Known local build behavior:

- `colcon build --symlink-install` previously caused a Python package metadata / legacy egg-link issue:
  `PackageNotFoundError: No package metadata was found for moveit-6dof-demos`
- After cleaning only this package's generated build/install output, normal build worked:
  ```bash
  colcon build --packages-select moveit_6dof_demos
  ```
- Do not generalize this into “symlink-install is bad”. It is a local toolchain issue.
- For now, after Python edits, use regular `colcon build --packages-select moveit_6dof_demos` before runtime validation.

---

## 2. Teaching / debugging protocol

Strict protocol:

```text
one hypothesis
→ one verification
→ one modification
```

Rules:

- One atomic step at a time.
- Do not dump many edits at once.
- Explain shell / Git commands before asking the user to run them.
- Prefer logs over guesses.
- Prefer explicit file paths / VS Code for edits.
- Build and runtime-verify after meaningful changes.
- Do not silently change architecture just because a shorter implementation exists.
- The user wants to understand why each layer exists.

Useful semantic mappings the user already understands:

```text
joint_positions
= where the robot should go

run_arm_stage()
= how MoveIt plans / executes / checks

StageResult
= what happened

Task Policy
= what the task should do next
```

Important conceptual boundary:

```text
low-level motion
= report facts

task-level policy
= make decisions
```

---

## 3. Long-term roadmap

The master sequence remains:

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

Current position:

```text
Pick & Place
        ↓
Failure Handling / Task State   ← NOW
        ↓
Pose-driven manipulation        ← NOT YET
```

Do not jump directly to VLA / heavy learning before the robot-system foundation is stable.

---

## 4. Current Pick & Place sequence

Current task sequence:

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

Semantic meanings:

```text
PREGRASP = move above the object
GRASP    = descend to grasp position
LIFT     = lift object away from the table
PREPLACE = carry object in the air to above destination
PLACE    = descend to the final placement position
RETREAT  = after release/detach, move the arm back upward
```

---

## 5. Planning Scene support-contact semantics — DO NOT REGRESS

Table:

- center z = `0.20`
- height = `0.05`
- top z = `0.225`

Pick object:

- center z = `0.275`
- height = `0.10`
- bottom z = `0.225`

Therefore:

```text
object bottom == table top
```

The object starts in intentional zero-gap support contact with the table.

A historical real failure occurred during LIFT after ATTACH because MoveIt detected:

```text
pick_object <-> table
```

as collision.

Correct semantic fix:

```text
ATTACH
→ temporarily allow pick_object <-> table
→ LIFT
→ restore normal collision checking
```

Do not “fix” this primarily by moving the object upward by an arbitrary epsilon.

`touch_links` already handles intended gripper/object contact.

---

## 6. Structured arm-stage foundation

The code defines:

```python
@dataclass
class StageResult:
    success: bool
    stage: str
    failure_type: str
    detail: str
```

The shared `run_arm_stage(...)` owns the common arm-motion flow:

```text
joint target
→ RobotState
→ current start state
→ goal state
→ MoveIt planning
→ trajectory execution
→ inspect execution status
→ StageResult
```

Current important failure categories include:

- `PLAN_FAILED`
- `EXECUTION_FAILED`

Do not teach these incorrectly:

- Planning failure is not automatically “software failure”.
- Geometric unreachability / IK infeasibility normally appears on the planning side.
- Controller rejection / tracking / execution problems appear on execution side.
- Robot-state problems can influence both.

---

## 7. Day26 completed work — exact architectural result

All six arm-motion stages now use `run_arm_stage()`.

Current structure:

```text
PREGRASP
pregrasp_joint_positions
→ run_arm_stage()
→ pregrasp_result

GRASP
grasp_joint_positions
→ run_arm_stage()
→ grasp_result

LIFT
pregrasp_joint_positions
→ run_arm_stage()
→ lift_result

PREPLACE
preplace_joint_positions
→ run_arm_stage()
→ preplace_result

PLACE
place_joint_positions
→ run_arm_stage()
→ place_result

RETREAT
preplace_joint_positions
→ run_arm_stage()
→ retreat_result
```

Status:

```text
PREGRASP ✅ migrated + runtime verified
GRASP    ✅ migrated + runtime verified
LIFT     ✅ migrated + runtime verified
PREPLACE ✅ migrated + runtime verified
PLACE    ✅ migrated + runtime verified
RETREAT  ✅ migrated + runtime verified
```

Target reuse is intentional:

```text
LIFT:
GRASP low position
→ pregrasp_joint_positions

RETREAT:
PLACE low position
→ OPEN / DETACH
→ preplace_joint_positions
```

---

## 8. LIFT special logic

LIFT is intentionally not identical to other stages because it has stage-specific Planning Scene semantics.

Correct order:

```text
pick_object <-> table = ALLOWED
        ↓
run_arm_stage(LIFT)
        ↓
pick_object <-> table = NOT ALLOWED
        ↓
inspect lift_result / task policy
```

The restore to `NOT ALLOWED` must happen before failure abort / later task-policy handling.

Reason:

```text
LIFT fails
→ environment cleanup must still happen
```

Do not move this collision-semantic behavior into generic `run_arm_stage()`.

Key Day26 lesson:

> Common motion behavior belongs in the common motion function; stage-specific task semantics stay in the task/stage layer.

---

## 9. Temporary compatibility RobotState variables were removed

During migration, these were temporarily retained because legacy stages depended on them:

```text
pregrasp_joint_state
preplace_joint_state
```

After LIFT and RETREAT migration, both became unused and were deleted.

A final grep:

```bash
grep -n "pregrasp_joint_state\|preplace_joint_state" \
src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py
```

returned no output.

The latest remote code was also checked after the Day26 push:

- all six `stage_name="..."` calls are present;
- `pregrasp_joint_state` is absent;
- `preplace_joint_state` is absent;
- `set_allowed_collision(...)` is still present.

Do not recreate these compatibility variables unless a new real dependency requires them.

---

## 10. Day26 verification evidence

After final cleanup:

```bash
python3 -m py_compile \
src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py
```

passed with no output.

Then:

```bash
colcon build --packages-select moveit_6dof_demos
```

passed.

Then a full Pick & Place run passed.

Final runtime tail included:

```text
Place 执行状态：SUCCEEDED
Place 执行成功 ✅
PLACE OPEN ✅
pick_object detach 消息已发布 ✅
Retreat Joint Goal 规划成功，开始执行...
Retreat 执行状态：SUCCEEDED
Retreat 执行成功 ✅
完整 Pick & Place 执行成功 ✅
process has finished cleanly
```

Therefore Day26 is:

```text
CODED ✅
SYNTAX VERIFIED ✅
BUILT ✅
RUNTIME VERIFIED ✅
```

---

## 11. Git state / important commits

The Day26 source commit is:

```text
3029568 day26: unify arm stages with structured execution
```

Before it, the local benchmark commit is:

```text
128c40d day25: add pick and place benchmark runner
```

The user pushed both commits to remote `main` successfully on 2026-09-30.

The push advanced remote:

```text
182ac2f..3029568  main -> main
```

This documentation update is a later commit on top of `3029568`, so a future GPT must still verify the actual current HEAD rather than hard-code this SHA.

At the time immediately before this docs update, the user's local working tree had one intentionally untracked path:

```text
?? ../artifacts/
```

Do not use `git add .` casually.

---

## 12. Benchmark status

`tools/run_pick_benchmark.py` is tracked from:

```text
128c40d day25: add pick and place benchmark runner
```

Capabilities already tested:

- launch Pick & Place automatically;
- stream output to terminal;
- create unique logs;
- classify PASS / FAIL;
- classify historical LIFT planning failure as `PLAN_FAILED`;
- classify startup package failure as `PACKAGE_ERROR`;
- append one CSV row per run;
- support `--runs N`;
- collect structured per-run results;
- print batch summary.

Formal 3-run smoke test:

```text
Runs: 3
PASS: 3
FAIL: 0
Success Rate: 100.0%
```

User decision:

> Do not spend time on a 20-run benchmark now. Prioritize the mainline.

---

## 13. Controller / launch reminder

A previous attempt to launch `pick_demo.launch.py` without the needed controller/demo infrastructure reached:

```text
等待 gripper_controller：OPEN...
gripper_controller 不可用
```

Do not interpret that as a Pick & Place logic bug.

If it happens again:

- inspect the controller/demo launch state;
- do not immediately edit motion code.

---

## 14. Exact Day27 boundary

After Day26, the low-level arm-motion layer already reports structured results.

Example:

```python
pregrasp_result = run_arm_stage(...)
```

The outer task layer still does:

```python
if not pregrasp_result.success:
    print(...)
    os._exit(1)
```

So the architecture is currently:

```text
run_arm_stage()
= diagnoses / reports what happened

main()
= currently makes only one task decision:
  ABORT
```

This is exactly where Day27 begins.

At Day26 end, `pick_demo.py` contained 10 direct `os._exit(1)` sites.

Conceptually they fall into three groups:

```text
A. startup / infrastructure failure

B. gripper-action failure
   OPEN / CLOSED / PLACE OPEN

C. six arm StageResult failures
   PREGRASP
   GRASP
   LIFT
   PREPLACE
   PLACE
   RETREAT
```

Do **not** globally replace all `os._exit(1)`.

The arm stages already have `StageResult`.
The gripper and startup paths are not yet modeled in exactly the same way.

---

## 15. Day27 goal — Failure Handling / Task State

The user already understands the high-level goal as:

```text
以前：
每个阶段报错
→ os._exit(1)

现在想要：
每个阶段报错
→ structured result
→ recovery / decision layer
→ decide what to do
```

More precise architecture:

```text
Task Stage
↓
run_arm_stage()
↓
StageResult
↓
Task Policy
├── RETRY
├── RECOVER
├── RESET
└── ABORT
```

Separation:

```text
run_arm_stage()
= report facts

task-level policy
= decide next action
```

Low-level motion should not decide that the entire Pick & Place must terminate just because planning failed.

---

## 16. Day27 recommended atomic sequence

Do not build a large state machine in one edit.

### Step 0 — Git reality check

Before editing:

```bash
git fetch origin
git status -sb
git log --oneline --decorate --graph -6
```

If this documentation commit was made remotely after the user's Day26 push, the user's local branch may simply need:

```bash
git pull --ff-only
```

Verify before running it.

### Step 1 — inspect only PREGRASP failure path

Start with:

```text
pregrasp_result
→ if not success
→ current os._exit(1)
```

Explain that this is already the task-policy boundary.

Do not modify all six stages yet.

### Step 2 — introduce an explicit task-decision concept

A likely minimal concept:

```text
TaskAction
├── ABORT
├── RETRY
└── RECOVER
```

Potentially add `RESET` later when its semantics are concrete.

The first refactor should preserve current behavior:

```text
StageResult
→ Task Policy
→ ABORT
```

This gives architecture without changing robot behavior yet.

### Step 3 — centralize task decision while preserving behavior

Goal:

```text
StageResult
→ one task-level decision function
→ existing ABORT behavior
```

Then verify:

```text
py_compile
→ build
→ runtime equivalence
```

### Step 4 — add bounded retry to one safe failure type

Only after Step 3 is stable.

Likely first experiment:

```text
PLAN_FAILED
→ retry planning once
→ if still failed, ABORT
```

No infinite retry loops.

Do not automatically retry every `EXECUTION_FAILED`.

### Step 5 — later expand policy

Possible later semantics:

```text
PLAN_FAILED
→ bounded replan

EXECUTION_FAILED
→ inspect / recover robot state before retry

scene inconsistency
→ scene reset

unrecoverable failure
→ abort
```

### Step 6 — preserve LIFT cleanup

Whatever retry/recovery design is introduced:

```text
pick_object <-> table
```

temporary collision allowance must still be restored correctly.

Do not reintroduce the historical LIFT cleanup bug.

### Step 7 — only after arm policy is stable

Then decide whether to bring:

- gripper failures;
- startup failures;
- Planning Scene failures;

into a unified task-failure model.

Do not mix all categories in the first Day27 edit.

---

## 17. What NOT to do next

Do not:

- jump directly to Pose-driven manipulation;
- jump to camera / perception;
- jump to MuJoCo;
- add a giant retry/recovery state machine in one patch;
- globally remove all `os._exit(1)`;
- mix gripper/startup failures into arm policy immediately;
- remove or bypass LIFT collision cleanup;
- reintroduce deleted compatibility RobotState variables;
- spend time on a 20-run benchmark;
- assume local and remote Git state are synchronized without checking.

---

## 18. Recommended first response from a new GPT

After reading the master plan, this handoff, and the actual latest code, a new GPT should say approximately:

```text
Day26 is complete:
all six arm-motion stages use run_arm_stage() and return StageResult,
and the final full Pick & Place run passed after compatibility-state cleanup.

We are now at Failure Handling / Task State.

First I will verify local vs origin/main.
Then Day27 will start with PREGRASP only:
we will introduce an explicit task-level decision boundary while initially
preserving the current ABORT behavior.
```

Then continue one atomic step at a time.

---

## 19. Later milestones after Day27

Only after Failure Handling / Task State is stable:

```text
Failure Handling / Task State
↓
Pose-driven manipulation
↓
dynamic object pose
↓
fake perception
↓
camera frame / TF
↓
camera geometry / PnP
↓
hand-eye calibration foundation
↓
MuJoCo tabletop
↓
robot data / benchmark
↓
LeRobot
↓
ACT
↓
Diffusion Policy
↓
LIBERO / robustness
↓
VLA
```

---

## 20. Day26 one-sentence summary

> Day26 converted all six arm-motion stages from duplicated inline MoveIt planning/execution code into the shared `run_arm_stage()` + `StageResult` architecture, preserved LIFT-specific collision semantics, removed temporary compatibility `RobotState` variables, and runtime-verified the complete Pick & Place task after cleanup.
