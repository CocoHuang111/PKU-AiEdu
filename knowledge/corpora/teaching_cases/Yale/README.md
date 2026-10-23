# Yale

本目录保存 Yale Poorvu Center 的英文教学案例原文，不翻译、不改写。采集日期：2026-10-08。Open Yale Courses 已移动到 `knowledge/corpora/course_cases/Yale-OYC/`。

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
python3 scripts/crawl_other_cases.py --only poorvu
```

## 已知限制

Poorvu 新闻、纪念、年报和活动预告没有收进案例。本次没有 `make ingest`。
