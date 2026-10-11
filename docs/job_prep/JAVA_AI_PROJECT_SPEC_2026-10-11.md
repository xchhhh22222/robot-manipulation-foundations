# 就业项目规格：智能服务事件/工单与知识库平台（2026-10-11）

**这是一份设计稿，不代表Java程序、Redis实例或GitHub新仓库已经创建。** 适配运营商/行业数字化、成熟ToB软件，保留未来工业设备/ROS2事件接入能力，但不绑定真实机器人。数据全部自造、匿名，避免客户/实习商业数据上传。

## 最小架构
Java21、Spring Boot3.5稳定维护线、Maven、MyBatis、MySQL、JUnit5单体REST服务；早期只用curl/Postman或OpenAPI调用，不要求Vue全栈。逐步增加Redis cache-aside、Docker Compose、GitHub Actions。模块：api/、service/、repository/、infra/cache/、infra/ai/、tests/。核心表：incident、incident_event、knowledge_article，其他表按实需添加。基本端点：POST /incidents、GET /incidents/{id}、GET /incidents、PATCH /incidents/{id}/status。合法状态OPEN→ACKNOWLEDGED→RESOLVED→CLOSED，非法变更应返回明确错误并有单测。

## 七级能力验收
1. **V0 Java最小代码**：java/javac/mvn实际版本确认；最小编译程序与单测。
2. **V1 API＋MySQL**：查询/创建/状态变更、错误/异常测试，状态变更与incident_event记录使用事务；提供SQL脚本、请求与单测结果。
3. **V2 SQL性能**：多条件索引与EXPLAIN、真实查询规模/时间；不编“性能提高10倍”的虚假数据。
4. **V3 Redis缓存**：选热点事件详情或知识库，不把Redis当真实唯一存储。读取流程先查Redis，miss再MySQL并设置TTL，写库成功后删对应缓存键，验证回源/失效；说明短暂并发不一致风险；缓存不可用时降级MySQL；记录命中率与延迟的相同测试条件。不能盲目加缓存。
5. **V4并发/可靠性**：MySQL乐观锁version/重复提交幂等/错误日志/REST统一错误响应，人工注入异常；有明确异步通知需求时才引入RabbitMQ。
6. **V5 AI辅助**：给工单检索知识库建议故障原因并**提供证据引用和人工确认**；原始HTTP调用可行，选Spring AI/LangChain4j之一再优化RAG/工具编排；10—20条原创评测样本、引用有效性、错误建议、成本/延迟、禁用AI时后端仍可正常运行。默认不让LLM自动修改/关闭工单。
7. **V6十年具身可选**：若未来有招聘/研究需要，新建独立ROS2事件→HTTP adapter接入工单；Java后端不依赖真机，不能由此直接声称拥有VLA核心算法能力。

## GitHub真正交付
建议未来用户开始编码时创建**独立Java练习/业务代码仓库**（名称由用户决定），不把未运行代码堆在原robot-manipulation-foundations ROS2项目。正式文件应有README、src/main、src/test、SQL schema、deploy/compose.yaml、.env.example、.gitignore、docs/adr（技术取舍）、docs/evidence（命令、测试、失败修复日志）、.github/workflows/ci.yml。真实凭证、内网客户文档、手机号不入库。每个小任务需要Git SHA、实际运行和测试结果、GitHub fetch回读，未通过写PENDING_USER而非PASS。

未来换新框架只更新infra适配或实现模块，数据库/服务API/单测作为长期稳定资产。


## 2026-10-11 实习转Java与AI应用简历新增事实契约：从个人后端项目到可信Agent项目
- 工单/设备事件服务可以体现用户的运营商工业设备场景理解，但**只能使用本人设计的虚构设备事件、工单和知识文档**，不调用/复制当前实习单位内部生产资料。简历上项目须写“个人项目”，**不得声称在实习公司生产环境上线或曾维护其Java/Redis/Agent系统**。
- AI模块验收不仅是LLM聊天功能：知识库切分/索引/RAG引用、无依据拒答、只读工单工具、鉴权/参数白名单/工具执行审计、10—20条原创评测、工具拒绝越权与模型超时回退。禁止模型未经人工审核直接关闭/改写工单；指标真实测量，不能虚构。
- 完整从实习到J/JA双版本简历的证据边界和岗位JD见 [RESUME_AGENT_TRANSITION_2026-10-11.md](RESUME_AGENT_TRANSITION_2026-10-11.md)；实际Java代码仍未见本次运行证据，`PROJECT_PROPOSED`不变。
