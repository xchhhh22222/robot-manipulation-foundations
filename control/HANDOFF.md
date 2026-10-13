# 机器人项目中文交接（V4.2）

## 最新有效事实与历史边界

- 源main：`b117beba0e9290c31c8edb75f53d456a74aabdcc`。当前pick_demo.py没有DAY28_POSE_PROBE，也没有get_robot_trajectory_msg，不能把本地Day28功能称为远端已保存。
- 远端保留Day27结构化StageResult/TaskAction与PREGRASP有界重试。原构建文件、配置、实验记录及全部既有工程分支不因本轮改变。
- [原交接第22节](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/CURRENT_HANDOFF.md#L982-L1015)记录本地Day28 Pose Goal规划PASS且probe没有执行轨迹；后加轨迹终点提取只有语法检查，运行仍待验。第21节“不要进入Day28”及早期Day26起点属于已被第22节覆盖的历史。
- [10月13日只读工作树记录](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/job_prep/daily/2026-10-13_EMBEDDED_CPP.md#L31-L49)记载另一工作副本pick_demo.py+51/-3未提交、artifacts未跟踪；本轮未取得原改动，不推断其完整功能，不上传私人源码。
- 实际运行记录与代码保存分开；本轮只建立接手文件，没有新构建、实验或科研成果，不新增PASS。

## 当前任务与未知项

下一最小动作：在用户明确的原工作区只读核对分支、提交、工作树与差异，保护pick_demo.py/artifacts；与main比较后再审阅轨迹提取片段。未看到真实差异前不重置、不盲目pull、不把不明文件加入提交。先有代码证据，再在适合该ROS2实验的环境做一次构建/运行；规划probe保持无实际执行，验证限制必须说明。

工程状态：远端Day27代码已保存；本地Day28部分历史文字证据存在，完整未提交代码与新运行结果待核。知识掌握：不能从规划PASS推导轨迹执行/全部故障恢复熟练；RECOVER流程未见验收。科研论文/新实验本轮无新成果证据。

## 权威、来源与下次指令

当前唯一学习状态权威仍在 `xchhhh22222/robot-manipulation-foundations` main：
- [学习状态](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/job_prep/LEARNING_STATE.md)
- [复习队列](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/job_prep/SPACED_REVIEW_QUEUE.md)
- [原交接记录](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/job_prep/NEXT_CHAT_HANDOFF.md)

本次实际核验源提交：`b117beba0e9290c31c8edb75f53d456a74aabdcc`；时间：2026-10-13T15:53:30+08:00。固定提交供追溯；每次接手须核验源main最新版本。新领域索引和交接为只读摘要，不代表权威切换。

项目事实还需读取[实际pick_demo.py](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/ros2_ws/src/moveit_6dof_demos/moveit_6dof_demos/pick_demo.py)、[原项目交接](https://github.com/xchhhh22222/robot-manipulation-foundations/blob/b117beba0e9290c31c8edb75f53d456a74aabdcc/docs/CURRENT_HANDOFF.md)和对应实验配置。通用C++学习归技术库；机器人代码不复制到职业总控或技术库。

短接手指令：我接手机器人Day28，请先核验main和原工作树，保留未提交差异，区分历史Pose规划PASS、语法检查、运行和执行；只推进一个有源码依据的最小验证，不强制改变其他路线或操作系统。

执行、证据核验、远端同步分别记录。学习与实验结束后先在授权的唯一归属位置保存真实日志及版本，回读核验，再更新总控引用；失败位置如实登记。合并、本地文件上传和学习权威切换需另行批准。
