# Embodied AI / Robot Manipulation Master Plan

> 用途：这是本仓库的长期“总纲 / 新对话入口文档”。
>
> 新的 GPT 在开始指导前，必须先读本文件，再通过 GitHub connector 读取 `main` 最新代码和最近提交；不能把本文中记录的某个 commit 当成永久最新状态。
>
> 本文负责回答四件事：
> 1. 用户是谁、目标是什么；
> 2. 为什么当前路线这样安排；
> 3. GitHub 当前项目在整个年度路线中处于什么位置；
> 4. GPT 应该如何根据真实代码进度和最新招聘需求，滚动规划未来 4 周。

---

# 1. 用户背景与长期目标

## 1.1 学业与时间窗口

用户目前是计算机技术方向研究生，处于研二阶段，导师方向为具身智能（Embodied AI）。

长期就业目标不是纯大模型/NLP，而是：

**机器人 Manipulation / 具身智能 / Robot Learning / 工业视觉与机器人应用相关岗位。**

主要作品集建设窗口：

**2026-09 ～ 2027-08**

目标是在这一年内形成：

- 可公开；
- 可复现；
- 可量化；
- 可演示；
- 能讲清楚系统设计和失败原因；

的 GitHub 机器人作品集，为后续实习和秋招准备。

核心原则：

> 不追求“学过很多框架”，而追求“能够完成一条真实的机器人 Manipulation 技术链，并证明它为什么有效、哪里会失败、怎么改进”。

---

# 2. 当前计算环境与硬件边界

主力电脑：

- Windows 11
- AMD Ryzen 7 8845HS，8C/16T
- 约 32 GB 物理内存，系统当前可见约 27.8 GB
- 1 TB NVMe SSD
- Radeon 780M 核显
- 当前没有可用 NVIDIA CUDA 环境
- `nvidia-smi` 不可用

开发方式：

- Windows 11
- WSL2
- Ubuntu 24.04
- ROS2 Jazzy
- VS Code / Git / Python / C++

因此年度路线固定采用：

```text
本地电脑
├── ROS2
├── TF2
├── URDF / Xacro
├── MoveIt2
├── 机器人学基础
├── OpenCV / Camera Geometry / Calibration
├── MuJoCo 轻量仿真
├── 数据处理 / Benchmark
└── 工程代码 / GitHub

云 GPU
├── ACT 训练
├── Diffusion Policy
├── LIBERO 重型实验
├── VLA / SmolVLA / OpenVLA
├── 大规模 imitation learning / RL
└── Isaac Sim / Isaac Lab 等 GPU 依赖较强任务
```

不要把以下内容设为本机必须条件：

- Isaac Sim 本地完整部署；
- Isaac Lab 本地大规模 RL；
- 本地训练大型 VLA；
- 本地重型视觉大模型训练。

当某项热门技术明显依赖 NVIDIA GPU 时，应优先给出：

- MuJoCo；
- Colab；
- 云 GPU；
- Hugging Face Jobs；
- 其他按需 GPU 实例；

等替代路线，而不是让用户长期折腾本机兼容问题。

---

# 3. 目标岗位画像：2026-09 招聘信号校准

本路线必须参考招聘市场，但不能因为一两周热点频繁换方向。

2026 年 8～9 月观察到的具身智能 / 机器人岗位中，反复出现以下能力组合：

## A. 机器人底座能力

高频项：

- Linux / Ubuntu
- Python
- C++
- ROS / ROS2
- MoveIt / MoveIt2
- 机器人运动学
- 坐标变换 / SE(3)
- 运动规划
- 轨迹生成
- ros2_control / 真机接口
- 机械臂 Manipulation

结论：

**ROS2 + MoveIt2 + Robot Kinematics 仍然是主线底座，不能因为 VLA 热度跳过。**

## B. Robot Learning / VLA

高频项：

- PyTorch
- Imitation Learning
- ACT
- Diffusion Policy
- VLA / VLM
- RL
- World Model
- Action Chunk
- 真机部署

结论：

后半段必须进入 Robot Learning，但顺序应是：

```text
机器人系统
→ 数据
→ evaluation
→ imitation learning
→ diffusion policy
→ benchmark
→ VLA
```

而不是直接从 ROS2 跳到大模型。

## C. Data / Evaluation / Failure Analysis

近期招聘信号明显加强：

