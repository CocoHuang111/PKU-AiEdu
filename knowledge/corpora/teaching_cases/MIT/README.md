# MIT OpenCourseWare 课程库

本目录服务于课程匹配、大纲参考、教学设计检索和来源追溯。正文保存 OCW 页面上的英文原文，不翻译、不改写。

采集日期：2026-10-03。来源站点：<https://ocw.mit.edu/>。课程清单来自 MIT 公开检索接口中 `platform=ocw` 的课程，共 **2587** 个课程版本。同一门课的不同学期分开保存。

## 现在有什么

| 内容 | 数量 | 状态 |
| --- | ---: | --- |
| 课程版本 | 2587 | 每门都有 `course.yaml`、`resources.jsonl`，以及实际存在的 Markdown |
| 正文抽取完整 | 2582 | `extraction_status: complete` |
| 正文只抽到一部分 | 5 | `extraction_status: partial`，见文末 |

Markdown 共 14663 份。常见文件数量：课程说明 2587、syllabus 2412、作业总览 1988、阅读 1775、日历 1690、讲义总览 1233、考试总览 516、项目总览 495、相关资源 440、教师说明 298。一门课没有的栏目仍然没有空文件。

页面上标明的层次（一门课可以同时属于两层，所以合计大于 2587）：本科 1378、研究生 1201、非学分 70、高中 11。另有 2 门页面没有写层次，31 门没有写开课院系。这两项都留空，没有按课程名称补。

`subject_primary` 使用 OCW 主题控件里的第一个子主题；页面没有子主题时，用第一个主题。`subject_secondary` 保留其余由页面给出的主题。`topic_keywords`、`pedagogy_tags`、`assessment_types` 为空，因为页面没有单独给出这些字段，脚本也不从课名推断。

## 一门课里有什么

```text
courses/<course-slug>/
├── course.yaml
├── resources.jsonl
└── 实际存在的 Markdown
```

Markdown 只在页面真有可提取正文时生成。没有 Calendar 就不会有 `calendar.md`。

每篇 Markdown 开头有一段中文检索摘要，只复述课号、标题、学期和页内标题。`---` 以下是英文原文。`resources.jsonl` 的 `content_sha256` 是这段原文的 SHA-256，不含检索摘要。

相对链接已改成绝对 URL。站点菜单、页眉和页脚没有写入正文。视频、音频、图片、PDF、压缩包和代码包不下载；总览页上的文件名、大小和 URL 会留在总览 Markdown 和 `resources.jsonl` 里。

作业、考试、讲义如果还有更深的 HTML 子页，这次只保存总览页和子页链接，没有把每一份子页正文再抓下来。

## 验收时看过的 20 门

全量抽取之前，先用这 20 门核对正文写法。它们按课程主页上排在第一位的开课院系选取，并尽量带有 syllabus。交叉列出的第二院系不拿来代表该院系。全量抽取之后，这 20 门仍在库里，没有另做一份。

| 课程 | 名称 | 学期 | 层次 | 第一开课院系 |
| --- | --- | --- | --- | --- |
| 6.006 | Introduction to Algorithms | Spring 2020 | 本科 | EECS |
| 18.404J | Theory of Computation | Fall 2020 | 本科、研究生 | Mathematics |
| 8.04 | Quantum Physics I | Spring 2013 | 本科 | Physics |
| 7.05 | General Biochemistry | Spring 2020 | 本科 | Biology |
| 5.73 | Quantum Mechanics I | Fall 2018 | 研究生 | Chemistry |
| 14.03 | Microeconomic Theory and Public Policy | Fall 2025 | 本科、研究生 | Economics |
| 15.015 | Macro and International Economics | Fall 2011 | 研究生 | Sloan School of Management |
| 4.602 | Modern Art and Mass Culture | Spring 2012 | 本科 | Architecture |
| 17.20 | Introduction to the American Political Process | Fall 2020 | 本科 | Political Science |
| 2.61 | Internal Combustion Engines | Spring 2017 | 研究生 | Mechanical Engineering |
| 21H.116J | The Civil War and Reconstruction | Fall 2005 | 本科 | History |
| 21L.009 | Shakespeare | Spring 2004 | 本科 | Literature |
| 9.35 | Perception | Spring 2024 | 本科 | Brain and Cognitive Sciences |
| 3.032 | Mechanical Behavior of Materials | Fall 2007 | 本科 | Materials Science and Engineering |
| 16.001 | Unified Engineering: Materials and Structures | Fall 2021 | 本科 | Aeronautics and Astronautics |
| 11.601 | Introduction to Environmental Policy and Planning | Fall 2016 | 研究生 | Urban Studies and Planning |
| 24.900 | Introduction to Linguistics | Fall 2012 | 本科 | Linguistics and Philosophy |
| 14.271 | Industrial Organization I | Fall 2022 | 研究生 | Economics；含 Instructor Insights |
| 14.15J | Networks | Spring 2018 | 本科 | Economics；含 Projects |
| RES.TLL-005 | How to Speak | January IAP 2018 | 非学分 | 页面未写院系 |

名单也写在 `_crawl/sample_slugs.txt`。`_crawl/` 是续跑用的接口缓存，不是课程正文。

## 续跑

在项目根目录执行。已完成的课程会跳过。`--rate` 要写在子命令前面。

```bash
python3 scripts/crawl_mit_ocw.py discover
python3 scripts/crawl_mit_ocw.py --rate 4 discover --workers 4
python3 scripts/crawl_mit_ocw.py extract --sample 20
python3 scripts/crawl_mit_ocw.py --rate 4 extract --all
```

`extract --all` 已在 2026-10-03 之后跑完。已标成 `complete` 的课会跳过；5 门 `partial` 再跑同一条命令时会整门重试。问答要引用这些正文，还需执行 `make ingest`。本次没有入库。

## 已知限制

- 许可信息来自页面上的 Creative Commons 链接。这批课程都能读到许可 URL；引用时以每门课 `course.yaml` 里的 `license_url` 为准。
- 导航里没有发现 syllabus 本身就是一个 `.pdf` 地址的课。脚本在响应内容为 PDF 时会抽取文本且不保存 PDF。
- 部分新页面把讲义和作业放在 `/lists/` 而不是 `/pages/`。总览文字和每个文件的 URL 已保存，PDF 原件未下载。
- OCW 表格里夹有多余的段落标签。脚本会先修表格再转成 Markdown；带合并单元格的表保留为 HTML 表。
- 5 门课没有抽全。6.803 的项目页、17.447 的考试页、21G.405 的一页相关资源正文太短，没有写成可靠正文。15.392 的课程主页跳到 `https://scalingventures.ai/`，课程说明抽不出来。21W.780 仍用旧的 `/sections/` 地址，大纲、阅读、日历和作业页找不到正文容器。这 5 门其余能抽到的页面已经保存。
