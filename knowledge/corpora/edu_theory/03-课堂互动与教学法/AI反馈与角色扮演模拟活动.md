# AI 反馈与角色扮演模拟活动

> 用 AI 作苏格拉底对话者、历史人物或学科专家，支持课堂互动与形成性评价。

**文献性质**：课堂教学法 + 专著活动设计归纳  
**核心出处**：Bowen & Watson (2024) Ch.9；Mollick (2024)；AIMES 实践方向  
**整理说明**：活动流程与 prompt 模板据 Bowen & Watson 及 Mollick 课堂实验归纳。  
**核实日期**：2026-08-06

---

## 来源标注说明

Roleplaying with AI 见 Bowen & Watson [1]；coach 角色见 Mollick [2]。

## 适用 learning goals

- 口头论证、倾听与追问  
- 理解多元视角（历史/伦理/政策）  
- **评改** AI 输出而非照搬  
- 低 stakes 练习后再做 summative 口试  

**不适用**：替代应独立完成的 summative；替代 L2 学生的语言能力证明（需 policy 协调）。

## 三类标准模式

| 模式 | AI 角色 | 学生任务 | 评价焦点 |
| --- | --- | --- | --- |
| **苏格拉底追问** | 只提问、不给答案 | 口头或文字 defend 观点 | 论证链、回应追问 |
| **历史人物/专家对话** | 限定知识边界的 persona | 10 轮对话 + 反思 | 对话质量、史实/概念错误识别 |
| **挑剔审稿人** | peer reviewer | 带 draft 接受批评并修订 | 修订理由、是否采纳 AI 建议 |

## 模式 1：苏格拉底追问（15–25 分钟）

**流程**：

1. 学生提交 200 字 thesis 或问题（可课前完成）。
2. AI prompt（教师提供模板）：

```text
你是苏格拉底式对话者。学生论点如下：[粘贴]
规则：① 每次只问 1 个问题 ② 不给出结论或阅读清单 ③ 若学生逻辑跳跃，追问前提
生成 5 个递进问题。不要回答学生问题。
```

3. 学生书面或口头回答每问；可选：同伴互评。
4. 提交：问答记录 + 100 字「我修正了哪些前提」。

**AIAS 建议**：1–2（AI 不参与 final 论证文本）。

## 模式 2：历史人物 / 专家 roleplay（25–40 分钟）

Bowen & Watson 建议 [1]：有**较大原文语料**时效果更好；可要求 AI **仅引用可核查来源**（仍须学生核验）。

**流程**：

1. 设定 persona prompt：

```text
你扮演 [人物/角色]，时代/学科背景：[说明]
知识边界：仅讨论 [主题]；不确定时说「史料不足」
语气：[正式/口语]，不使用现代俚语
学生将 interview 你。每次回答不超过 120 字。
```

2. 学生进行 ≥8 轮对话。
3. 作业：① 对话导出 ② 标出 3 处 AI 可能不准确之处及核验方法 ③ 若换真实史料会如何修正回答。

**工具提示**：定制 GPT、Character.ai、HelloHistory.ai 等 — 选用须符合**数据隐私**校规；课堂可统一用机构批准工具。

**AIAS 建议**：2–3（AI 为对话对象，非 final essay 代写）。

## 模式 3：挑剔审稿人 + 修订（贯穿单元）

**流程**：

1. 学生 submit draft（AIAS 2–3）。
2. AI prompt：

```text
你是 [学科] 期刊审稿人。评分标准：[粘贴 rubric 摘要]
对以下 draft 写：① 3 条 major comments ② 5 条 minor comments
③ 不得重写全文，只指出问题与改进方向
[draft 粘贴]
```

3. 学生写 revision memo：逐条回应；标记接受/拒绝及理由。
4. 教师评：**revision 质量**，非 draft 初稿 polish 程度。

对齐 `04-评价与反馈/形成性评价与反馈原则.md`：feedback forward-looking。

## 模式 4：AI 模拟「患者/客户/谈判对手」（专业学位）

| 学科 | 模拟对象 | 评价 |
| --- | --- | --- |
| 医学教育 | 标准化患者式问诊 | 问诊结构、鉴别诊断思路 |
| 法学 | 当事人访谈 | 问题顺序、权利告知 |
| 商科 | 客户异议处理 | 沟通策略、伦理边界 |

**必须**：教师审校 scenario；**禁止**用真实患者/客户数据训练 prompt。

## 大班课缩放

| 策略 | 做法 |
| --- | --- |
| 分组 roleplay | 每组同一 scenario，组内轮流提问 |
| 抽样口试 | 随机 20% 做 live follow-up |
| 异步 | LMS 讨论区贴对话摘要 + 互评 |
| TA 协同 | AI 生成 scenario 库，TA 跑练习课 |

见 `03-课堂互动与教学法/大班课教学策略.md` 与本文互补。

## Policy 与诚信

- Syllabus 写明：对话可 AI 生成，**reflection 与口试须本人**。
- 要求保存 transcript 作为 process evidence。
- 历史人物对话**不等于**史学考证 — rubric 评「批判性使用 AI」。

## 边界与风险

- Persona AI 易**幻觉**史实或判例 — 必须设「核验」作业环节。
- 角色扮演对内向/ESL 学生压力不同 — 提供 written alternative。
- 商业角色扮演产品可能有**数据留存** — 优先机构工具。

## 参考文献与可追溯来源

1. **Bowen, J. A., & Watson, C. E.** (2024). *Teaching with AI*. Johns Hopkins University Press. ISBN 978-1-4214-4674-7（Ch.9 Feedback and Roleplaying with AI）
2. **Mollick, E.** (2024). *Co-Intelligence*. Portfolio/Penguin. ISBN 978-0-593-71671-7.
3. **Stanford CTL**. AIMES AI Teaching Strategies. https://ctl.stanford.edu/aimes/ai-teaching-strategies（访问 2026-08-06）
4. **Perkins, M., et al.** (2024). *The Artificial Intelligence Assessment Scale (AIAS)*. https://doi.org/10.53761/q3azde36
