# 主动间隔复习队列｜2026-10-10 建立

> 只基于用户已提交的答案/概念、GitHub main 已归档事实形成排期。状态不是通知送达证明；实际复习是否完成需要后续用户回答验证。日期按 Asia/Shanghai；及时阅读 [主动导师协议](PROACTIVE_TUTOR_PROTOCOL.md) 与 [LEARNING_STATE](LEARNING_STATE.md)。

## 一、当前待触发复习卡（不要把待办误写成PASS）

| review_id | track | topic | learned_at | T+1 / 隔日 | T+7 | 目前状态 | 已有可核验证据 | 下次必须问什么 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REV-20261010-GROWTH | 行测/企业测评资料分析 | 基期、现期、增长率、百分点 | 2026-10-10 | **2026-10-11** | **2026-10-17** | `PLANNED`，到期转`DUE`，不可先判PASS | 原题 JOB-20261010-005 答A、答案B（WRONG）；R1答B正确（仅答案PASS）；随后口述150→195以150作基期正确；用时未知 | T+1 给**新数据**原创题，请先答再讲；T+7 换应用情境并要求解释分母、限时90秒 |
| REV-20261010-ROS2-ACTION | ROS2技术 | Topic/Service/Action区分，Action Goal/Feedback/Result与FJT轨迹执行 | 2026-10-10（复习队列建卡日；实际首次学习日期未完整确认） | **2026-10-11（建议主动复述，不代表昨天刚学会）** | **2026-10-17** | `PLANNED`，掌握程度`NOT_MEASURED` | 用户曾运行 `ros2 interface show control_msgs/action/FollowJointTrajectory`；已查Action端点及服务端；未证实发出goal或成功执行 | T+1 请用自己的话区分一次Action目标请求、持续feedback、最终result，并说明为何server存在≠goal成功；T+7 让用户按新故障情境选择只读诊断命令 |
| REV-DAY28-EXECUTION | ROS2主课/实操 | Day28 Pose Goal规划→轨迹提取→实际执行验证 | `DATE_UNCONFIRMED`（当前步骤运行成果未提交） | **尚不能计算** | **尚不能计算** | `NOT_ATTEMPTED`（执行成功验证） | GitHub `docs/CURRENT_HANDOFF.md` 和 `LEARNING_STATE.md` 记载语法检查、规划/Action端点查询；远端不能证明新片段运行或轨迹执行 | 等用户提供本地日志或Git状态；先验证trajectory inspection与运行结果，再安排T+1/T+7 |

**注意**：2026-10-10的 `JOB-20261010-005-R1` 已经答过，不能在10-11原封不动拿来当新题。没有实测计时不可填“90秒达标”。这是一份计划，不是对当日结果的预判。

## 二、固定触发日历与八周观察

| 触发 | 日期或规则 | 当日动作 | 完成条件 |
| --- | --- | --- | --- |
| 日常检查 | 每个自然日的每日追踪任务/新对话出现时 | 先查上表是否到期，若到期最多抛出1道未答微练习；平时仍抓真实JD和公考内容 | 有用户当次回答才更新状态 |
| 第一周周复盘 | **2026-10-11（周日）** | 对未完成卡、贵州公共部门与一线研发JD分轨、技术运行证据、错题做短复盘；不虚构已有投递 | 明确下周1–3个可验证动作 |
| 此后周复盘 | 2026-10-18起每周日 | 复习队列、技术分支的14天可运行证据、真实JD与投递漏斗 | 写事实、问题、一个调整、验收条件 |
| 8周中途检查 | **2026-10-24、11-07、11-21**（建议时间点） | 看ROS2可运行证据/岗位匹配/真实练习错误，不满足时调整最小目标 | 依据实际证据写CONTINUE / NARROW / PAUSE（没有证据则PENDING） |
| 月度策略复盘 | **每月1日** | 招聘地域/学校初筛与简历A/D证据；应急金按**3–6个月必要支出**轻提醒 | 不假设用户已给出支出、储蓄 |
| 八周阶段复盘 | **2026-12-04** | 汇总实验可复现性、JD证据、求职路径及时间投入与生活可持续性 | 按观察证据判断继续/收窄/暂停 |

## 三、记录更新模板（新对话/定时任务回写）

```markdown
### REV-YYYYMMDD-XXXX | YYYY-MM-DD
- track:
- learned_at: YYYY-MM-DD / DATE_UNCONFIRMED
- learned_from: source link / Git commit / user statement
- question_id:
- user_answer_or_log: 已匿名脱敏的具体证据 / NOT_ATTEMPTED
- actual_duration: 秒 / NOT_MEASURED
- fact: 不臆测
- root_cause_hypothesis: ...（如不确定标 UNVERIFIED）
- single_adjustment: ...
- verification: ...
- review_due: YYYY-MM-DD
- status: PLANNED / DUE / PASS / WRONG / REVIEW / BLOCKED
- last_updated: YYYY-MM-DD
```

若当日没有真实学习/作答，就保留原始 due，不因为完成了一期招聘日报而自动后移复习。更新前重新读取当前远端文件、避免覆盖其他对话的更新；任何私密实际工资/资产、实名报考、公司资料和原始保密面试信息不得写入。


## 2026-10-10 更新：阶段概念PASS，复习日期不变

- REV-20261010-GROWTH 新的下降变式问分母（2027=200，2028=180）：用户答200，**基期识别 PASS**；当堂具体计算−10%由教师示范，不代表用户独立完成。
- 用户提出结束重复讲解、进入下一个知识点（言语理解）。**卡片仍为 PLANNED**：T+1 2026-10-11、T+7 2026-10-17，不提前PASS，不改复习日；复习应换新数字、新情境，验证限时和百分点。
