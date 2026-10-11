# Java面经＋手撕算法＋SQL训练（2026-10-11基线）

所有题目当前NOT_ATTEMPTED，无个人完成/练习时长证明；只概述面经，不能全文转载他人帖子。资料：牛客2025-09美团 https://www.nowcoder.com/discuss/801106192650043392 、Soul https://www.nowcoder.com/discuss/792085502886154240 、双非硕快手 https://www.nowcoder.com/discuss/793217447137447936 、美团秋招 https://www.nowcoder.com/discuss/792870676636901376 、牛客2025 Java手撕 https://www.nowcoder.com/discuss/739401539588042752 、JavaGuide2026 https://javaguide.cn/interview-preparation/backend-interview-plan.html 。

## 高频备考分层
- P0：Java集合/HashMap/ConcurrentHashMap、线程池/基本锁、Spring IoC/AOP/事务、MySQL索引/MVCC/事务/慢SQL、Redis类型/TTL/持久化/缓存一致性、Linux/HTTP/TCP、项目架构和真实问题复现。
- P1：JVM G1/GC、线程安全、SQL死锁、分布式基础、RabbitMQ幂等（若项目使用）、SQL优化；AI项目若写简历则必须能解释RAG准确率与工具权限。
- 项目面试回答链：“真实业务场景→本人改动→为什么这样设计→失败场景→日志和测试证据→未解决限制”，不编造并发量或所谓线上指标。

## 原创训练目录（首批）
| 编号 | 题型/原型 | 本次练习要求 | 状态 |
|---|---|---|---|
| ALG01 | LC1两数之和 | HashMap复杂度/重复数据 | NOT_ATTEMPTED |
| ALG02 | LC3无重复最长子串 | 滑动窗口/边界 | NOT_ATTEMPTED |
| ALG03 | LC206反转链表 | 自定义Node和Java main/ACM输入 | NOT_ATTEMPTED |
| ALG04 | LC21合并有序链表 | 空链表/不同长度 | NOT_ATTEMPTED |
| ALG05 | LC102层序遍历 | BFS/队列 | NOT_ATTEMPTED |
| ALG06 | LC103锯齿形层序 | 动态层序顺序 | NOT_ATTEMPTED |
| ALG07 | LC704二分查找 | 左右界与越界 | NOT_ATTEMPTED |
| ALG08 | LC200岛屿数量 | DFS/BFS/网格边界 | NOT_ATTEMPTED |
| ALG09 | LC70爬楼梯 | DP/空间优化 | NOT_ATTEMPTED |
| SQL01 | 按部门分组求人数且筛出大于3人的部门 | SQL文件、建表/测试数据、GROUP BY/HAVING | NOT_ATTEMPTED |

## 训练与评判
每周技术块内3题Java算法/1题SQL起步、每周一次项目追问（5—10分钟）；Java独立限时每题20—35分钟，保留源文件、JUnit或main测试、空/重复/常规边界、时间空间复杂度、真实用时；不看题解独立通过才PASS，提示后PASS单列，WRONG/TIMEOUT/NOT_ATTEMPTED不造假。先学LeetCode方法签名，再练真实机考要求的Scanner/BufferedReader输入输出。错误点当天最多一次补救，下一工作日T+1和约一周T+7另设情境复测，不能出现8小时无限补题。2027-06前扩展到约60—90道精选题是可调整的个人训练目标，非求职通过保证。算法/SQL与行测/申论分开记录。

GitHub建议在新Java独立仓库存algo、sql、interview-notes和匿名真实运行输出；当前未创建代码/仓库。