- 机器人数据采集；
- 数据清洗；
- 多模态对齐；
- episode / trajectory 数据；
- 离线评测；
- 真机验证；
- failure case 分析；
- 数据闭环；
- benchmark；
- 回归测试。

因此从 2026-09 起，项目必须逐渐从：

```text
“Demo 跑通”
```

升级为：

```text
“可以重复实验、统计成功率、分类失败原因、形成改进闭环”
```

这部分是长期作品集的重要差异化资产。

## D. Simulation / Sim2Real

常见要求包括：

- MuJoCo
- Isaac Sim / Isaac Lab
- Gazebo
- Webots
- PyBullet
- Sim2Real

用户当前没有 NVIDIA CUDA，因此：

**本地优先 MuJoCo，Isaac 系列安排在云端或以后有 NVIDIA 工作站时。**

## E. 工程落地

岗位不只看论文模型，还反复要求：

- 仿真到真机；
- 系统集成；
- 调试；
- C++ / Python 工程；
- SDK；
- latency / stability；
- 版本管理；
- benchmark；
- 可复现开源项目。

因此 GitHub 不应该只是“学习笔记”，而应逐步变成：

**工程能力 + 实验能力 + 机器人学习能力的证据库。**

---

# 4. 总体技术主线

长期主线保持：

```text
ROS2
↓
TF2 / SE(3)
↓
URDF / Xacro
↓
ros2_control
↓
MoveIt2
↓
IK / Planning / Execution
↓
Planning Scene
↓
Gripper
↓
Attach / Detach
↓
Pick & Place
↓
Failure Handling / Task State
↓
Pose-driven Manipulation
↓
Camera / TF / Calibration
↓
MuJoCo
↓
Robot Data / Benchmark
↓
LeRobot Dataset
↓
ACT
↓
Diffusion Policy
↓
LIBERO / Robustness
↓
VLA
↓
云端大型实验
```

辅助但不能忽略：

- C++
- Linux
- Git
- OpenCV
- NumPy
- PyTorch
- HDF5 / Parquet 等数据格式
- 数学：线性代数、刚体变换、运动学、优化基础

---

# 5. 年度路线：2026-09 ～ 2027-08

这不是死日历。

每个月末都要根据：

1. GitHub 实际进度；
2. 真实运行结果；
3. 招聘需求连续多周变化；
4. 用户时间投入；

进行校准。

只有当某种招聘需求持续多周明显变化时，才允许调整年度主线。

---

## Phase 1｜2026-09 ～ 2026-10
## Robot Manipulation Foundations

目标：

把“固定脚本式 Pick & Place”升级为：

**Robust + Pose-driven + Measurable Manipulation Pipeline**

重点：

- Failure Handling
- Task State
- Scene Reset
- Planning / Execution failure 区分
- 动态 Object Pose
- Pose → IK → Planning
- Fake Perception
- Camera Frame
- TF
- Camera Geometry
- PnP
- Hand-Eye Calibration 基础
- MuJoCo tabletop
- 最小 benchmark

阶段产物：

- 稳定 Pick & Place
- Failure log
- CSV benchmark
- Camera → TF → Base manipulation demo
- MuJoCo manipulation demo
- README / GIF / Architecture Diagram

---

## Phase 2｜2026-11 ～ 2026-12
## Robot Data + Imitation Learning Foundation

目标：

从“机器人会执行”进入：

**机器人会产生和消费 demonstration data。**

重点：

- Observation / Action / State
- Trajectory / Episode
- Dataset schema
- LeRobot Dataset
- HDF5 / Parquet
- 数据读取、可视化和统计
- Teleoperation 概念
- Behavior Cloning
- ACT
- offline evaluation

ACT 可以云 GPU 训练。

不要一开始追求很大模型。

阶段产物：

- 一个可解释的数据集分析 notebook / script
- 一个小型 imitation learning 实验
- ACT baseline
- train / val / eval 指标
- failure cases

---

## Phase 3｜2027-01 ～ 2027-02
## Diffusion Policy + Benchmark

目标：

真正进入现代 Robot Learning。

重点：

- Diffusion Policy
- action horizon
- observation horizon
- action chunk
- image / proprioception conditioning
- policy evaluation
- multi-seed experiments
- success rate
- robustness

推荐环境：

- MuJoCo
- robomimic
- LIBERO（必要时云端）

这一阶段不要只复现论文数字。

必须开始加入自己的实验问题。

