# 高校 AI 课程政策设计要点

> 综合斯坦福 AIMES、Teaching Commons AI Guide 及学术诚信研究的政策撰写框架。

**文献性质**：高校政策指南综述 + 政策模板（二次整理）  
**核心出处**：Stanford Teaching Commons [1][2]；Bowen & Watson (2024)；Bertram Gallant & Rettinger (2025)  
**整理说明**：六问框架与默认 honor code 规则据斯坦福公开指南；模板为归纳性示范，非任何校方正式文件。  
**核实日期**：2026-08-02

---

## 来源标注说明

政策撰写六问见 Teaching Commons [1]；三档模板依据 AIMES 三路径 [2] 归纳。

## 为什么需要课程级 AI 政策

校级规定通常只能给出底线（如学术诚信、数据安全）。**具体什么作业能用 AI、怎么用、怎么 cite**，必须由任课教师在 syllabus 中明确——因为：

- 不同学科 integrity 惯例不同（coding vs essay vs lab）。
- 不同课程 learning goals 不同（skill-building vs exploration）。
- 学生无法 guess 每门课的期望——「别的课让用」不等于「这门课让用」。

斯坦福默认规则：无明确 statement 时，AI = outside assistance，substantial use 完成 assignment **禁止**。

---

## 政策撰写六问（Teaching Commons）

有效 AI policy 应回答：

| 问题 | 示例内容 |
| --- | --- |
| **What** — 政策是什么？适用哪些工具？ | ChatGPT、Claude、Copilot、Midjourney、翻译 AI…… |
| **When** — 何时适用？什么条件允许/禁止？ | 头脑风暴允许；final draft 禁止；take-home 允许 limit；in-class exam 禁止 |
| **How** — 不合规的后果与流程？ | 先 warning + redo；严重 case 报 academic integrity office |
| **Why** — 理由与 reasoning？ | 「本课目标是独立论证，AI 代写无法训练此 skill」 |
| **Support** — 如何 support 学生？ | office hour 讨论 AI use；writing center；AI literacy workshop |
| **Well-being** — 如何考虑学生福祉？ | 不因 AI anxiety 羞辱；提供 alternative；deadline flexibility 政策 |

---

## 三种政策模板（可 tailoring）

### 模板 A：严格限制 / 禁止

**适用**：写作 intensive、基础技能训练、认证性考试 prep。

```markdown
## AI 使用政策

本课程以培养你的**独立分析、论证与写作能力**为核心目标。除非下方明确允许，
**不得**使用生成式 AI（含 ChatGPT、Claude、Copilot、文心一言等）完成任何
课程作业的全部或实质部分。

**允许**：
- 使用 spell-check / grammar 工具（非 generative）
- 经教师书面批准的特定练习（如有）

**禁止**：
- AI 生成文本作为你的作业提交
- AI 总结替代阅读原文/文献
- AI 代写代码、证明、实验报告

**须披露**：若 incidental use（如查一个术语），在作业末尾注明工具与用途。

**违规处理**：按本校学术诚信规定处理；首次 minor violation 可能要求重做并扣分。
```

### 模板 B：有限允许 / 部分场景

**适用**：高年级、研究方法、需 AI literacy 的专业课。

```markdown
## AI 使用政策

本课程认为 AI 工具是 contemporary scholarship 的一部分，但你必须**批判性、
透明地**使用，且不得让 AI 替代你应掌握的核心技能。

**允许（须 disclosure + citation）**：
- 文献检索辅助（你须亲自阅读原文）
- 头脑风暴与 outline（final 须大幅改写并标注 AI 参与阶段）
- 代码 debug 提示（你须理解每一行并能在 oral 中解释）
- 语言润色（非改变论点）

**禁止**：
- AI 生成整段/整篇提交物
- 考试、quizzes、in-class writing
- 上传含 privacy / 未公开数据 的内容到公共 AI 服务

**披露格式**：作业末尾附「AI 使用声明」：工具名、用途、prompt 摘要、你如何 verify。

**评估**：使用 AI 不自动扣分，但无法 explain your work 时视为 integrity 问题。
```

### 模板 C：指定使用 AI

**适用**：AI literacy、digital humanities、特定 tool 训练课。

