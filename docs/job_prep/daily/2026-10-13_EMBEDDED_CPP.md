# 2026-10-13（周二）｜嵌入式 C++ M1 Day2 与 ROS2 Day28 实际记录

> **状态：C++ 函数与三组测试 RUN_VERIFIED；GDB F11 / Shift+F11 截图证实；ROS2 工作树 READ_ONLY_AUDITED。** 基于本日用户终端回贴、VS Code 截图和文字回复。**学习时长未独立计时**，120/30 分钟是预算而非实耗。详见 [当日执行教案](2026-10-13_EXECUTION_PLAN.md)。用户本地源文件和 WSL 未提交代码并未因此上传 GitHub。

## 1. Linux / C++ 项目：函数与运行

- Ubuntu VS Code 工作目录 `/home/wxc/embedded-linux-learning`；`pwd` 回传该目录，`ls -l temperature_demo.cpp` 证实昨日源码仍在（240 字节，10月12日）。
- 新练习文件 `temperature_function.cpp`，学生先在函数体内写 `return raw = raw / 10.0;`；教师指出 `raw` 是 `int`，赋值会先截断小数、再转换为函数返回的 `double`。学生还提出把参数 `raw` 改为 `double` 的可行性，理解会避免该次截断，但设备原始寄存器值宜保持整数。后续截图可见更正为 `return raw / 10.0;`。
- 学生独立提交 `double temperature = rawToCelsius(raw);`，正确调用并保存返回值；截图可见 `main()` 内 `int raw = 318;` 以及 `std::cout` 输出温度。
- 用户回贴实际编译命令，无报错或警告可见：
  ```bash
  g++ -std=c++17 -Wall -Wextra -Wpedantic -g -O0 temperature_function.cpp -o temperature_function
  ./temperature_function
  ```
- 用户实际逐次重新编译并运行（前一次318也有完整编译运行日志）：
  ```text
  Temperature: 31.8 C
  Temperature: 0 C
  Temperature: -5.5 C
  ```
  对应原始数值 `318`、`0`、`-55`，三组 **RUN_PASS 3/3**。证明这三个样本通过，不等于大范围边界或生产级可靠性已验证。

## 2. VS Code + GDB 调试证据

- F5 启动 C/C++ g++ 调试，截图：第13行 `double temperature = rawToCelsius(raw);` 有断点及黄色箭头；Locals `raw = 318`；调用尚未结束前 `temperature` 可能显示未初始化的无效数值。
- 学生按 F11 后截图：黄色箭头停在函数体第6行 `return raw / 10.0;`；Locals `raw = 318`；Call Stack 上层为 `rawToCelsius(int raw)`、下层为 `main()`。**STEP_INTO_SCREENSHOT_VERIFIED**。
- 学生按 Shift+F11 后截图：Call Stack 仅剩 `main()`，显示 `$ReturnValue = 31.80000...`，黄色箭头仍在第13行；`temperature` 尚未完成赋值、仍显示未初始化值。**STEP_OUT_SCREENSHOT_VERIFIED**，但不能误称此时赋值完成。
- 进一步按一次 F10 后学生回复「变回来了」，上下文对应 `temperature` 恢复为正确温度，**ASSIGNMENT_AFTER_STEP_USER_REPORTED**，未提供此最后步骤的截图。并未专门通过重启调试演示“从函数调用处一次F10跳过”的独立对照，不能把键位概念解释判为完全自主背诵。
- 学生解释提炼函数「这样可以方便调用吧也可以做检测方便」，**REUSE_TESTABILITY_EXPLANATION_PASS**。关于 `int raw`、`double` 类型转换需要后续不同情境迁移核验；今天首次 `return raw =...` 的纠错是教师指导，不标独立无提示全通过。

## 3. ROS2 Day28 安全只读检查（不同主机/工作区）

用户在 `wanxincheng@xiaocheng:~/robotics/robot-manipulation-foundations` 实际回贴：