优先考虑：

- viewpoint perturbation
- camera perturbation
- pose noise
- object location shift
- observation noise

阶段产物：

- ACT vs Diffusion Policy 对比
- 一个 robustness benchmark
- 表格 / 曲线 / failure taxonomy
- 完整实验说明

---

## Phase 4｜2027-03 ～ 2027-04
## LIBERO + Generalization + VLA Understanding

目标：

进入具身智能 benchmark 和 VLA，但仍以“理解 + 小规模实验”为主。

重点：

- LIBERO
- long-horizon tasks
- task generalization
- language-conditioned manipulation
- VLA architecture
- OpenVLA / SmolVLA / π 系模型的思想
- token / action representation
- VLM → Action
- policy inference pipeline

大型训练：

优先云 GPU。

阶段产物：

- LIBERO benchmark 实验
- VLA paper / code architecture notes
- 至少一个可运行 inference / evaluation pipeline
- 不要求本地训练大模型

---

## Phase 5｜2027-05 ～ 2027-06
## Flagship Project

目标：

从多个学习 Demo 收敛成一个招聘作品。

建议主项目定位：

**Robust Vision-Guided Manipulation Benchmark**

可能包含：

```text
Perception
↓
TF / Calibration
↓
Planning Scene
↓
Manipulation
↓
Policy
↓
Evaluation
↓
Failure Analysis
↓
Data Loop
```

结合用户已有工业视觉 / 动态抓取经验时，可以逐渐加入：

- conveyor / moving object
- timestamp alignment
- motion compensation
- dynamic pick
- visual calibration

但不要为了“复杂”破坏可复现性。

阶段产物必须包括：

- architecture
- setup
- reproducible commands
- benchmark
- ablation / comparison
- demo video
- failure cases
- known limitations

---

## Phase 6｜2027-07 ～ 2027-08
## 求职作品集与面试收口

目标：

把学习成果翻译成岗位语言。

重点：

- GitHub README 重构
- 项目 Demo 视频
- 技术报告
- 简历 bullet
- 面试讲解
- C++ / ROS2 / TF / MoveIt 复习
- Robot Learning 原理复习
- 系统排障案例整理
- LeetCode / 基础编程按岗位需要补齐

最终至少形成：

### Project A
Robot Manipulation Foundations

证明：

- ROS2
- TF
- MoveIt2
- Planning Scene
- ros2_control
- Gripper
- Failure Handling
- Pose-driven Manipulation
- Camera / Calibration

### Project B
Robot Learning / Benchmark

证明：

- Robot Data
- ACT
- Diffusion Policy
- Evaluation
- Robustness
- LIBERO / MuJoCo
- Failure Analysis

如进度足够，再形成：

### Project C
Flagship Vision-Guided Manipulation

把前两者整合成招聘主项目。

不要创建大量只有几十行代码的小仓库。

---

# 6. 当前 GitHub 项目

仓库：

`xchhhh22222/robot-manipulation-foundations`

默认分支：

`main`

## 6.1 新 GPT 的强制 GitHub 阅读流程

每次新的 GPT 接手本项目时：

### Step 1

确认：

- `main` HEAD SHA
- 最近 5～10 个 commit
- 最近修改的文件

### Step 2

至少检查：

- `README.md`
- 当前主任务脚本
- 对应 launch
- URDF / Xacro
- SRDF
- ros2_control config
- MoveIt controller config
- package.xml
- setup.py / CMakeLists.txt（按包类型）

如果 HEAD 已进入新的阶段，则继续读取新阶段核心文件。

### Step 3

根据“实际源码 + 用户真实运行日志”判断当前能力。

优先级：

```text
真实 terminal / runtime evidence
>
GitHub 最新代码
>
本文件中的历史进度
>
聊天里的旧计划
```

绝对不要因为本文件写着“已经完成”就跳过运行证据。

---

# 7. 当前代码快照（2026-09-28）

本文件创建时，确认的 `main` HEAD：

`42e69d9adc82e9fc523e9491fcecfcf4e2c58e2c`

Commit：

`complete day24 pick and place execution`

当时已经完成：

- ROS2 基础
- Topic / Service / Action
- TF
- URDF / Xacro
- simple_6dof_arm
- MoveIt2 配置
- Joint Goal
- Pose / IK
- Cartesian 基础
- Planning Scene
- Collision-aware planning
- ros2_control trajectory execution
- 双指 gripper
- Attach / Detach
- Pick
- Pick & Place

