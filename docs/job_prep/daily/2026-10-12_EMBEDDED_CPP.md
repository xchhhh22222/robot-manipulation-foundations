# 2026-10-12（周一）嵌入式C/C++ M1实际学习记录与结课
状态：**首个源码/运行/GDB流程引导式实操完成**，不是独立掌握整门C++。下一学习日：**2026-10-13周二**，见[完整执行教案](2026-10-13_EXECUTION_PLAN.md)。

## 学生实际证据（非助手代运行）
- 学生本人在Ubuntu `~/embedded-linux-learning` 终端回传：
  ```text
  wxc@wxc-MS-7D36:~/embedded-linux-learning$ ./temperature_demo
  Temperature: 31.8 C
  ```
- Ubuntu `g++ --version` 实测13.3.0（此前已回传）。
- VS Code截图中的`temperature_demo.cpp`关键语句为：
  ```cpp
  int raw = 318;
  double temperature = 0;
  temperature=raw/10.0;
  ```
  第9行`std::cout`打印`Temperature: ... C`。这里说明`10.0`触发浮点运算；此前学生一开始写`raw/10`会整数截断，后本人成功修改。只确认截图所见，不编造完整文件版本或Git提交。
- 学生安装微软C/C++扩展并使用`code .`打开源码目录；开始F9断点无反应，重新载入VS Code后截图显示第9行红点。
- F5选择`C/C++: g++ build and debug active file`。截图Debug Console为`Breakpoint 2, main() ... temperature_demo.cpp:9`且第9行有黄色执行标记 → **断点命中证实**。
- 鼠标悬停变量后学生回答“是的我看到了”，即**学生口述变量观察成功**（没有独立截图展示弹窗内容）。
- F10 Step Over后另一截图黄色箭头从第9行移到`return 0;`第11行；学生切换到Terminal后说“哦输出了” → **单步跨过及输出位置确认**。
- 快捷键理解提问：学生答“f11是下一步10是跳出函数”，教师解释F10 Step Over、F11 Step Into、Shift+F11 Step Out。**学生尚未在真实函数上独立验证F11/Shift+F11**，不能记概念完全掌握。

## 结果与边界
| 事项 | 状态 | 证据 |
|---|---|---|
| C++工具链查询 | VERIFIED | Ubuntu g++ 13.3.0实际终端 |
| 温度计算程序运行 | VERIFIED | 318转31.8的实际输出 |
| 关键运算写法 | SOURCE_SCREENSHOT_VERIFIED | `raw/10.0` |
| GDB断点命中 | VERIFIED | main第9行Debug Console截图 |
| F10执行位置变化 | VERIFIED | 停到return 0第11行截图 |
| 变量悬停 | USER_REPORTED | 口头确认看到 |
| F11函数进入/跳出 | NOT_TESTED | 只有教学解释，答题部分概念混淆 |
| 独立构建/全量代码审查 | PARTIAL | 已运行、自动构建调试，但尚无独立完整编译命令日志、全源码审查 |
| 本地练习代码已推GitHub | NOT_VERIFIED | 只在Ubuntu工作目录，未见`git push` |

## 下次最小任务
在VS Code复用`~/embedded-linux-learning`，本人创建`rawToCelsius(int raw)`温度转换函数并输出`318→31.8`，独立测试`0`和`-55`，用GDB F11验证进入函数、F10跨过函数调用和Shift+F11退出。技术与ROS、公考、科研全部按明日教案时间盒安排；明日结果必须有用户实际输出才能改状态。

> 历史上多次GitHub更新学习状态遭拦截，故本日另设短记录作为可查的真实会话证据；该记录本身仅表示此Markdown已写GitHub，**不代表用户本地源文件已上传**。
