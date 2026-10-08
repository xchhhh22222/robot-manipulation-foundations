# CURRENT HANDOFF — 2026-10-08 — Day27 PREGRASP Bounded Retry Verified

> Repository: `xchhhh22222/robot-manipulation-foundations`
>
> Current as of 2026-10-08: Day26 complete; Day27 PREGRASP bounded planning retry implemented and validated. Day27 recovery / broader task-state handling is NOT complete.
>
> A new GPT must **first read** `docs/EMBODIED_AI_MASTER_PLAN.md`, then verify the actual latest `main` state and read the latest `pick_demo.py`. Do not treat this handoff as a substitute for the real repository state.
>
> **Important:** Sections 14–20 retain the historical Day26→Day27 starting plan. For actual progress and the next task, read **Section 21 (2026-10-08 update)**.

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

The current milestone is **Day27: Failure Handling / Task State**. PREGRASP has a tested single-retry policy; the **next atomic learning topic is RECOVER semantics and state inspection for execution failures**, not Pose-driven manipulation or a wholesale refactor.

```text
StageResult → TaskAction policy → bounded PREGRASP retry  ✅
EXECUTION_FAILED → state inspection / safe RECOVER design  NEXT
Other stages, startup/gripper failures, RESET       NOT IMPLEMENTED
```

---

## 1. Repository / environment

Environment (updated 2026-10-08):

- **Main development:** Windows 11 + WSL2 Ubuntu 24.04. Edit with VS Code, study ROS2, run small tests, build, and commit from WSL.
- **Experiment / training host:** native Ubuntu 24.04.5 LTS desktop with NVIDIA RTX 4090; use for heavier MoveIt2 / simulation experiments and local GPU training.
- ROS2 Jazzy; each environment has its **own** workspace under `~/robotics/robot-manipulation-foundations/ros2_ws` and must build/source independently.
- Repository: `xchhhh22222/robot-manipulation-foundations`; branch: `main`. Use GitHub commits to synchronize WSL and native Ubuntu; **do not** assume either clone has pulled new commits.
- WSL development machine has Radeon 780M integrated GPU (no CUDA on that machine); do not confuse it with the separate native Ubuntu RTX 4090 host.
- Cloud GPU is optional if local GPU capacity is insufficient; no longer treat cloud GPU as the only training path.
- Current robot backend: mock `ros2_control GenericSystem` / mock hardware behavior.
- Native Ubuntu remote desktop was too laggy for frequent editing; SSH / remote command execution can be considered for experiments without requiring GUI interaction.

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

## 14. Exact Day27 boundary (historical state at Day26 end)

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

## 16. Day27 recommended atomic sequence (original plan; early steps now completed)

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

## 18. Recommended first response from a new GPT (historical Day26 snapshot; see §21 for current)

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

---

## 21. 2026-10-08 — Day27 PREGRASP bounded retry: implemented and verified

This section is the **current state of the project** and supersedes the historical Day26→Day27 starting instructions in Sections 14–18. Do not repeat already completed Day27 steps.

### 21.1 Git truth and environment transition

