# 开发环境一键启动 — DEV_STARTUP

> 更新时间：2026-10-09
>
> 项目：`xchhhh22222/robot-manipulation-foundations`
>
> 本文解决「重启电脑 / 新开 WSL 终端后，如何快速回到机器人项目」的问题。学习进度、已完成实验和下一步任务以 [CURRENT_HANDOFF.md](CURRENT_HANDOFF.md) 为准；长期路线以 [EMBODIED_AI_MASTER_PLAN.md](EMBODIED_AI_MASTER_PLAN.md) 为准。

## 1. 每次打开 WSL：只需一个命令

在 **Windows 的 WSL2 Ubuntu 终端**输入：

```bash
rosdev
```

已在 WSL 用户 `wanxincheng` 的 `~/.bashrc` 中配置并实测通过（2026-10-09）。成功时显示：

```text
✅ ROS2 Jazzy 环境已加载
📁 当前工作空间：/home/wanxincheng/robotics/robot-manipulation-foundations/ros2_ws

📌 Git 状态：
## main...origin/main
?? ../artifacts/
```

Git 输出会随实际提交/文件变化。`?? ../artifacts/` 代表仓库根目录下的未跟踪实验目录，**不是报错，不要随意删除，也不要用 `git add .` 把它提交进去**。

`rosdev` **不会自动启动** `demo.launch.py`、MoveIt2、控制器、RViz 或训练任务。它只负责准备当前 shell 的开发环境。

## 2. rosdev 的配置（仅用于新 WSL 环境或恢复配置）

`~/.bashrc` 中的函数如下。**现有 WSL 已经配置成功，无需重复追加。**

```bash
# Robot Development Environment
rosdev() {
    local WS="$HOME/robotics/robot-manipulation-foundations/ros2_ws"

    if [ ! -f "$WS/install/setup.bash" ]; then
        echo "❌ ROS2 工作空间不存在或尚未构建"
        return 1
    fi

    cd "$WS" || return 1

    source /opt/ros/jazzy/setup.bash || return 1
    source "$WS/install/setup.bash" || return 1

    echo "✅ ROS2 Jazzy 环境已加载"
    echo "📁 当前工作空间：$PWD"
    echo ""
    echo "📌 Git 状态："
    git status -sb
}
```

函数适用于 **Bash**。新建配置后运行 `source ~/.bashrc`，再运行 `rosdev`。之所以用函数而不是普通 `bash some_script.sh`，是为了让 `cd` 和 `source` 的效果留在当前终端。

如果函数不存在，可先运行 `type rosdev`，确认 `~/.bashrc` 是否加载。运行 `pwd` 可检查当前工作目录。

## 3. 手动启动方式（rosdev 失效时）

```bash
cd ~/robotics/robot-manipulation-foundations/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
pwd
git status -sb
```

注意：

- `/home/wanxincheng` 是用户主目录，**不是** `ros2_ws`。
- 在 `~` 下直接运行 `source install/setup.bash` 会找错路径。
- 在 `ros2_ws` 目录下源码路径从 `src/` 开始，**不要再多写一个 `ros2_ws/`**。
- 项目 Python 源码绝对路径：
  `/home/wanxincheng/robotics/robot-manipulation-foundations/ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py`
- 若在 Windows VS Code 打开 WSL 文件，应使用实际 WSL 路径/WSL 扩展或相应的 `\\wsl.localhost\<发行版名称>\...` UNC 路径，确保编辑的是 24KB 左右的真实源码文件，而非误创建的空白文件。

## 4. 写完代码后：检查、构建

确保已经在 `ros2_ws`，然后：

```bash
python3 -m py_compile src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py
colcon build --packages-select moveit_6dof_demos
source install/setup.bash
```

- `py_compile` 只检查 Python 语法。
- `colcon build` 验证 ROS2 功能包的构建过程。
- 以上两项**都不能**代替 Pick & Place 运行或失败分支测试。
- WSL 曾因 `--symlink-install` 的 Python 包元数据兼容问题构建失败；目前这个功能包使用常规 `colcon build`。

## 5. 需要仿真时：两个终端

仅在要做运行验证时启动。每个**新开的 WSL 终端**先执行 `rosdev`。

**终端 A — 启动演示环境（保持运行）：**

```bash
rosdev
ros2 launch simple_6dof_moveit_config demo.launch.py
```

**终端 B — 检查控制器，执行 Pick & Place：**

```bash
rosdev
ros2 control list_controllers
ros2 launch moveit_6dof_demos pick_demo.launch.py
```

`arm_controller`、`joint_state_broadcaster`、`gripper_controller` 均应为 `active` 再进行完整运行测试。如果 `ros2 control list_controllers` 一直等待 `/controller_manager/list_controllers`，先检查终端 A 的演示服务是否启动；**不要首先修改运动代码**。

## 6. Git 与两套 Ubuntu 环境

目前的职责分工：

| 环境 | 主要任务 |
| --- | --- |
| Windows + WSL2 Ubuntu 24.04 | 日常编辑、学习、ROS2/MoveIt2 小规模验证、Git 提交 |
| 原生 Ubuntu 24.04.5 + NVIDIA RTX 4090 | 较重的仿真、实验、模型训练 |
| GitHub `main` | 两套环境同步的代码基线 |

在任何一台机器上同步代码前，先到**仓库根目录**：

```bash
cd ~/robotics/robot-manipulation-foundations
git status -sb
git fetch origin
git status -sb
```

如果确认没有冲突性的本地修改且只需快进，再使用：

```bash
git merge --ff-only origin/main
```

不要无条件 `git reset --hard`；不要删除或默认提交 `artifacts/`。远端文档由 ChatGPT/GitHub 连接器直接更新时，WSL 不会自动收到更新，仍需 `fetch`/快进。

## 7. 新对话 / Codex 预热顺序

1. 读取 `docs/EMBODIED_AI_MASTER_PLAN.md`（长期路线）。
2. 读取 `docs/CURRENT_HANDOFF.md`，特别是最新的日程/阶段追加章节（当前进度和已验证事实）。
3. 查 `git status -sb` 和最近提交，再读最新的 `pick_demo.py`，不要仅凭文档猜代码。
4. 指出已完成的里程碑、尚未实现的部分；**一次只给一个原子步骤**（理解 → 修改 → 验证）。

截至 2026-10-09：Day27 PREGRASP 有限规划重试已经实现、模拟测试和一次性故障注入验证过；`RECOVER` 尚未实现。用户已开始 Day28 Pose-driven Manipulation，从 Object Pose → Pre-grasp Pose → IK → MoveIt2 Pose Goal 逐步学习。Day28 的源码修改是否提交，以实际 Git 为准。
