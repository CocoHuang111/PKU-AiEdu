# Open Yale Courses 课程库

本目录保存 Open Yale Courses 的英文原文，不翻译、不改写。采集日期：2026-10-08。

- 课程：40 门
- 课次页：1060 个
- 英文 Markdown：1100 份
- 中文检索摘要：40 份，每门课程一份
- 入口：<https://oyc.yale.edu/courses>

```text
courses/<course-slug>/
├── course.yaml
├── resources.jsonl
├── 检索摘要.md
├── course-description.md
└── lecture-N.md / exam-N.md / 其他课次文件
```

每篇英文页面开头只保留来源信息，分隔线以下为来源页原文；页面文件不重复写检索摘要。`content_sha256` 只覆盖英文原文。音频、视频与 PDF 不下载，来源地址保留在正文或 `resources.jsonl`。本次没有执行 RAG 入库。