Confirmed GitHub \`main\` at the start of this update:

\`\`\`text
418b372 day27: add bounded pregrasp planning retry
cd23216 day27: introduce task action policy for pregrasp
327b217 fix: declare MoveItPy dependency and remove missing rviz path
b1d789b docs: update day26 current handoff
3029568 day26: unify arm stages with structured execution
\`\`\`

- Work originally continued on native Ubuntu, then moved back to **Windows + WSL2 as the primary development environment** because GUI remote access to native Ubuntu was laggy.
- \`327b217\` fixed native Ubuntu portability: declare the \`moveit_py\` runtime dependency, and remove a nonexistent \`rviz\` install directory from the description package.
- WSL initially remained at \`b1d789b\` with an untracked \`artifacts/\` directory; after \`git fetch origin\` and \`git merge --ff-only origin/main\`, WSL moved to \`cd23216\`. \`artifacts/\` was preserved.
- WSL then completed and pushed \`418b372\`. Source was syntax-checked, built, and runtime-verified in WSL.
- At the end of that push, \`main\` matched \`origin/main\`; \`artifacts/\` remained **untracked**. Never casually run \`git add .\` or remove that directory.
- **This documentation update itself creates a newer remote commit**. Any existing local clone, including WSL and native Ubuntu, must check \`git status -sb\` and fetch/fast-forward safely before editing further. Never assume \`418b372\` stays latest.

### 21.2 Exact task-policy implementation

Existing Day26 low-level result contract is unchanged:

\`\`\`python
@dataclass
class StageResult:
    success: bool
    stage: str
    failure_type: str
    detail: str
\`\`\`

Day27 added the task decision enum and policy:

\`\`\`python
class TaskAction(Enum):
    RETRY = "RETRY"
    RECOVER = "RECOVER"
    ABORT = "ABORT"

def decide_task_action(
    result: StageResult,
    retry_count: int = 0,
) -> TaskAction:
    if (
        result.failure_type == "PLAN_FAILED"
        and retry_count == 0
    ):
        return TaskAction.RETRY
    return TaskAction.ABORT
\`\`\`

\`RETRY\`, \`RECOVER\`, and \`ABORT\` here are **Python task-policy decisions**, not ROS2 Action interfaces. \`RECOVER\` is declared but **not implemented as an executor**. The current policy does not decide based on \`result.success\` because the caller only invokes it on failures.

Only **PREGRASP** has been rewired to an execution loop:

\`\`\`text
retry_count = 0
while:
  run_arm_stage(PREGRASP)
  ├─ success → break; continue with GRASP
  └─ failure → decide_task_action(result, retry_count)
       ├─ PLAN_FAILED, retry_count=0 → RETRY; increment; call run_arm_stage again
       ├─ another failure → ABORT via os._exit(1)
       └─ unsupported action → raise NotImplementedError
\`\`\`

Exactly one retry means **at most two total PREGRASP attempts**. Each call to \`run_arm_stage()\` calls \`arm.set_start_state_to_current_state()\` and \`arm.plan()\` again. This uses MoveIt's current **known** state; a real robot may still require freshness checks.

\`EXECUTION_FAILED\` is **not automatically retried**: execution may have moved the arm partially. Do not blindly re-execute it.

Other stages (GRASP / LIFT / PREPLACE / PLACE / RETREAT), gripper, and startup still use previous failure handling. Do not infer a general task-state machine from this limited implementation.

### 21.3 Verification evidence and limitations

Verified in WSL with ROS2 Jazzy and mock ros2_control controllers:

1. \`python3 -m py_compile src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py\` passed.
2. \`colcon build --packages-select moveit_6dof_demos\` passed.
3. Policy / mock-loop tests passed:
   - PLAN_FAILED on first attempt → RETRY, then simulated success → total calls 2, retries 1.
   - Two successive simulated PLAN_FAILED outcomes → RETRY then ABORT, total calls 2.
   - EXECUTION_FAILED with retry_count=0 → ABORT.
4. Regular full Pick & Place after adding the PREGRASP loop completed:
   \`Place SUCCEEDED\`, \`Retreat SUCCEEDED\`, \`完整 Pick & Place 执行成功 ✅\`, process finished cleanly.
5. **Controlled one-shot fault injection exercised the actual PREGRASP loop** using temporary environment flag \`DAY27_TEST_PREGRASP_FAIL_ONCE=1\`. First attempt returned a synthetic \`StageResult(PLAN_FAILED)\` *without calling MoveIt planning*; the next attempt used the real \`run_arm_stage()\`. Observed log:

   \`\`\`text
   [DAY27 TEST] 注入一次模拟 PLAN_FAILED
   PREGRASP 阶段失败：PLAN_FAILED | Day27 一次性故障注入测试
   PREGRASP 开始第 1 次重试
   开始规划 Pre-grasp Joint Goal...
   ...
   完整 Pick & Place 执行成功 ✅
   process has finished cleanly
   \`\`\`

6. Temporary fault-injection code was **removed** after the test. \`git diff --exit-code -- pick_demo.py\` returned clean relative to committed \`418b372\`; later GitHub source inspection confirmed the production loop has **no fault-injection branch**.

**What this proves:** the PREGRASP loop handles one synthetic planning failure and successfully re-enters genuine MoveIt planning/execution. **What it does not prove:** a natural real MoveIt planning failure recovering successfully, a real execution failure recovery, or the actual process-abort branch under live controllers. Do not overclaim coverage.

### 21.4 Immediate next work (continue Day27, not Day28)

1. Read latest Git state and \`pick_demo.py\`; if a clone is behind, inspect local changes and use a safe fast-forward. Preserve \`artifacts/\`.
2. Explain and design **RECOVER vs RETRY vs ABORT** for \`EXECUTION_FAILED\`: inspect actual/known arm state, controller status, whether movement partially occurred, and Planning Scene consistency before deciding any safe recovery.
3. Implement one minimal, explicitly bounded and testable recovery/state-inspection step **only after review**; avoid a large state machine or premature modifications to every stage.
4. Maintain LIFT's invariant: temporary \`pick_object ↔ table\` collision allowance must be restored before failure handling, even when LIFT fails.
5. Add deterministic tests and runtime verification for any new recovery code; log outcomes. Do not jump to Pose-driven manipulation before Failure Handling / Task State foundations are stable.

**Teaching protocol stays strict:** one hypothesis → one verification → one change. Explain why, verify using logs, and make at most one small code edit at a time.
