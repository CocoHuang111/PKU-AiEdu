# Columbia Center for Teaching and Learning

本目录保存哥伦比亚大学教学中心教师案例的英文原文。正文不翻译、不改写。

采集日期：2026-10-08。

## 现在有什么

53 篇，全部 `extraction_status: complete`。名单在 `catalog.jsonl`。

| 集合 | 篇数 | 来源 |
| --- | ---: | --- |
| Teaching Transformations | 49 | <https://ctl.columbia.edu/transformations/faculty/> 下列出的教师页 |
| CTL spotlight or announcement | 4 | 案例库旧链接里、不在上面名单中的 4 个页面 |

这 4 个页面是：

- <https://ctl.columbia.edu/spotlight/rachel-cummings/>
- <https://ctl.columbia.edu/spotlight/sewell-chan-tollman/>
- <https://ctl.columbia.edu/announcements/faculty-spotlight-mary-ann-price/>
- <https://ctl.columbia.edu/announcements/techniques-for-just-in-time-teaching-in-a-medical-school-course/>

原先的 8 篇中文改写稿和 `source/` HTML 已经不在这个目录里。

## 一篇案例里有什么

```text
cases/<slug>/
├── case.yaml
├── resources.jsonl
└── case.md
```

写法与 Cornell 相同：检索摘要里有一句根据正文写成的主要内容，然后是英文原文。`content_sha256` 只覆盖原文。

`mona-boside` 和 `kapadia-marti` 两页没有可用的文字版一级标题，`title` 用的是正文里的第一个标题：Dr. Mona Boside, DDS；Dr. Amy Kapadia, PhD and Dr. Yamile Marti, PhD。

## 续跑

```bash
python3 scripts/crawl_other_cases.py --only columbia
```

已完成的案例会跳过。

## 已知限制

Faculty spotlights 总索引由页面脚本加载，这次没有把 CTL 公告站整站抓下来，只保留了 Transformations 名单和上面 4 个已经对上旧案例的页面。图片不下载。本次没有 `make ingest`。