```text
$ git status -sb
## main...origin/main
 M ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py
?? artifacts/
$ git diff --stat
 ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py | 54 +++++++++++++++++++++++++++++++++++++++++++++++++---
 1 file changed, 51 insertions(+), 3 deletions(-)
$ git branch --show-current
main
```

- **WORKTREE_AUDIT_VERIFIED**：`main` 分支，`pick_demo.py` 未提交修改（+51/-3），`artifacts/` 未跟踪，必须保留。状态显示 `main...origin/main`，不代表已 fetch 验证最新远端。
- 当次只读，无 `git add` / `commit` / `pull` / `reset` / `clean` / ROS launch。本次**未检查54行具体语义**，不能推断它们一定就是轨迹终点代码。
- Day28既有 Pose Goal probe 此前 PASS；轨迹终点提取此前仅语法检查、**RUNTIME_NOT_VERIFIED**。留到2026-10-15（周四）ROS 深度课在保护工作区前提下继续，勿覆盖本地代码和 `artifacts/`。

## 4. 课程与其他轨道边界

- 2026-10-13行测由另一个对话单独结案并同步：[行测日志](2026-10-13_XINGCE.md)，常规 Q057—Q076 **20题17对3错**，实际用时 NOT_MEASURED；不在技术记录里重复记题或改变错题状态。
- 本对话没有2026-10-13具身小论文**真实文献阅读、实验或科研日志**证据；**RESEARCH_NOT_REPORTED**，不可写 PASS。
- 项目路线不变：Linux C/C++ 工业设备监控为主、ROS2辅助、科研/行测各自独立。**本地 `temperature_function.cpp` 未通过本次GitHub记录同步到仓库；本次上传的是文字化学习证据。**

## 5. 下一工作日：2026-10-14（周三）低思考度执行入口

技术/GPT协作预算 **180分钟：C/C++ 与 Linux 150分钟 + GitHub/等待/复盘30分钟**（含聊天时间，非真实实耗承诺）。不要重复昨日三样本/GDB教学。
1. **0—15min** 打开 Ubuntu VS Code `~/embedded-linux-learning` 的 `temperature_function.cpp`，仅回顾函数参数与返回值。快速让学生独立判断 `int raw`、`double`、`raw/10.0` 的关系，围绕昨日赋值截断做一次新情境迁移（不刷重复题）。
2. **15—60min** 将程序由写死 `raw=318` 改成**终端输入原始温度值**，由学生本人添加 `std::cin >> raw;` 或小型输入接口，理解输入、类型和函数调用；先给骨架、本人写关键语句。
3. **60—105min** 至少测试一个正常整数、0、负数及一个无效输入，学习 `if (!(std::cin >> raw))` 的意义，区分数值边界与输入格式错误。按能力决定是否加入简单范围校验，**不抢进CMake/网络/STM32**。
4. **105—140min** 完成一次GDB断点查看读入值及函数入参，做到在新输入下观察和简述变量传递；如时间不足优先真实编译输出与可解释代码。
5. **140—150min** 本人用几句话复述输入→校验→转换→输出数据链，记录仍未掌握之处。
6. **150—180min** 集中核对回贴的源码/编译结果、更新当天记录与GitHub（不能提前标PASS）。
7. 行测仍单独上限120min，2026-10-14新情境复习Q057工程余时、Q065百分点单位、Q071增长贡献率并正常继续新题，**不要重复2026-10-13已结案题**；科研独立120min，先验证2篇原始论文或实验基线并形成最小可证伪假设，未上手不算成果。
8. **2026-10-15周四** ROS Day28 深度课先复核WSL本地差异、保护未提交文件，再验证轨迹终点提取功能；保留 `artifacts/`。**2026-10-19周一** 在真实新函数中T+7复测GDB三快捷键，今天的T+1截图已通过。

**下一句开场：**「继续10月14日C++输入与验证，在 Ubuntu VS Code 打开 `temperature_function.cpp`，先根据你现有代码判断怎样把写死的318改为用户输入。每轮一个小操作，真实编译后再记录。」不得伪造当天已执行的内容。
