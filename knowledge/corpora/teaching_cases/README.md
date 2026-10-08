# 高校教学案例库

本目录有两类材料。

- `PKU/`：北京大学教务部公开的优秀本科教学改革项目案例，以及公开教师教学专访。2016–2018 年汇编的整理稿按原文栏目写成设计思路、实施过程、实施成果、存在问题和可迁移场景。`source/` 保留教务部原始 PDF。
- `MIT/`：MIT OpenCourseWare 课程库。2587 个课程版本都有目录；2582 门的英文原文已抽全，5 门只抽到一部分。说明见 `MIT/README.md`。
- `other/`：Cornell、Columbia、Michigan、Yale 来源页上的英文原文。每篇开头有一段中文检索摘要，其中一句是这页的主要内容；`---` 以下是原文。说明见各校 `README.md`。

成效主要来自项目自述或课程反馈。原文没有对照研究时，北大整理稿不写成严格因果结论。MIT 和 `other/` 保存来源页原文，页内没有的字段留空。

## 当前规模

| 来源 | 数量 | 形态 |
| --- | ---: | --- |
| 北京大学教改与教师案例 | 32 | 中文整理稿。29 份汇编案例全覆盖，另含护理、医学免疫学、学习科学 3 例 |
| 北京大学课程思政档案 | 66 | 中文整理稿。课程可能与上一行重叠 |
| Cornell | 27 | 英文原文。Teaching Innovation Case Study Library |
| Columbia | 53 | 英文原文。49 篇 Teaching Transformations，另有 4 篇 CTL spotlight / announcement |
| Michigan | 35 | 英文原文。Provost's Teaching Innovation Prize，获奖年份 2019–2025 |
| Yale Poorvu Center | 14 | 英文原文。课程、课堂活动或教学合作的故事 |
| Yale Open Yale Courses | 40 门课，1060 个课次，1100 份 Markdown | 英文原文。课程说明和课次页 |
| MIT OpenCourseWare | 2587 门目录，14663 份 Markdown | 英文原文。见 `MIT/README.md` |

北大两行是中文整理稿，合计 **98**。MIT 与 `other/` 是来源页原文，单独计数。

**采集日期**：北大材料 2026-09-21 至 2026-09-22。`other/` 为 2026-10-08。MIT 为 2026-10-03。

这些英文原文还没有写入向量库。问答要引用它们，需要再执行 `make ingest`。增量入库不会删掉库里已经不在磁盘上的旧块；若库里还留着以前的中文改写稿，应重建 `teaching_cases`。
