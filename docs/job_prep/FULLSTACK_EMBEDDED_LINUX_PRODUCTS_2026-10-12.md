# 2028届嵌入式Linux求职：完整开源产品二次开发候选与验收契约｜2026-10-12

> **用户最新纠偏：不接受把“工业通信边缘网关”这种通信骨架当完整毕业/求职项目；要真实前端、后端、业务流程、设备服务一体化的成品。希望借成熟开源系统合法二次开发、更换产品视觉和功能，亲自理解代码并能深入面试。** 本文是重新调研与候选设计（RESEARCH_COMPLETE / PRODUCT_CANDIDATE / USER_APPROVAL_PENDING），非项目已经开工，也没有创建项目代码、配置电脑或寄STM32板。保留每天工作日行测约20道、计划加入申论和Linux面经5题，但具体项目/面经新增训练尚未获明确开工批准。

## 1. 2026年完整现成产品实查

| 产品 | 当前有的真实产品功能 | 后端/前端及许可 | 求职适配与问题 |
|---|---|---|---|
| **FUXA** https://github.com/frangoteam/FUXA | 浏览器里的工业SCADA/HMI编辑器、实时可视化、Modbus TCP/RTU、MQTT、报警、历史数据采集、设备标签、支持Docker与Linux/ARM；有完整运行路径和文档 https://frangoteam.github.io/FUXA/ | **Node.js后台＋Angular前端；MIT**（原LICENSE必须依规定随衍生分发保留）。截至2026-10报告最新发行 v1.3.4 (2026-08)：https://github.com/frangoteam/FUXA/releases | **产品底座/界面二开首选候选**，但原生非C++，不能仅做换肤就称嵌入式Linux研发；须开发实质C/C++采集守护进程、协议状态机、日志/故障恢复，并证明自己对前后端业务功能的修改。项目已有2026年多项安全公告 https://github.com/frangoteam/FUXA/security ，应使用当时已修补并固定依赖版本，默认仅本地/测试网运行，禁止未经审计公网暴露。 |
| **EMQX Neuron** https://github.com/emqx/neuron + https://github.com/emqx/neuron-dashboard | C语言工业连接服务器、Modbus与MQTT驱动、HTTP接口、浏览器管理界面 | **C核心＋Vue旧Dashboard；核心/开放组件LGPLv3**，并有商业插件限制 https://docs.emqx.com/en/neuron/latest/introduction/license/license-policy.html | 与C/Linux更贴近，但官方明示Dashboard开源2.6.3 **停止开发维护**，不宜未经代码安全审查就作为最终UI底座；可做嵌软架构学习/备选代码参考。 |
| **ThingsBoard** https://github.com/thingsboard/thingsboard | 功能齐全的物联网设备管理、可视化、规则与远程管理 | Java后端＋Angular前端；**4.4及以上BUSL 1.1**（4.4以前版本另为Apache2） https://github.com/thingsboard/thingsboard/blob/master/README.md | 功能成熟，但核心以Java/大平台为主，与嵌软C/C++主线弱；BUSL对品牌/生产场景许可的限制增加直接整体二开门槛。当前**不推荐**“整体换皮当自己的”路线。 |

**特别纠错**：libmodbus 3.2.0 (2026-07) 是协议库而非完整工业产品，发布新版本不能证明选的成品值得做。可作为合法依赖，不是直接克隆换UI的应用原型。

## 2. 推荐的成品候选：工业设备智能监控与运维平台

**业务目标**：车间操作员通过Web添加设备、配置采集、实时监测、设备历史、报警确认/关闭、故障记录、后台服务健康与权限。完整链路：本人的模拟Modbus/未来STM32设备 → **本人C/C++ Linux采集与状态服务** → MQTT/受限API → **Web后端/存储/实时推送** → **自定义的Web管理前端**。依实际软件接口选型，不能先假设FUXA自带业务模块都适用。

**一条可验收操作剧本**：用户登录→新增模拟设备并配置点位→C++服务连接Modbus模拟器→采集数据并把设备状态与时序数据上报→Web显示趋势→断开设备网络→有离线告警/错误日志/重连节流→设备恢复→前端状态恢复，留下报警处理和历史追踪证据。每一段都需要代码/命令/自动化/手工测试记录。

**预计七个产品页面**：登录/权限、总览、设备列表与详情、采集点位与配置、实时/历史曲线、报警中心/处理记录、运行诊断/日志。页面设计可以全部自定义，不要求沿用FUXA视觉或完整代码，但**不能把依赖原有Node/Angular代码的能力标为本人原创C++**。

**Linux主角模块**：Linux C++17/20的设备进程、libmodbus或协议适配、超时/重连状态机、线程及有界队列、TCP/串口对接、结构化日志与诊断、权限约束、性能/CPU/RSS、ARM交叉构建。MQTT Broker/第三方协议库可复用，需记录许可和边界；历史库可以初期SQLite，后续按实测换更合适存储，不盲堆Kafka/Redis/分布式。

