# 实践案例：编程课 AI-debug 与代码评改

> PROCESS 模板在计算机教学中的示范设计（非特定课程正式 syllabus）。

**文献性质**：教学实践案例（二次设计）  
**核心出处**：Bowen & Watson (2024) PROCESS 变体；Chan & Colloton (2024) SARPS；AIMES  
**整理说明**：案例为可复用模板；编程 integrity 须对齐院系学术规范。  
**核实日期**：2026-08-06

---

## 来源标注说明

Debug 与 prompt 迭代流程据 Bowen & Watson PROCESS Variation 2 [1]。

## 课程情境（示范）

| 项 | 设定 |
| --- | --- |
| **课程** | 本科数据结构 / 编程基础 |
| **单元** | 链表实现与单元测试 |
| **AI 路径** | AI-limited（AIMES 第二路径） |
| **AIAS** | 作业1: 0；作业2: 3；作业3: 2 |

## 学习目标

1. 独立实现指定 ADT 并通过 hidden tests  
2. 阅读与 debug 他人（或 AI）代码  
3. 解释时间/空间复杂度 trade-off  
4. 合规使用 AI 并记录 prompt  

## 三次作业设计

### 作业 1：Closed implementation（AIAS 0）

| 项 | 内容 |
| --- | --- |
| **形式** | 课堂 lab 70 分钟 + 限时提交 |
| **允许** | 仅 IDE、课程提供的 stub；**禁止** Copilot/ChatGPT |
| **证据** | 本地 git commit 时间戳 + 现场随机 code walkthrough（SARPS S4） |
| **目的** | 证明 baseline 能力 |

### 作业 2：AI 协作 + Debug（AIAS 3，PROCESS 变体）

**流程**：

1. 用 AI 生成链表某操作的初版实现（prompt 由教师提供模板，含 language/version）。  
2. 编写 **≥10 个** 自己设计的 test cases（含 edge cases）。  
3. 记录 AI 代码在哪些 test 失败；**人工 fix** 并注释每处修改理由。  
4. 写 300 字：你的 fix 策略 vs 若让 AI 继续 fix 的风险。  
5. 提交：code + test log + prompt transcript + AI 使用声明。

**Rubric 要点**（Better than AI [2]）：

| 维度 | F (AI-level) | B | A |
| --- | --- | --- | --- |
| Tests | 仅样例级 | 覆盖 main edges | 边界+性能意识 |
| Debug | 仅粘贴 AI fix | 有系统诊断 | 解释 root cause |
| 文档 | 无 prompt log | 完整声明 | 反思 AI 局限 |

### 作业 3：复杂度 trade-off 报告（AIAS 2）

1. AI 生成两种实现（如 array vs linked list）及 Big-O 说明。  
2. 学生**手工验证** Big-O（用小规模 benchmark 或推导）。  
3. 指出 AI 分析中**一处不精确或遗漏前提**的表述。  
4. 800 字报告 + 自己跑的 timing 图（可 AI 辅助 matplotlib 草稿，图须核验）。

## 课堂配套活动（90 分钟 lab）

| 时段 | 活动 |
| --- | --- |
| 0–15' | 演示：同一 bug 的 AI fix vs 人工 fix — 讨论 test 重要性 |
| 15–50' | Pair：互换 AI 生成代码，互相写 failing test |
| 50–70' | `AI支持的主动学习与课堂脚手架.md` 活动 2：AI 错误解析 |
| 70–90' | Q&A；强调作业 2 提交格式 |

## Policy 片段（syllabus 示范）

```markdown
本课允许在 **作业 2–3** 使用生成式 AI 辅助 coding，须：
① 使用声明 ② 保留 prompt 与关键输出 ③ 禁止上传 course autograder 的 hidden test
④ 禁止将同学代码输入公共 AI
作业 1 与 所有 exam：**禁止** AI。违规按院系程序处理。
```

## 与北大沙龙连接

`pku_salon` 多次讨论编程课 Copilot 边界 — 本案例强调 **test-driven + walkthrough**；沙龙内容为非 peer-reviewed 经验。

## 教师 checklist

- [ ] Autograder 不与 public AI 训练数据重叠策略（若院系有要求）  
- [ ] 提供 **无 AI 环境** lab seat  
- [ ] Hidden tests 定期轮换  
- [ ] 口试/walkthrough 抽样比例定明  

## 边界与风险

- AI 代码可能有**许可证/抄袭**风险 — 要求学生能解释每行。  
- Copilot 在 lab 网络难以完全屏蔽 — 作业 1 靠 timed + walkthrough。  
- 勿将 debug 作业权重过高惩罚「不用 AI 也能写对」的学生 — rubric 评 process。

## 参考文献与可追溯来源

1. **Bowen, J. A., & Watson, C. E.** (2024). *Teaching with AI*. Johns Hopkins University Press. ISBN 978-1-4214-4674-7（PROCESS Variation 2）
2. **Bowen & Watson** (2024). Ch.8 Better than AI grading — 见 `Better-than-AI评分与Rubric调整.md`
3. **Chan, C. K. Y., & Colloton, T.** (2024). *Generative AI in Higher Education*. https://doi.org/10.4324/9781003459026
4. **Stanford CTL**. AIMES Library of Examples（CS 类 policy 参考）. https://ctl.stanford.edu/aimes/aimes-library-examples（访问 2026-08-06）
5. **Weber-Wulff, D., et al.** (2023). AI-generated code detection limitations. *International Journal for Educational Integrity*, *19*, 26. https://doi.org/10.1007/s40979-023-00146-z
