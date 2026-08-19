# AI 时代作业 Redesign 框架

> 从「禁止 AI」到「重构任务 + 对齐 policy + 评价证据」的系统方法。

**文献性质**：高校教学指南 + 专著实践框架归纳  
**核心出处**：Stanford AIMES；Bowen & Watson (2024)；TEQSA (2023)  
**整理说明**：策略表据 AIMES 与 `高校AI课程政策设计要点.md` 升格；流程为教学 design 归纳。  
**核实日期**：2026-08-06

---

## 来源标注说明

Redesign 策略见 Stanford AIMES [1]、Bowen & Watson [2]；评价对齐见 TEQSA [3]。

## 为什么需要 Redesign

单纯在旧作业上贴「禁止 ChatGPT」往往失效——因为任务本身**奖励** AI 可完成的产出（泛化 essay、标准 coding exercise）[1][2]。

**Redesign 目标**：使 learning goals 仍可达，且评价证据**可信、公平**。

## 四步框架

```text
1. 重审学习目标 → 2. 选 AI 路径 → 3. 重构任务与证据 → 4. 写清 policy 并首堂对话
```

### Step 1：重审学习目标

| 问题 | 若答案为「否」则需 redesign |
| --- | --- |
| 此作业训练的能力，AI 能否一键完成？ | 是 → 改任务或改权重 |
| 若学生用 AI，仍能达到 course outcomes 吗？ | 否 → 调整活动或 policy |
| 评价方式能否观测到「思考过程」？ | 否 → 增加 process evidence |

### Step 2：选择 AI 路径（AIMES 三路径）

| 路径 | 适用 | 作业特征 |
| --- | --- | --- |
| **AI-critical** | 技能训练、基础掌握 | 课堂 closed section；AI 禁止或仅 planning |
| **AI-limited** | 多数本科课 | 分阶段允许；强制 disclosure |
| **AI-inclusive** | 高阶整合、探索 | AI 协作 + 批判评价 AI 输出 |

详见 `斯坦福AIMES框架与策略.md`。

### Step 3：重构策略工具箱

| 策略 | 做法 |
| --- | --- |
| **Process artifacts** | outline → draft → revision log → reflection |
| **In-class components** | 课堂 writing、quiz、演示 |
| **Authentic / localized** | 本地数据、个人经验、实时事件 |
| **AI-critical tasks** | 评改 AI 输出；compare AI vs expert |
| **Oral component** | 答辩、随机追问 |
| **Staging** | proposal 先审再展开 |
| **Spec breakdown** | 大项目拆成不可一次性生成的子任务 |

### Step 4：Policy 与对话

- Syllabus 写清 **What / When / How / Why / Support / Well-being**（六问，见 `高校AI课程政策设计要点.md`）。
- 每个 assignment brief 标明 **AIAS 级别**（见 `09-AI时代的评价与诚信/AI使用分级与披露规范.md`）。
- 首堂 15–20 分钟 scenario 讨论：「这样算不算违规？」

## 学科快速参考

| 学科 | Redesign 方向 |
| --- | --- |
| **写作/人文** | 过程 portfolio + 口试；禁止 AI 写 final argument |
| **编程** | 现场 debug；提交 test cases + 代码 walkthrough |
| **实验科学** | 原始 lab notebook + 现场操作检查 |
| **大班讲授课** | 低 stakes 在线 quiz + 高 stakes 课堂测 |

## 与 OBE / 逆向设计的关系

`逆向设计与OBE.md`：从 outcomes 反推 assessment → activities。

AI 时代追加一问：**「在此 outcome 下，何种 evidence 在 AI 存在下仍有效？」**

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 加 oral = 完全防 AI | 需配合 process；口试可抽样 |
| 更复杂 prompt = 更安全 | 复杂任务 AI 仍可能完成部分 |
| Redesign 一次就够 | 每学期根据工具演进微调 |
| 只改 rubric 不改 task | Rubric 无法拯救无效任务 |

## 参考文献与可追溯来源

1. **Stanford CTL**. AI Teaching Strategies / AIMES. https://ctl.stanford.edu/aimes/ai-teaching-strategies（访问 2026-08-06）
2. **Bowen, J. A., & Watson, C. E.** (2024). *Teaching with AI: A Practical Guide to a New Era of Human Learning*. Johns Hopkins University Press. ISBN 978-1-4214-4674-7.
3. **TEQSA** (2023). *Assessment reform for the age of artificial intelligence*. https://www.teqsa.gov.au/about-us/news-and-events/latest-news/assessment-reform-age-artificial-intelligence（访问 2026-08-06）
4. **MIT TLL**. Generative AI & Your Course. https://tll.mit.edu/teaching-resources/course-design/gen-ai-your-course/（访问 2026-08-06）
5. **Wiggins, G., & McTighe, J.** (2005). *Understanding by Design* (2nd ed.). ASCD.（逆向设计经典）