**实施方式二选一**：
- **方案F（低风险首选调查）**：先固定一个**安全修订过的FUXA版**验证其真正完整功能及可修改性，再合法fork保留MIT声明；自定义工业场景、Web视图和部分业务流程，开发单独可运行的C++ Linux边缘服务与状态/故障测试，通过MQTT或API集成。缺点：原有Web后端Node.js，C++模块需承担足够复杂度以匹配职位，不能谎称整个后端C++开发。
- **方案N（C底层为重点）**：沿Neuron C核心与现有Vue界面实际源码评估二开；若Dashboard停止维护导致投入很大，采用**独立小型Vue Web业务前端+本人C++后台**更诚实但工时增加。LGPLv3及商业功能边界必须另核。暂不直接定案。
- 可将FUXA当**产品功能、UI交互和业务场景参考**而用合法独立原创前后端构建另一完整产品；但这个方案更费时，不能假设12周能覆盖完整前后端＋ARM＋驱动＋RTOS。

**验收闸门**：必须（1）用原厂说明复现原产品部署及前后端功能；（2）确定许可证与当前安全公告（完整MIT notice或LGPL obligations；品牌商标另核）；（3）独立个人贡献计划明确具体代码模块；（4）能形成可演示端到端业务闭环；（5）用断联/错误数据/MQTT掉线/后端重启/越权等测试验证；（6）部署ARM或QEMU后才能自称嵌入式实际部署；（7）README写清“基于XX开源版本二次开发、第三方与我本人新增模块”，保留Git历史/可复现测试；实际无测试绝不吹QPS或成功率。

## 3. 二次开发与所谓“内化”的真实标准

允许合法改产品名称、视觉、功能并进行深度技术重构；不支持“只改Logo/颜色/目录/代码格式/变量名就隐去原作者，声称整个项目都是我从零开发”。开源许可证、版权声明及可能的商标/去品牌限制必须核实。最佳表达是**基于某成熟开源产品进行二次开发，我本人设计实现Linux C++设备通信/状态恢复/联动业务、独立部署与压力故障测试**。面试可逐行解释本人贡献以及上下游的工作原理；能够独立维护/解决故障才叫技能内化。FUXA官方还销售Pro版白标等高级特性，不能把商业Pro功能直接作为MIT开源代码使用。

## 4. 与最早的“一个骨架＋STM32项目”方案关系
- 之前[EMBEDDED_LINUX_PRESTART_MASTER_PLAN_2026-10-11.md](EMBEDDED_LINUX_PRESTART_MASTER_PLAN_2026-10-11.md)的`Modbus→MQTT headless edge gateway`降级为**新全栈产品的C++设备通信子模块候选**，不再独占“主项目”称号。
- 新完整产品是**单一主项目**（前端/后端/通信/日志/告警等），STM32板是后续真实设备端可选扩展，而不是并行再做第二套Web大平台。
- 工作量诚实估算：如果技术块每周仅约3×60—90分钟，12周可能只能做好真实可演示的MVP（且取决于源码难度）；完整产品+ARM和可靠性可延续到2027春季，不承诺一键fork改名即可毕业/过面。
- **开工闸门不变**：用户尚未批准具体最终项目、时间或环境配置。下一次先讨论FUXA/Neuron/原创全栈三种投入策略与哪一条最能证明Linux C/C++主技能；未经明确指示不得下载/改电脑、开新仓库或寄STM32板。
- 今天的行测Q037—Q041已发布但尚未得到用户作答，状态NOT_ATTEMPTED，不受项目改提议影响。工作日20题与循序加入申论/嵌软面经计划维持。

## 2026-10-12 源码级核验：用户明确希望Node.js后端换成Linux C++

**用户最新疑问**：能否把FUXA主要Node.js后端替换为自己开发的C++服务，在Linux（后续可为ARM）上运行，从而成为更有个人代码贡献的完整项目？**结论：可行，但不是语言自动转换，必须实现兼容API、实时消息和原有业务功能。重新编写的独立C++部分属于用户原创实现；保留/修改的MIT原版Angular或Node功能仍属于衍生代码，不能称整个仓库从零独立原创。** 整体项目在用户审核前仍为`DESIGN_CANDIDATE/PROJECT_NOT_STARTED`。

### 源码真实边界（直接核对frangoteam/FUXA公开仓库）
- `client/src/app/` 是Angular应用，有editor、device、alarms、users、fuxa-view、_services及其他业务模块，若保留它，就需要继续用前端JavaScript/TypeScript的工具链构建，并非系统绝对“100% C++”。
- `server/main.js` 创建Express和Socket.IO运行服务，`server/api/index.js` 涉及auth、users、projects、alarms、daq、reports、scheduler、scripts等API；`server/runtime/index.js`负责Socket.IO连接/业务事件；`server/runtime/devices/`包含Modbus、MQTT、S7、OPCUA、BACnet等设备驱动；`server/runtime/storage/`具有SQLite/Influx/QuestDB存储适配。资料：https://github.com/frangoteam/FUXA/tree/master/server 和 https://github.com/frangoteam/FUXA/tree/master/client 。
- 因此并非“所有JS换成CPP即完成”，**Socket.IO与标准WebSocket不是直接兼容协议**。可修改Angular Web端`_services`逐步换成普通WebSocket+REST，或者专门实现必要的Socket.IO兼容层；推荐前者更可控，但UI前端源码也要调整。
- FUXA源码MIT https://github.com/frangoteam/FUXA/blob/master/LICENSE ，衍生分发需保留著作权/许可文本；第三方依赖/素材/商标/Pro白标功能另核，不能以换Logo掩盖原代码作者。
- C++后台可考虑成熟Drogon框架 https://github.com/drogonframework/drogon （HTTP路由、WebSocket、鉴权过滤器、SQLite、ARM支持），设备通信libmodbus、paho-mqtt-cpp依其各自许可证引入，日志spdlog、单测GoogleTest为候选而非已经装好。

