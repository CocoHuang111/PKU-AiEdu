# AI 辅助教师备课与学情分析工作流

> 高校教师在合规前提下，用 AI 支持课程设计、材料生成与学情洞察的方法。

**文献性质**：教学实践工作流（二次整理）  
**核心出处**：Bowen & Watson (2024) Ch.5；Mollick (2024)；Furze (2024)  
**整理说明**：任务清单与 prompt 示例据 Bowen & Watson 归纳；工具名为举例，非采购推荐。  
**核实日期**：2026-08-06

---

## 来源标注说明

教师侧 AI 应用框架见 Bowen & Watson [1]；合规边界见清华/北大校规 [2][3]。

## 基本原则

| 原则 | 操作含义 |
| --- | --- |
| **AI 辅助，人负责** | 你对 syllabus、评分、反馈、学术判断负最终责任 |
| **不上传敏感数据** | 无学生 identifiable 作业、成绩、医疗/涉密研究数据进公共 AI [2] |
| **核验一切事实性输出** | 文献、日期、法条、代码须人工或数据库核对 |
| **透明** | 若 AI 生成材料直接发给学生，考虑标注；AI 生成例题须教师审校 |

Bowen & Watson：AI 可承担**低阶、耗时**任务，释放时间做高阶教学设计 [1]。

## 工作流总览

```text
课程规划 → 材料草稿 → 活动/作业设计 → 学情/评教分析 → 迭代
     ↑__________________________________________|
```

## 1. 课程与单元规划

| 任务 | AI 可协助 | 教师必须做 |
| --- | --- | --- |
| 从 learning outcomes 反推单元结构 | 生成 2–3 种章节/周次方案 | 选方案并对齐院系要求 |
| 对齐布鲁姆层次 | 标注每单元认知层次草案 | 确认无「全停留在记忆层」 |
| 识别与 AI 冲突的目标 | 列出「AI 可一键完成」的目标 | 改写目标或改评价 |

**Prompt 示例**：

```text
我是 [学科] 本科 [课程名] 教师。以下是 5 条 learning outcomes：[粘贴]
请提出 14 周单元划分方案，每单元含：主题、预期认知层次（布鲁姆）、
1 个主动学习活动建议。标注哪些作业可能被 GenAI 轻易完成，并建议 redesign 方向。
不要编造文献。
```

## 2. 阅读与文献工作（研究型备课）

Bowen & Watson 列举的用途 [1]：检索、对比、摘要、找反证、组织论点。

| 用途 | 说明 | 风险 |
| --- | --- | --- |
| 文献初筛 | 关键词扩展、摘要对比 | **幻觉 citation** — 须回数据库核验 |
| 论文段落解释 | 上传 PDF 后解释难句 | 版权与隐私；优先用机构订阅工具 |
| 论点对立面 | 「找反对我 thesis 的证据」 | 训练批判思维设计，非代替阅读 |

**禁止**：将**学生论文、匿名化不足的数据**上传公共 AI 做分析 [2][3]。

## 3. 教学材料草稿

| 材料 | AI 协助方式 | 审校要点 |
| --- | --- | --- |
| 讲义 outline | 由 outcomes 生成结构 | 概念准确性、深度、例子适切 |
| 例题/习题 | 生成多难度题目 | 答案正确性；是否与 AI 可秒解 |
| Rubric 草案 | 由 outcomes 生成标准描述 | 是否体现「优于 AI」的维度 [1] |
| 课堂讨论题 | 生成争议性问题列表 | 学术中立、文化敏感 |
| 双语/无障碍草稿 | 简化语言、替代格式 | **不保证** WCAG；人工复核 |

## 4. 作业与 AI policy 联动设计

与 `高校AI课程政策设计要点.md` 同步：

1. 先定 **AIMES 路径**（critical / limited / inclusive）。
2. 为每个 assignment 定 **AIAS 级别**。
3. 写 **ready-to-submit** 清单（见 `02-课程与教学设计/Human-Effort与PROCESS作业模板.md`）。

**Prompt 示例**：

```text
Assignment brief：[粘贴]
课程 AI 政策：AIAS 2（仅 planning/editing，核心论证须人工）
请生成：① ready-to-submit 检查清单 ② 课堂讨论用 3 个 integrity scenario
③ 口试追问示例 5 条
```

## 5. 学情与评教文本分析（聚合、去标识）

| 数据源 | 可问的问题 | 前提 |
| --- | --- | --- |
| 聚合 exam 错题分布 | 哪些概念集中混淆 | 仅统计摘要，非个体作业 |
| 课堂 exit ticket 汇总 | 今日 top 3 困惑 | 学生自愿、无姓名 |
| 评教开放题（脱敏） | 主题聚类、情感倾向 | 机构 policy 允许 |

**注意**：属于 learning analytics 时适用 `10-公平无障碍与数据治理/学习分析伦理与数据治理.md`。

## 6. 反馈与办公时间准备

| 场景 | AI 协助 |
| --- | --- |
| 常见写作问题 | 从 anonymized 片段归纳 error patterns（须合规） |
| 反馈语言润色 | 教师写要点，AI 辅助多种语气版本 — **内容须教师定** |
| 个别辅导预案 | 根据 assignment rubric 生成追问清单 |

**禁止**：AI 自动给分或替代对 individual student 的 integrity 认定。

## 7. 学期迭代 checklist

- [ ] 每个 assignment 是否仍测到「AI 无法单独证明」的能力？
- [ ] policy 与 AIAS 是否一致？
- [ ] 是否提供 institutional AI 访问或替代（公平）？
- [ ] 学生是否完成至少一次 AI literacy / disclosure 训练？
- [ ] 教师是否核验过 AI 生成的例题、引用、代码？

## 边界与风险

- 工具迭代快，文档中的产品名可能过时 — 原则优先于工具。
- AI 生成 slide/讲义可能导致**千班一面** — 保留学科特色与本地案例。
- 过度依赖 AI 备课可能削弱教师对**难点**的体感 — 保留手写 outline 环节。

## 参考文献与可追溯来源

1. **Bowen, J. A., & Watson, C. E.** (2024). *Teaching with AI: A Practical Guide to a New Era of Human Learning*. Johns Hopkins University Press. ISBN 978-1-4214-4674-7（Ch.5 AI-Assisted Faculty）
2. **清华大学**. 《清华大学人工智能教育应用指导原则》. https://www.tsinghua.edu.cn/info/1176/122770.htm（访问 2026-08-06）
3. **北京大学 AI 科研诚信治理平台**. http://scielab.pku.edu.cn/aigc/guidelines/overview.html（访问 2026-08-06）
4. **Furze, L.** (2024). *Practical AI Strategies: Engaging with Generative AI in Education*. Amba Press. ISBN 978-1-923116-35-1.
5. **Mollick, E.** (2024). *Co-Intelligence*. Portfolio/Penguin. ISBN 978-0-593-71671-7.
