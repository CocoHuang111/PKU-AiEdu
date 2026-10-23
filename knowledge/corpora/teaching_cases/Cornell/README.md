# Cornell Teaching Innovation Case Study Library

本目录保存康奈尔教学创新案例库的英文原文，供课程匹配和来源追溯。正文不翻译、不改写。

采集日期：2026-10-08。入口：

- <https://teaching.cornell.edu/teaching-spotlight/teaching-innovation-case-study-library>
- <https://blogs.cornell.edu/teachingcasestudies/>

## 现在有什么

27 篇，全部 `extraction_status: complete`。名单在 `catalog.jsonl`。

原先按学科改写的 6 篇中文稿，以及 `source/` 里的原始 HTML，已经不在这个目录里。同一批页面上的其余案例也收了进来，包括 Creative Teaching Awards 的案例页。

## 一篇案例里有什么

```text
cases/<slug>/
├── case.yaml
├── resources.jsonl
└── case.md
```

`case.md` 开头是中文检索摘要：机构、标题、一句主要内容，以及页内标题。这一句只根据该页正文来写，不另加页面没有的事实。`---` 以下是英文原文。`resources.jsonl` 的 `content_sha256` 只覆盖这段原文，不含检索摘要。

页面上的事实表原来是嵌套的 `info-row`，正文里写成 **Category:**、**Instructor:** 这样的段落。`topic_keywords`、`pedagogy_tags`、`assessment_types` 留空，不从标题推断教学法或层次。

视频、图片和 PDF 不下载。链接留在正文和 `resources.jsonl` 里。

## 续跑

在项目根目录执行。已经标成 `complete` 且有 `case.md` 的案例会跳过。

```bash
python3 scripts/crawl_other_cases.py --only cornell
```

## 已知限制

案例库页面上的导航、短标题入口没有当成案例。PDF 和视频只有 URL。本次没有 `make ingest`。
