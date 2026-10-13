# 机器人项目下一对话入口（V4.2）

这是只增加交接文档的独立审核分支，尚未合并。原main及已有工程分支不改。先读 [中文交接](control/HANDOFF.md)，再核验源main源码与最新实验事实。

远端代码停在Day27；Day28本地Pose Goal规划与轨迹提取分开记录，不能因旧标题CURRENT就认为都已上传或执行成功。机器人项目、ROS2、MoveIt及科研实验继续属于本库。

本次源main核验提交：`b117beba0e9290c31c8edb75f53d456a74aabdcc`；核验时间：2026-10-13T15:53:30+08:00。当前学习权威仍是本库原docs/job_prep/LEARNING_STATE.md、SPACED_REVIEW_QUEUE.md和NEXT_CHAT_HANDOFF.md；项目事实以实际源码、实验记录及docs/CURRENT_HANDOFF.md为依据。本入口只展示来源摘要，不取代原状态。

短接手指令：先核验main和用户原机器人工作树，保护未提交pick_demo.py与artifacts；核对Day28轨迹提取真实差异后再设计一次受控构建/运行。Pose规划通过不等于轨迹执行通过；环境由具体ROS2实验决定，不要求全局换操作系统。
