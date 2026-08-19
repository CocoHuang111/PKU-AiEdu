# Co-Intelligence：课堂人机协作四原则

> Ethan Mollick (2024) 提出的 AI 协作原则及高校课堂落地方式。

**文献性质**：专著实践框架提炼  
**核心出处**：Mollick, E. (2024). *Co-Intelligence: Living and Working with AI*  
**整理说明**：四原则与课堂示例据 Mollick 原文及 Wharton 教学实践归纳；非逐字翻译。  
**核实日期**：2026-08-06

---

## 来源标注说明

四原则见 Mollick [1]；Inside Higher Ed 对高校在线教学团队的解读见 [2]。

## 核心定位

Mollick 将生成式 AI 视为 **co-intelligence（共同智能）**：不是替代人类思考，而是可协作的「思维工具」。高校应用重点是：**在明确 policy 下，把 AI 嵌入备课、课堂活动与形成性反馈**，同时保持 human in the loop [1]。

## 四原则

| 原则 | 含义 | 课堂含义 |
| --- | --- | --- |
| **1. Always invite AI to the table** | 主动实验，而非回避 | 教师先在小范围试用活动设计； syllabus 写清允许范围 |
| **2. Be the human in the loop** | 人做最终判断与责任承担 | 学生须核验 AI 输出；评价看过程证据而非仅 final text |
| **3. Treat AI like a person (tell it what kind)** | 给角色、受众、语气、约束 | 教 prompt 时强调**情境化**，而非万能咒语 |
| **4. Assume this is the worst AI you'll use** | 工具会快速迭代 | 教**持久能力**（核验、批判、披露），少绑单一产品 |

## 原则 3 的课堂 prompt 结构

Mollick 强调 LLM 输出质量随 **context + specificity + iteration** 提升 [1][2]：

```text
你是 [角色，如：苏格拉底式提问者 / 某学科 peer reviewer]
受众是 [如：本科二年级、无先修 XX 的学生]
任务：[具体任务，如：只提追问，不给最终答案]
约束：[如：引用须可核验；不确定处明确说「不知道」]
输出格式：[bullet / 表格 / 不超过 200 字]
```

**教学提示**：让学生对比「空 prompt」与「结构化 prompt」的输出，作为 AI literacy 第一课。

## 三类课堂角色：co-worker / co-teacher / coach

| 角色 | 适用场景 | 示例活动 |
| --- | --- | --- |
| **Co-worker** | 学生与 AI 共同完成复杂任务 | 分工：AI 列选项，人做选择与论证 |
| **Co-teacher** | AI 提供多版本解释或练习 | 同一概念三种难度讲解；学生选最适合的一种并说明理由 |
| **Coach** | AI 追问、反馈、模拟对话 | 口试排练；「扮演挑剔的审稿人」 |

与 `08-AI教学整合模型/人机共同调节学习.md` 衔接：coach 模式最贴近 co-regulation。

## 可复制的课堂活动（15–30 分钟）

### 活动 A：双 prompt 对比（AI literacy）

1. 全班同一问题，两组分别用「模糊 prompt」与「结构化 prompt」。
2. 小组标记：事实错误、逻辑跳跃、遗漏前提。
3. 全班归纳：**何种信息让 AI 更可用**。

### 活动 B：AI 作「错误示范」

1. 教师用 AI 生成一份**含典型错误**的短文/代码/分析。
2. 学生找出错误并改写；提交 revision log。
3. 对齐 learning goal：**识别质量**，而非生成速度。

### 活动 C：Human in the loop 口试排练

1. 学生带 outline 或 draft。
2. 用 AI 生成 5 个追问（prompt 限定「只提问」）。
3. 学生口头回答并记录；正式口试仍由人评价。

## 与 policy / 诚信的衔接

- 活动 A–C 须在 syllabus 标明 **AIAS 级别**（见 `09-AI时代的评价与诚信/AI使用分级与披露规范.md`）。
- 禁止把**未公开数据、学生个人信息**输入公共 AI [3]。
- 披露：保存关键 prompt 与 AI 输出片段用于 formative，非 surveillance。

## 边界与风险

- Mollick 偏乐观实验取向——**仍需**本校 AI 规范与学科红线。
- 「Treat AI like a person」是**比喻**，避免学生 anthropomorphize 导致过度信任。
- 四原则不替代 TPACK 分析：见 `08-AI教学整合模型/TPACK与AI-TPACK.md`。

## 参考文献与可追溯来源

1. **Mollick, E.** (2024). *Co-Intelligence: Living and Working with AI*. Portfolio/Penguin. ISBN 978-0-593-71671-7.
2. **Kim, J.** (2025). Why online learning teams should read "Co-Intelligence". *Inside Higher Ed*. https://www.insidehighered.com/opinion/columns/learning-innovation/2025/03/18/why-online-learning-teams-should-read-co（访问 2026-08-06）
3. **UNESCO** (2023). *Guidance for Generative AI in Education and Research*. https://doi.org/10.54675/EWZM9535
4. **Mollick, E.** *One Useful Thing* (Substack). https://www.oneusefulthing.org/（持续更新的课堂实验，访问 2026-08-06）
