"""从专家评分表学习可执行评分规则。

用法：
    python -m scripts.build_expert_rules ingest
    python -m scripts.build_expert_rules extract --resume
    python -m scripts.build_expert_rules distill
    python -m scripts.build_expert_rules freeze
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.eval_dataset.expert_rules import (  # noqa: E402
    build_rule_candidates,
    distill_rule_candidates,
    extract_mentions,
    freeze_approved_rules,
    ingest_expert_reviews,
)

DEFAULT_SOURCE = ROOT / "test" / "expert_judge"
DEFAULT_WORK = ROOT / "dataset" / "expert_rules"
DEFAULT_FROZEN = ROOT / "ai_engine" / "pedagogy" / "expert_rules.yaml"


def cmd_ingest(args: argparse.Namespace) -> int:
    rows = ingest_expert_reviews(Path(args.source), Path(args.out))
    usable = sum(bool(r["use_for_rule_learning"]) for r in rows)
    teachers = len({r["teacher_id"] for r in rows})
    print(f"写入 {len(rows)} 条评分记录，{usable} 条可学习，覆盖 {teachers} 位教师")
    print(Path(args.out) / "expert_reviews_long.csv")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    ok, skipped, failed = extract_mentions(
        Path(args.dir), resume=args.resume, limit=args.limit
    )
    print(f"原子观点抽取完成：新增 {ok}，复用 {skipped}，失败 {failed}")
    print(Path(args.dir) / "expert_mentions.jsonl")
    return 1 if failed else 0


def cmd_candidates(args: argparse.Namespace) -> int:
    rows = build_rule_candidates(Path(args.dir))
    print(f"生成 {len(rows)} 组问题统计")
    print(Path(args.dir) / "rule_candidates.csv")
    return 0


def cmd_distill(args: argparse.Namespace) -> int:
    rules = distill_rule_candidates(Path(args.dir))
    print(f"生成 {len(rules)} 条待审核规则；默认 approved=false，不会自动进入 Judge")
    print(Path(args.dir) / "rules_candidate.yaml")
    return 0


def cmd_freeze(args: argparse.Namespace) -> int:
    n = freeze_approved_rules(Path(args.candidate), Path(args.out))
    print(f"冻结 {n} 条已批准规则到 {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="专家评分表 → 可执行 Judge 规则")
    sub = p.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="四份评分表清洗成长表（不调用 LLM）")
    ingest.add_argument("--source", default=str(DEFAULT_SOURCE))
    ingest.add_argument("--out", default=str(DEFAULT_WORK))
    ingest.set_defaults(func=cmd_ingest)

    extract = sub.add_parser("extract", help="逐条评语拆成原子观点（调用 LLM）")
    extract.add_argument("--dir", default=str(DEFAULT_WORK))
    extract.add_argument("--resume", action="store_true")
    extract.add_argument("--limit", type=int, default=0)
    extract.set_defaults(func=cmd_extract)

    candidates = sub.add_parser("candidates", help="统计问题与分数条件（不调用 LLM）")
    candidates.add_argument("--dir", default=str(DEFAULT_WORK))
    candidates.set_defaults(func=cmd_candidates)

    distill = sub.add_parser("distill", help="生成结构化待审核规则（调用 LLM）")
    distill.add_argument("--dir", default=str(DEFAULT_WORK))
    distill.set_defaults(func=cmd_distill)

    freeze = sub.add_parser("freeze", help="仅冻结 approved=true 的规则")
    freeze.add_argument(
        "--candidate", default=str(DEFAULT_WORK / "rules_candidate.yaml")
    )
    freeze.add_argument("--out", default=str(DEFAULT_FROZEN))
    freeze.set_defaults(func=cmd_freeze)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
