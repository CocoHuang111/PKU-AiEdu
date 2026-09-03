# 专家评分规则学习产物

本目录只放运行产物，不放实现代码，也不复制原始 xlsx。

| 文件/目录 | 生成阶段 | 用途 |
| --- | --- | --- |
| `source_manifest.json` | `ingest` | 原表文件名、内容哈希与记录数审计 |
| `expert_reviews_long.csv` | `ingest` | 一行一个“分数—评语”关系；不含邮箱、工号、电话 |
| `mentions/*.json` | `extract` | 每条评语的可恢复 LLM 原子抽取缓存；已 gitignore |
| `expert_mentions.jsonl` | `extract` | 原子观点合并文件；已 gitignore |
| `rule_candidates.csv/json` | `candidates/distill` | 问题被提及时的分数条件、支持量和反例 |
| `rules_candidate.yaml` | `distill` | 默认 `approved: false` 的待审核规则 |
| `rule_audit.md` | `distill` | 面向人工确认的统计和规则清单 |

只有在 `rules_candidate.yaml` 中明确改为 `approved: true` 的规则，才会被
`python -m scripts.build_expert_rules freeze` 写入生产侧
`ai_engine/pedagogy/expert_rules.yaml`。

