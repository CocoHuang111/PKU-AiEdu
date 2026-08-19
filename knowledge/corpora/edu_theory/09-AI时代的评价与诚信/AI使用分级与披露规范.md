# AI 使用分级与披露规范

> AIAS、AAA 及中外课程级 AI 披露模板，供 syllabus 与作业说明使用。

**文献性质**：教学实践框架 + 高校政策指南归纳  
**核心出处**：Perkins et al. (2024) AIAS；MIT TLL Quickstart；Stanford Teaching Commons  
**整理说明**：AIAS 级别据 Perkins 原文；披露模板为归纳示范，非任何校方正式文件。  
**核实日期**：2026-08-06

---

## 来源标注说明

AIAS 见 Perkins et al. [1]；syllabus policy 要素见 MIT TLL [2]、Stanford [3]。

## 为什么需要「分级 + 披露」

- 不同作业 AI 允许程度不同——**课程级** policy 无法替代**作业级**说明。
- 披露不是惩罚透明，而是让评价者判断**证据效力**与**诚信** [2][3]。
- 清华、北大等校规均强调**依规披露** AI 使用 [4][5]。

## AIAS（Artificial Intelligence Assessment Scale）

Perkins 等 (2024) 提出 0–5 级，便于在 rubric 与 assignment brief 中沟通 [1]：

| 级别 | 名称 | 典型允许行为 |
| --- | --- | --- |
| **0** | No AI | 任何 AI 辅助均违规 |
| **1** | AI-assisted planning | 仅 brainstorming、结构建议；提交内容须完全人工 |
| **2** | AI-assisted editing | AI 改语法/格式；观点论证须人工 |
| **3** | AI as collaborator | AI 生成部分段落/代码，人工大幅编辑与整合 |
| **4** | AI as co-creator | AI 完成明确子任务，人工负责整合与质量 |
| **5** | Full AI | 开放使用，**必须完整披露** |

**使用注意**：每级须配**具体场景示例**（「这样算不算违规？」），否则学生仍无法执行。

## 披露内容清单（建议最低要求）

MIT TLL Quickstart 与多校指南共识 [2][3]：

| 项目 | 说明 |
| --- | --- |
| 工具名称与版本 | ChatGPT-4o、Claude 3.5、Copilot 等 |
| 使用日期与环节 | 何时用于 outline / draft / 润色 |
| 用途说明 | brainstorming、翻译、debug、文献初筛…… |
| 关键 prompt 摘要 | 不必全文，但须可追溯 |
| 人工核验与修改 | 哪些 AI 输出被采纳/拒绝及理由 |
| 生成内容在成果中的位置 | 页码、段落、代码块 |

## 作业末尾声明模板（示范）

```markdown
## 生成式 AI 使用声明

- **工具**：［名称与版本］
- **使用环节**：［如：2026-03-10 用于初稿 outline；2026-03-15 用于语法检查］
- **用途**：［如：头脑风暴三个论证角度；未直接粘贴 AI 文本］
- **人工修改**：［说明对 AI 建议的核验与修订］
- **本作业 AI 允许级别**：AIAS ［0–5］（见 assignment brief）
```

## 与 APA / MLA 等引用规范

- **APA**：AI 生成内容引用格式见 APA Style 官网 AI 章节 [6]。
- **MLA**：MLA 对 AI 引用有专门说明 [7]。
- **中文课程**：可要求「脚注说明 AI 辅助段落」+ 上述声明表——**与院系格式指南一致即可**。

## 三档课程 policy 与 AIAS 的对应

| 课程 policy 档位（见 `06-生成式AI与大学教学/高校AI课程政策设计要点.md`） | 典型 AIAS 范围 |
| --- | --- |
| 完全禁止 | 全作业 AIAS 0 |
| 有限允许 | 按作业指定 0–3 |
| 开放探索 | 多数作业 3–5 + 强制披露 |

## 边界与风险

- 披露负担不应**超过学习价值**——低 stakes 练习可简化声明。
- **Competence penalty**：研究显示评价者可能对 disclosed AI use 有偏见——rubric 应评学习而非惩罚透明 [8]。
- 日志要求需考虑**隐私**——勿要求上传含个人信息的完整 chat 到公共平台。

## 参考文献与可追溯来源

1. **Perkins, M., Furze, L., Roe, J., & MacVaugh, J.** (2024). *The Artificial Intelligence Assessment Scale (AIAS)*. https://doi.org/10.53761/q3azde36
2. **MIT Teaching + Learning Lab** (2025). *A Quickstart Guide to Thinking about AI in your Course* (PDF). https://tll.mit.edu/wp-content/uploads/2025/07/GAI_Policies_Quickstart-web.pdf（访问 2026-08-06）
3. **Stanford Teaching Commons**. Creating your course policy on AI. https://teachingcommons.stanford.edu/teaching-guides/artificial-intelligence-teaching-guide/creating-your-course-policy-ai（访问 2026-08-06）
4. **清华大学**. 《清华大学人工智能教育应用指导原则》. https://www.tsinghua.edu.cn/info/1176/122770.htm（访问 2026-08-06）
5. **北京大学 AI 科研诚信治理平台**. 使用规范说明. http://scielab.pku.edu.cn/aigc/guidelines/overview.html（访问 2026-08-06）
6. **American Psychological Association**. How to cite ChatGPT. https://apastyle.apa.org/blog/how-to-cite-chatgpt（访问 2026-08-06）
7. **Modern Language Association**. How do I cite generative AI in MLA style? https://style.mla.org/citing-generative-ai/（访问 2026-08-06）
8. **Bertram Gallant, T., & Rettinger, D. A.** (2025). *Teaching for Integrity in the Age of AI*. University of Oklahoma Press.
