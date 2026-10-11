# 2028届 Java后端＋AI应用工程路线（2026-10-11）

> 已进行2025—2026牛客真实面经、JavaGuide2026学习路线、Spring官方版本与LangChain4j对照。这是**规划已完成、实际Java/Redis项目未开始**，并非用户确认最终工作时间与技术掌握。就业定位：贵州运营商/行业数字化研发，省外成熟ToB软件；贵州公考省考事业编并行。导师具身研究与毕业责任保留，不再把纯VLA算法与重复Demo交付作为求职主线。用户明确重视生活质量，常态20:00后下班与996原则排除，未知工时写UNKNOWN。

## 1. 外部资料与事实边界
- JavaGuide 2026学习路线（基础→SQL/Spring→Redis→项目→高阶）https://javaguide.cn/roadmap/java-roadmap.html
- JavaGuide 2026后端面试（项目真实性、Java/MySQL/Redis、问题追问）https://javaguide.cn/interview-preparation/backend-interview-plan.html
- 牛客美团2025-09 Java实习：线程池、JVM/GC、MySQL索引/事务、Redis、Spring、OS https://www.nowcoder.com/discuss/801106192650043392
- 牛客2025-09 Soul面经：树Z字遍历、手撕SQL、Spring、MySQL、Redis、Linux https://www.nowcoder.com/discuss/792085502886154240
- 牛客2025-09双非硕快手Java面试：项目/Redis/MQ/索引深问、反转链表需自行处理输入输出 https://www.nowcoder.com/discuss/793217447137447936
- 牛客2025-09美团后端：实习/线程池/数据库/二叉树手撕 https://www.nowcoder.com/discuss/792870676636901376
- 牛客2026面经整理（个人总结、非抽样统计）https://www.nowcoder.com/discuss/864594486704291840
- Spring Boot 3.5官方支持Java17以上，Java21适用 https://docs.spring.io/spring-boot/3.5/system-requirements.html
- Spring Boot 4.0官方新版本 https://docs.spring.io/spring-boot/4.0/system-requirements.html
- Spring AI 2.0.0 GA（2026-06-12）https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/
- Spring AI 1.1兼容Spring Boot3.4/3.5 https://docs.spring.io/spring-ai/reference/1.1-SNAPSHOT/getting-started.html
- LangChain4j支持RAG、Tools及Spring Boot https://github.com/langchain4j/langchain4j
- JavaGuide 2026 Java/Go转AI应用仍优先工程化 https://javaguide.cn/roadmap/backend-to-ai-agent-roadmap.html
所有牛客帖为单人/评论样本，不能据此算录用率或所有企业考题频次。2027届/2026届JD仅供技能参照，不代表2028可投。

## 2. 融合后的技术栈：核心、增补、AI、未来机器人

| 级别 | 技术 | 具体学习与取舍 |
|---|---|---|
| P0核心 | Java21、OOP/集合/泛型/异常/并发基础、Maven、Git、Linux | 实际编译和运行、基础题限时独立复现 |
| P0业务 | Spring Boot3.5维护线、REST、IoC/AOP/事务、MyBatis、MySQL/SQL、JUnit5/Mockito | 单体分层API、有实测数据库和异常测试；MyBatis为默认，不否定JPA |
| P1工程 | Redis cache-aside、TTL、缓存失效与回源、鉴权、SQL EXPLAIN、Docker Compose、日志、GitHub Actions | 项目有需求后逐项接入，记录引入前后真实性能和失败恢复 |
| P1可选 | RabbitMQ一次异步可靠投递实验 | 仅有真实通知/任务队列需求时才上；Kafka/RocketMQ先了解用途，不同时堆三种 |
| P2 AI应用 | 后端集成一个LLM API、RAG引用或工具调用、评测/权限/成本/回退；Spring AI或LangChain4j二选一 | 后端可独立运行后再接AI；AI框架不替代Spring Boot，拒绝套壳聊天Demo |
| 延后 | Spring Cloud微服务、K8s、分库分表、ElasticSearch、大量前端框架、裸机MCU/VLA模型训练 | 秋招前不主动开新坑；如真实目标JD证明必要再复评 |
| 长线能力 | HTTP/日志/事件/模型服务与ROS2适配器 | 导师研究保留，未来有机器人系统/部署岗位时补专项技能；不能自动视为VLA算法胜任 |

选择Java21+Spring Boot3.5成熟线是稳健起点；Spring Boot4/AI2新功能已存在但可能需适配，项目初期不为追新版重构。版本以正式实施时官方兼容表确认。

## 3. 12周可执行路线（用户尚未开展Java代码）
| 周期 | 任务 | 验收证据 |
|---|---|---|
| W1—W2 | 核验Java/Javac/Maven环境；Java集合/OOP/异常/基础算法 | 实际命令输出、最小Java程序/测试、2题独立代码 |
| W3—W4 | SQL/JDBC概念与MySQL索引，Spring Boot接口骨架 | REST健康检查、SQL建表/查询、JUnit样例 |
| W5—W6 | 工单/事件创建查询/状态变更、MyBatis、事务/错误处理 | 真实curl/接口测试、合法/非法用例、commit SHA |
| W7—W8 | Redis缓存/失效、SQL EXPLAIN、Docker部署 | 可复现cache miss/hit/TTL/故障回源、SQL测量 |
| W9—W10 | 并发/乐观锁/幂等、日志和GitHub Actions；MQ有必要才上 | 并发重复请求、失败恢复、CI/测试日志 |
| W11—W12 | 增加一项AI检索/工单建议，至少10—20例原创评价集 | 结果有引用、离线回退、错误分析、延迟成本日志、项目面试解释 |

项目规格见 JAVA_AI_PROJECT_SPEC_2026-10-11.md；手撕/面经题见 JAVA_AI_INTERVIEW_PRACTICE_2026-10-11.md。
用户原工作日行测60—120分钟约20题、周末无常规任务、导师具身研究义务不变。建议每周3个60—90分钟Java技术块，算法/SQL嵌入其中，不要求另外无限加时。

## 4. 市场雷达：稳定主线、定向小改
已创建**每周五北京时间约16:00**“Java与AI招聘雷达”，首次2026-10-16，关注真实2028届JD、牛客新面经、Spring/Java官方发布。每周最多3条变化和一项建议；单篇热帖不构成换Spring理由。调整主框架必须同时有跨周多家目标企业JD证据、实测项目收益、可承担迁移成本；2027年1月第一工作周按12周成果复盘。当前ChatGPT通知是否实际弹送取决于用户设置，不以任务创建保证推送成功。

## 5. 时间线及下一入口
2026-12可构建单体后端（实际可用以进度为准），2027-03-31实习就绪，2027-06-30校招准备就绪，2027-07起2028届秋招。**下一次唯一原子检查**：在计划使用的Windows PowerShell或Ubuntu/WSL执行 java -version；javac -version；mvn -version；git --version 并回传真实输出。未收到之前标ENV_UNVERIFIED。