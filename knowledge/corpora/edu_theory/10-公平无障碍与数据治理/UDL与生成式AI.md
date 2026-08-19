# UDL 与生成式 AI

> CAST UDL 3.0 原则下，AI 作为辅助而非替代无障碍设计的定位。

**文献性质**：官方 UDL 框架 + 高等教育实证访谈研究  
**核心出处**：CAST UDL Guidelines 3.0 (2024)；WCAG 2.2；残障学生 GenAI 访谈研究  
**整理说明**：UDL 三原则据 CAST 官网；GenAI 风险与机遇据 2025 访谈研究 [3]。  
**核实日期**：2026-08-06

---

## 来源标注说明

UDL 3.0 见 CAST [1]；无障碍技术标准见 W3C WCAG [2]。

## UDL 3.0 三项原则（简）

| 原则 | 含义 | AI 可能角色 |
| --- | --- | --- |
| **多元参与（Engagement）** | 动机、选择、自我调控 | 个性化练习建议——**不能替代**有意义任务设计 |
| **多元表征（Representation）** | 多种方式呈现信息 | 文本简化、多模态转换——须**人工核验准确性** |
| **多元行动与表达（Action & Expression）** | 多种方式展示学习 | 语音转文字、构思辅助——须保留**等效评价标准** |

UDL 3.0 加强对**身份、系统性排斥与偏见**的关注 [1]——AI 整合需主动识别算法偏见与数字鸿沟。

## AI 可辅助的场景

- **材料获取**：为屏幕阅读器优化格式前的初稿整理（需人工确认结构）。
- **语言支持**：ESL 学生的 draft 阶段语言反馈——policy 须区分「翻译辅助」与「代写」。
- **表达替代**：语音输入、 outline 扩展——配合 `09-AI时代的评价与诚信/` 披露规范。
- **复习与脚手架**：苏格拉底式提问 bot——宜用于 formative，非 summative 唯一证据。

## AI 不能替代什么

| 责任 | 说明 |
| --- | --- |
| **源头可访问设计** | 课件、平台、实验环境须符合 WCAG [2] |
| **合理便利（accommodation）** | 正式便利措施由 disability services 决定，非学生自找 GenAI |
| **内容等价** | AI 简化版可能丢概念——需学科教师审核 |
| **隐私与安全** | 不宜把 disability 相关信息输入公共 AI |

## 实证：残障学生的 GenAI 体验

2025 年对高校残障学生的访谈研究 [3] 发现：

- **潜在收益**：降低表达与材料获取障碍。
- **风险**：工具本身不可访问、错误输出、隐私与平台收费。

安大略高校调查亦显示：部分学生将 GenAI 当作**正式便利不足时的替代**——暴露制度供给缺口，而非证明可取消 accommodation [3]。

## 政策设计建议

1. **禁止 AI 的 policy** 可能意外取消残障学生已依赖的辅助——需与 disability services 协调例外。
2. **鼓励 AI 的 policy** 须考虑**付费工具鸿沟**——提供 institutional access。
3. 评价 redesign 时，口试/实时任务对焦虑或语言障碍学生负担更大——须提供**替代证据形式**。

## 与现有 UDL 文档的关系

`02-课程与教学设计/通用学习设计UDL.md` 覆盖经典 UDL 原理；本文档专注 **GenAI 交汇**。

## 边界与风险

- 自动生成「无障碍版本」**不保证** WCAG 合规或内容等价。
- 勿将结构性支持责任**转移**给学生与商业平台。
- AI 偏见可能放大对少数群体的刻板印象——需人类审核。

## 参考文献与可追溯来源

1. **CAST** (2024). *Universal Design for Learning Guidelines 3.0*. https://udlguidelines.cast.org/（访问 2026-08-06）
2. **W3C** (2023, updated 2024). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/（访问 2026-08-06）
3. **Exploring the role of generative AI in higher education: Interviews with students with disabilities** (2025). *Education and Information Technologies*. https://doi.org/10.1007/s10639-024-13134-8
4. **UNESCO** (2023). *Guidance for Generative AI in Education and Research*. https://doi.org/10.54675/EWZM9535
5. **清华大学**. 《清华大学人工智能教育应用指导原则》（公平包容原则）. https://www.tsinghua.edu.cn/info/1176/122770.htm（访问 2026-08-06）
