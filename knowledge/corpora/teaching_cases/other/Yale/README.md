# Yale

本目录有两套英文原文，都不翻译、不改写。采集日期：2026-10-08。原先的中文改写稿和 `source/` HTML 已经不在这里。

## Open Yale Courses

目录：`oyc/`。课程清单来自 <https://oyc.yale.edu/courses>，共 **40** 门。课次页 **1060** 个，Markdown **1100** 份（每门另有 `course-description.md`）。全部 `extraction_status: complete`。名单在 `oyc/catalog.jsonl`。

```text
oyc/courses/<course-slug>/
├── course.yaml
├── resources.jsonl
├── course-description.md
└── lecture-N.md / exam-N.md / 其他课次文件名
```

课次文件名是来源 URL 的最后一段。天文课两节后来补上的讲座在 `/node/1855` 和 `/node/1856`，文件名是 `1855.md`、`1856.md`。建筑课的论文题页是 `paper-topics.md`。

每篇开头是中文检索摘要，其中一句根据该页 Overview 或课程介绍写成主要内容。`---` 以下是英文原文，含页面上的 HTML 讲稿。`content_sha256` 只覆盖原文，不含检索摘要。音频、视频和 PDF 不下载，链接留在正文和 `resources.jsonl`。

`course.yaml` 里：

- `course_codes`、`professors`、`description` 来自课程主页上的 Course Number、Professor、About the Course。姓名和职衔在页面上是同一栏，所以写在同一个字符串里。
- `department_path` 是课程主页 URL 的第一段，连字符换成空格。心理学导论的主页在 `/introduction-psychology/psyc-110`，这一栏是 `introduction psychology`。课次链接有时在另一条路径下，例如 `/psychology/psyc-110/lecture-1`。
- `topic_keywords`、`pedagogy_tags`、`assessment_types` 留空。

天文课 Lecture 25、Lecture 26 的页面本身只有概述，讲稿表格里没有正文。文件按页面保存。

## Poorvu Center

目录：`poorvu/`。Poorvu 的 `/posts/` 是中心新闻流。这里只保留写课程、课堂活动或教学合作的 **14** 篇。名单在 `poorvu/catalog.jsonl`。另外 19 个新闻 URL 记在 `poorvu/skipped_news.txt`，没有正文。

```text
poorvu/cases/<slug>/
├── case.yaml
├── resources.jsonl
└── case.md
```

Poorvu 的案例页也是同一写法：检索摘要里有一句根据正文写成的主要内容，分隔线后是英文原文。

## 续跑

在项目根目录执行。`course.yaml` 或 `case.yaml` 里 `extraction_status` 为 `complete` 的会跳过。

```bash
python3 scripts/crawl_other_cases.py --only oyc
python3 scripts/crawl_other_cases.py --only poorvu
```

## 已知限制

Open Yale Courses 的音频和 PDF 只有 URL。Poorvu 新闻、纪念、年报和活动预告没有收进案例。本次没有 `make ingest`。