### 两个实施强度
**S1（更现实的主候选）：逐步替换**：在合法保留FUXA前端/临时Node基线的情况下，先运行原成品形成操作验收；新增独立Linux C++服务处理虚拟Modbus设备采集/断连/多线程与状态、REST/WebSocket的新增业务接口；重构前端若干数据服务指向新C++ API；逐步迁移设备配置/历史/告警/权限，一条业务链不再依赖Node时给出集成测试。最终做简历时如仍有Node，诚实写“双后端过渡/本人C++设备服务”，不能写“完全替代Node”。
**S2（高风险候选）：全部更换后端**：必须重建项目编辑器读写/报表/全部驱动/鉴权/脚本/调度/报警/DAQ历史与Node-RED等众多功能才可能保持FUXA全功能等价，超出当前秋招准备预算；可有意识**缩减成自有产品功能集**（设备列表/实时图表/报警/历史/权限），而不是追求FUXA所有功能兼容。精简后有完整产品闭环，不能称兼容原FUXA所有特性。

### 可审阅的完整产品MVP合同
1. Web端能登录及新增一台虚拟设备（含RBAC、请求验证）；C++后台能保存与加载配置。
2. C++设备采集通过libmodbus TCP与虚拟设备读取状态；在数据库记录时间戳和事件、前端REST读历史及WebSocket实时状态。
3. 设备断线有超时/重连（有界退避、不忙循环）、异常告警产生/确认及历史审计，可回放真实重启/故障测试。
4. 源代码可在原生Ubuntu上构建/测试；申请“嵌入式Linux/ARM部署”必须另外取得QEMU/ARM真实构建/运行日志；仅普通x86 Linux启动不足以宣称ARM底层经验。
5. 明确本人成果的C++模块代码、文档、测试、Git提交记录，保留所有原版权/许可要求，模拟数据均为个人虚构，无电信实习保密材料。

**不能保证项目“自动算自己东西”**：面试主要考用户自己是否设计实现、懂原理、能复现并修复故障；例如提问C++线程如何退出、缓存/数据库一致性、Socket.IO为什么不兼容、设备断联状态机、跨架构编译和错误日志。**项目深度与工程证据比“后端是否写成C++”更重要**，但正确实施重构确实能显著提高嵌软JD匹配度。

开工闸门保持：本轮只是C++替换可行性和范围审核，**暂不下载/装环境/开源Fork/建立新代码仓/购买或寄送开发板，也不开始新5题Linux面经**，等用户认可以“完整可演示产品的核心功能＋本人Linux C++后端”为目标，再确定迁移范围、起始日和电脑环境。原Q037–Q041其他对话已发题，暂无用户答题证据。


## 2026-10-12 用户认可设计、要求社交平台秋招项目交叉验证
- 用户明确“好的那么就先这么办”，认可继续以**成熟工业监控Web前端+本人Linux C++后端+设备通信、后续ARM测试**为项目设计主线，要求定期参考牛客、B站、CSDN等平台博主的2024—2026嵌入式秋招项目，检查重大偏差、借鉴其他人的项目设计。**状态升级为 USER_APPROVED_DESIGN**，但没有要求下载/安装/编码/配置电脑或开始五题面经，保持 START_NOT_APPROVED。
- 本轮[跨平台项目和校招JD交叉研究](EMBEDDED_AUTUMN_PROJECT_BENCHMARK_2026-10-12.md)：参考B站Linux+Qt工业电表/智慧家庭、Linux C++ Qt电网监控、智能车库以及牛客2026届FreeRTOS机器人、V4L2相机、xv6、嵌入式Linux边缘AI两类案例。重点借鉴**设备-数据-界面闭环、STM32通信/板级调试、ARM与故障复现**，不因博主建议立即加Qt、驱动、摄像头、VLA。
- 对照2027届精智达Linux C++、海雀科技嵌软多线程Socket、联影嵌软、思必驰IoT、影石通信嵌软的实际JD：现有系统设计对**嵌入式Linux应用/通信设备平台**无重大方向偏差，但对纯驱动/BSP/MCU岗覆盖不足。最小调整要求C++守护进程深度>换肤、ARM真实目标运行、择机使用旧STM32做协议联调；本机x86不能冒称ARM嵌入式。
- 保留开源许可证、作者归属及原项目真正保留的功能声明。每周招聘雷达顺带关注新秋招项目和面经的实质差距，有可靠跨来源证据再提局部改动，避免被商业课程营销带偏。