当时 `pick_demo.py` 已实现：

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

该系统使用 MoveIt + ros2_control FakeSystem / Mock Hardware。

它已经是真正的软件执行链，但不是物理动力学抓取。

当前主要缺口：

- failure detection 有了，但 recovery 不完整；
- 没有成熟 Task State；
- 多处 joint target 仍硬编码；
- object pose 还不是完整外部输入；
- camera → TF → manipulation 尚未接通；
- 缺少 benchmark / success rate；
- README 与实际能力仍需要同步；
- package metadata / dependency 仍需逐步工程化。

新 GPT 必须重新检查当前 HEAD，因为这些缺口未来会变化。

---

# 8. 四周滚动规划机制

不要一次规划未来一年每天做什么。

长期方向由本文件负责。

具体执行使用：

**4 周滚动窗口。**

每周结束进行一次复盘。

---

## 每周复盘必须包含

### A. GitHub Reality Check

重新检查：

- main HEAD
- 本周 commits
- 本周关键 diff
- README
- 新增 scripts / launch / configs

### B. Runtime Evidence

区分：

`CODED`

与：

`VERIFIED`

验证优先：

- terminal logs
- `/joint_states`
- controller state
- Action server
- TF
- Planning Scene
- execution status
- benchmark CSV

不要只根据 RViz “看起来成功”。

### C. Concept Check

随机检查本周 2～3 个概念。

要求用户自己解释：

- 为什么需要；
- 输入输出是什么；
- 在系统哪一层；
- 常见 failure 是什么。

### D. Failure Review

记录：

```text
Symptom
→ Hypothesis
→ Verification
→ Root Cause
→ Fix
→ Regression Test
```

失败记录不是垃圾信息，而是作品集资产。

### E. Portfolio Review

检查：

- README 是否过时
- 是否有 Demo GIF / Video
- 是否有 Architecture
- 是否有 benchmark
- 是否有 failure cases
- 是否有 known limitations
- 是否存在应该删除的临时代码
- 是否存在复制粘贴而未抽象的逻辑

### F. Recruitment Calibration

每周扫描：

- 主流招聘平台；
- 具身智能公司官网；
- 近期校招 / 实习岗位；
- 主流开源框架变化。

只统计与以下目标相关岗位：

- Manipulation
- Robot Learning
- Embodied AI
- Motion Planning / Control
- VLA / Generalist Robot Policy
- Robot Data / Evaluation

每周输出：

1. 岗位方向热度；
2. 技术栈变化；
3. 用户当前差距；
4. 是否值得调整未来四周。

**只有连续多周出现明显变化，才修改年度路线。**

---

# 9. 新 GPT 每次应该输出什么

当用户说：

“继续学习”
“帮我规划下周”
“看一下我现在进度”
“按招聘需求校准”

GPT 应先完成 GitHub Reality Check，然后输出：

## 1. 当前真实里程碑

用一句话说明：

**现在已经真正做到什么。**

## 2. 当前最大三个 Gap

不能列十几个方向。

只选择最影响下一阶段的三个。

## 3. 与招聘需求的对应关系

说明当前项目已经覆盖哪些招聘能力，还缺哪些。

## 4. 未来四周路线

每周必须包含：

- 核心问题
- 学习主题
- 项目修改
- 验收标准
- GitHub 产物
- 本地 / Linux / 云 GPU 标签

## 5. 本周只做什么

最终收敛成不超过 3 个任务。

## 6. 下一原子步骤

如果开始动手教学，每次只推进一个小步骤。

---

# 10. 教学协议

GPT 的角色不是“代写项目”。

而是：

**机器人 / 具身智能导师 + 工程 Reviewer + 作品集 Reviewer。**

每增加一个重要机制，都必须解释：

1. 为什么需要；
2. 当前代码哪里需要；
3. 输入是什么；
4. 输出是什么；
5. 它属于系统哪一层；
6. 怎么验证；
7. 如何留下 GitHub 证据。

---

## Debug 协议

严格遵循：

```text
一个假设
↓
一个验证
↓
一个修改
```

不要一次修改五个地方。

当用户贴真实日志时：

**日志优先于猜测。**

---

## 命令协议

给 shell / ROS / Git 命令时，说明：

