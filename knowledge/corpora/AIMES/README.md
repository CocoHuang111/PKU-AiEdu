# 斯坦福 AIMES 语料

整理自 [AI Meets Education at Stanford](https://ctl.stanford.edu/aimes)。每篇开头是中文内容概括和来源网址，正文保留英文原文的标题、列表和链接。访问日期 2026-10-02。

| 目录 | 内容 |
| --- | --- |
| `AI Teaching Strategies/` | 同一策略页拆成总览和三条路径。总览是导语和所有路径共用的策略；Assigning / Limiting / Prohibiting 三个文件只放该路径专属内容 |
| `AI Course Policies.md` | 课程 AI 政策页本身 |
| `AI and Your Learning - A Guide for Students.md` | 学生指南 |
| `AIMES co-leads reflect on progress and trends/` | 两篇共同负责人反思。同一页上的 Upcoming Opportunities for Engagement 未收录 |
| `Academic Technology Tools List/` | 32 个校级教学技术工具的 Teaching Commons 详情页 URL，不含详情页正文 |
| `AIMES Library/` | 案例库 41 条材料按课程合并为 25 个文件（含 1 份院系指导，不是一门课）。同一课程的多条材料写在同一文件里，每条保留自己的网址 |
| `Tool/` | 两部分：`产品访问入口.md` 是上述工具的产品或访问地址；其余文件是 AI Course Policies 页指向的外链资源正文 |

## 整理时的取舍

- `Technology, Innovation, and Great Power Competition` 与带 “the” 的标题是同一门课，合并进前一个文件名。
- 社区标准办公室的生成式 AI 指导挂在 BCA 指导汇编页上，`Tool/OCS Generative AI Policy Guidance.md` 只保留 Generative AI Policy Guidance 一节。
- CTL 大纲模板的示例条文在 [Google 文档](https://docs.google.com/document/d/15NUp5scC067RvQZUdHPUkVt5n-fyzmXcSLHQVSBBpy4/edit?usp=sharing) 里。`Tool/CTL Syllabus Template.md` 保留使用说明和文档地址，没有把文档正文拉下来。
- 学术诚信工作组主页主要是监考和考试后勤，四项政策结构已经写在 `AI Course Policies.md` 里。

入库：`make ingest`（增量）。本目录对应 `config.yaml` 里的语料库 `AIMES`。
