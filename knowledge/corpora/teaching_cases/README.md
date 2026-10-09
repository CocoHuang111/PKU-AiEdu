# 高校教学案例库

本目录保存教学改革、教学策略与课堂干预案例；完整课程已移至相邻的 `course_cases/`。

- `PKU/`：北京大学教务部公开的优秀本科教学改革项目案例，以及公开教师教学专访。2016–2018 年汇编的整理稿按原文栏目写成设计思路、实施过程、实施成果、存在问题和可迁移场景。`source/` 保留教务部原始 PDF。
- `MIT-Open-Learning/`：MIT Open Learning 的 146 项 Residential Digital Innovations 教学创新资料，英文原文加中文检索摘要。
- `Cornell/`、`Columbia/`、`Michigan/` 与 `Yale/poorvu/`：各校来源页上的英文原文。每篇开头有中文检索摘要，`---` 以下是原文。

成效主要来自项目自述或课程反馈。原文没有对照研究时，北大整理稿不写成严格因果结论。MIT 和上述国外来源保存来源页原文，页内没有的字段留空。

## 当前规模

| 来源 | 数量 | 形态 |
| --- | ---: | --- |
| 北京大学教改与教师案例 | 32 | 中文整理稿。29 份汇编案例全覆盖，另含护理、医学免疫学、学习科学 3 例 |
| 北京大学课程思政档案 | 66 | 中文整理稿。课程可能与上一行重叠 |
| Cornell | 27 | 英文原文。Teaching Innovation Case Study Library |
| Columbia | 53 | 英文原文。49 篇 Teaching Transformations，另有 4 篇 CTL spotlight / announcement |
| Michigan | 35 | 英文原文。Provost's Teaching Innovation Prize，获奖年份 2019–2025 |
| Yale Poorvu Center | 14 | 英文原文。课程、课堂活动或教学合作的故事 |
| MIT Open Learning | 146 | 英文原文。Residential Digital Innovations，另有 146 份 `检索摘要.md` |

北大两行是中文整理稿，合计 **98**。MIT 与上述国外来源是来源页原文，单独计数。

**采集日期**：北大材料 2026-09-21 至 2026-09-22；Cornell、Columbia、Michigan 与 Yale Poorvu 为 2026-10-08；MIT Open Learning 为 2026-10-09。

向量库按案例只保存一条中文检索索引，命中后从本目录读取整个案例原文。当前 `teaching_cases` collection 已按这一规则全量重建；后续删除或迁移案例时仍应重建 collection，避免旧索引残留。