- 应在哪个目录运行；
- 命令做什么；
- 是否修改文件；
- 是否运行机器人；
- 是否影响 Git；
- 是否上传远程。

编辑源码默认：

`code <absolute-path>`

不要默认使用 nano。

---

# 11. GitHub 作品集标准

一个学习点只有在至少产生以下一种资产后，才算真正进入作品集：

- runnable code
- unit / integration test
- benchmark
- CSV / metrics
- plot
- GIF / video
- architecture diagram
- technical note
- failure analysis
- reproducible commands

优先：

**一个持续长大的高质量项目**

而不是：

**很多零散 Demo repo。**

README 不应该只写：

“我学了 ROS2 / MoveIt / VLA”。

应该回答：

- 这个项目解决什么问题？
- 架构是什么？
- 如何运行？
- 成功率多少？
- 在什么条件下失败？
- 做过哪些实验？
- 我做了哪些设计选择？
- 下一步是什么？

---

# 12. 招聘能力矩阵

后续 GPT 可用这个矩阵检查用户进度。

| 能力 | 目标级别 |
|---|---|
| Linux / Git | 熟练 |
| Python | 熟练 |
| C++ | 能独立开发机器人模块 |
| ROS2 | 熟练 |
| TF2 / SE(3) | 熟练 |
| URDF / Xacro | 能独立建模 |
| MoveIt2 | 熟练 |
| ros2_control | 理解并能调试 |
| Kinematics / IK | 理解并能应用 |
| Motion Planning | 理解算法 + 工程接口 |
| Planning Scene | 熟练 |
| Gripper / Manipulation | 能构建完整任务 |
| Camera Geometry | 熟练基础 |
| Calibration / Hand-Eye | 能完成实验与误差分析 |
| OpenCV / PnP | 能实现 |
| MuJoCo | 能独立搭建 manipulation experiment |
| Robot Dataset | 能读写、统计、设计 schema |
| LeRobot | 能使用 Dataset / Policy / Eval |
| ACT | 能训练与评测 |
| Diffusion Policy | 能复现并做对比实验 |
| LIBERO | 能跑 benchmark |
| Robustness | 能设计 perturbation experiment |
| VLA | 理解架构并完成云端小规模实验 |
| Evaluation | 能构建 success / failure metrics |
| Failure Analysis | 能系统分类和回归验证 |

---

# 13. 优先级判断规则

当技术太多时，按照以下顺序决策：

### P0：当前项目阻塞项

例如：

- controller 不稳定；
- TF 错；
- Planning Scene 错；
- 状态不一致。

先修。

### P1：招聘高频 + 作品集可见

例如：

- ROS2
- MoveIt2
- Manipulation
- C++
- Robot Data
- Evaluation
- Failure Analysis

优先。

### P2：能够形成下一阶段接口

例如：

- Camera → Pose
- Pose → Planning
- Dataset → Policy

优先。

### P3：热门但当前无法形成产物

例如：

- 本地大型 VLA
- 本地 Isaac 重型训练
- 纯追论文名词

暂缓。

---

# 14. 当前不应走偏的方向

不要把路线变成：

```text
看到新模型
→ clone
→ 跑 checkpoint
→ README 写“已掌握”
```

也不要变成纯 ROS 工程师路线。

正确目标是：

```text
Robot System
+
Manipulation
+
Perception
+
Data
+
Policy
+
Evaluation
```

最终形成完整 Embodied AI 能力链。

---

# 15. 给新 GPT 的第一条执行指令

如果你是刚接手这个项目的新 GPT：

1. 先读完本文件；
2. 使用 GitHub connector 获取 `xchhhh22222/robot-manipulation-foundations` 的 `main` HEAD；
3. 读取最近 commits；
4. 阅读当前阶段关键代码；
5. 不要默认当前仍停留在本文 2026-09-28 的快照；
6. 根据真实代码说明当前做到哪里；
7. 再扫描最近招聘需求；
8. 将招聘变化与年度路线比较；
9. 如果没有连续多周明显变化，不修改年度主线；
10. 给出未来四周滚动计划；
11. 把第一周拆成 2～3 个可验收任务；
12. 真正开始教学时，只给下一个原子步骤。

最终目标始终是：

> **让用户真正掌握完整机器人 Manipulation / Embodied AI 技术链，并把学习过程沉淀成面向招聘的、可公开、可复现、可量化、可演示的 GitHub 作品集。**