```markdown
## AI 使用政策

**本课程要求**在指定作业中使用 generative AI，目标是训练 prompting、
verification 和 ethical judgment。

**要求**：
- 使用课程指定平台（避免 upload sensitive data 到未批准工具）
- 提交 full prompt history + output + 你的 edit/ critique
- 标注 AI 输出中 factual errors 及你的修正

**评估维度**（见 rubric）：
- Prompt 质量与迭代
- 对 AI 输出的 critical evaluation
- 最终产品中你的人类贡献与原创分析

**伦理**：讨论 training data、bias、environmental cost；允许 ethical objection 的
alternative assignment（须开学两周内与教师书面确认）。
```

---

## 工具范围：policy 应 explicit 列出

Teaching Commons 建议 policy 涵盖（至少提及）：

- **Chatbots**：ChatGPT, Claude, Gemini, 文心一言, Kimi……
- **Code**：GitHub Copilot, Cursor, Tabnine……
- **Image**：DALL-E, Midjourney, Stable Diffusion……
- **Audio/Music**：各类生成工具
- **Built-in AI**：Word/Google Docs 内置 AI、搜索引擎 AI summary、Zotero AI……

**Built-in AI 陷阱**：学生可能「无意间」使用 prohibited assistance——需在 policy 中说明如何 disable 或何时算违规。

---

## 与 assignment redesign 联动

AI 时代单纯「禁止」常失效——需同时 redesign tasks：

| 策略 | 说明 |
| --- | --- |
| **Process artifacts** | 交 outline、draft、revision log、reflection |
| **In-class components** | 课堂 writing、oral defense、closed-book section |
| **Authentic tasks** | 本地数据、实时事件、personal experience——AI 难以替代 |
| **AI-critical tasks** | 评 AI 输出错误、compare AI vs human analysis |
| **Oral component** | 随机 follow-up questions on submitted work |
| **Staging** | Proposal → draft → peer review → final |

---

## 首堂课必做：对话，非只念 policy

- 用 15–20 分钟讨论 policy，举 2–3 个 scenario（「这样算不算违规？」）。
- 邀请学生 questions——surface 灰色地带。
- 连接 learning goals：「我们为什么这样规定。」
- 新 assignment 类型出现时 revisit。

---

## 公平性与 inclusion 考量

- **Digital divide**：Not all students 有 equal access to paid AI tools——若 assign AI use，provide institutional access。
- **Learning differences**：Limited AI use 可能对某些学生是 reasonable accommodation——与 disability services 协调。
- **Competence penalty**：Research 提示 evaluator 可能 bias against disclosed AI use——rubric 应 evaluate learning, not penalize transparency。
- **Language learners**：需区分「AI 翻译」与「AI 代写」——policy 可 allow 前者 for draft stage with disclosure。

---

## 其他高校参考

除斯坦福 AIMES 外，可参考：

- **MIT**：generative AI 教学 guidance（强调 course-level policy）
- **Harvard**：AI learning principles 与 school-level resources
- **University of Toronto**：AI 与 academic integrity FAQ
- **UNESCO**：Guidance for generative AI in education and research (2023)

中国高校近年陆续出台 AI 使用规范——课程 policy 应**不低于**校级底线，且更具体。

---

## 参考文献与可追溯来源

1. **Stanford Teaching Commons**. Creating your course policy on AI. https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/creating-your-course-policy-ai（访问 2026-08-02）
2. **Stanford CTL**. AI Teaching Strategies. https://ctl.stanford.edu/aimes/ai-teaching-strategies（访问 2026-08-02）
3. **Stanford CTL**. AIMES Library of Examples. https://ctl.stanford.edu/aimes/aimes-library-examples（真实课程 policy 范例，访问 2026-08-02）
4. **Bowen, J. A., & Watson, C. E.** (2024). *Teaching with AI: A Practical Guide to a New Era of Human Learning*. Johns Hopkins University Press. ISBN 978-1-4214-4674-7.
5. **Bertram Gallant, T., & Rettinger, D. A.** (2025). *Teaching for Integrity in the Age of AI*. University of Oklahoma Press.
6. **UNESCO** (2023). *Guidance for Generative AI in Education and Research*. https://unesdoc.unesco.org/ark:/48223/pf0000386693（国际政策参考，访问 2026-08-02）
7. **MIT**. Generative AI and Teaching / Academic Integrity resources. https://tll.mit.edu/（高校政策参考索引，访问 2026-08-02）
8. **University of Toronto**. Generative Artificial Intelligence and Academic Integrity. https://www.academicintegrity.utoronto.ca/（访问 2026-08-02）
