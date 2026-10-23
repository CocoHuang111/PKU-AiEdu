# Michigan Provost's Teaching Innovation Prize

本目录保存密歇根大学 CRLT「Provost's Teaching Innovation Prize」获奖页的英文原文。正文不翻译、不改写。

采集日期：2026-10-08。名单页：<https://crlt.umich.edu/tip-winners>。

## 现在有什么

35 篇，全部 `extraction_status: complete`。获奖年份写在名单页上，记在 `case.yaml` 的 `awarded_year`。

| 年份 | 篇数 |
| --- | ---: |
| 2025 | 5 |
| 2024 | 5 |
| 2023 | 5 |
| 2022 | 5 |
| 2021 | 6 |
| 2020 | 5 |
| 2019 | 4 |

原先按学科挑选的 4 篇中文改写稿和 `source/` HTML 已经不在这个目录里。能打开的名单第一页上的获奖页都收了，包括原先那 4 篇的来源页。

## 一篇案例里有什么

```text
cases/<slug>/
├── case.yaml
├── resources.jsonl
└── case.md
```

写法与 Cornell 相同，检索摘要里有一句根据正文写成的主要内容。幻灯片和 PDF 不下载，URL 留在 `resources.jsonl`。

## 续跑

CRLT 对脚本直接请求返回 HTTP 403。现有 35 篇来自浏览器打开名单页之后、在页面里取回的正文。抓取文件不在仓库里。文件还在时可以重跑，已完成的会跳过：

```bash
python3 scripts/crawl_other_cases.py --only michigan
```

抓取文件不在、但 `catalog.jsonl` 还在时，脚本会留下已保存的案例并跳过这一校。

## 已知限制

名单第二页 <https://crlt.umich.edu/tip-winners?page=1> 返回 HTTP 500。2018 年及更早的获奖页没有收进来，也没有根据搜索摘要补写。本次没有 `make ingest`。
