"""让 LLM 仅根据五维诊断和客观特征独立判总分，再与专家/GB 做盲后对照。

评分请求构造阶段不会读取专家标签、专家评语或 GB 预测；所有 LLM 输出落盘后，
比较阶段才读取 gb_predictions.csv，防止标签泄漏。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.judge import _parse_json  # noqa: E402
from ai_engine.evaluation.gb import SCORE_MAPPING_VERSION  # noqa: E402
from ai_engine.evaluation.pipeline import _objective_rows  # noqa: E402
from ai_engine.pedagogy.loader import PROMPT_DIR, render_prompt  # noqa: E402
from ai_engine.providers import ChatMessage, ProviderError, get_llm  # noqa: E402

SYSTEM = "你是严谨的高校教学质量评估专家。你只能输出合法 JSON。"
PROMPT_NAME = "eval_overall_judge.j2"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _fingerprint(prompt_version: str) -> str:
    h = hashlib.sha256()
    h.update((PROMPT_DIR / PROMPT_NAME).read_bytes())
    h.update(prompt_version.encode("utf-8"))
    return h.hexdigest()[:16]


def _dimension_context(scores: dict[str, Any]) -> list[dict[str, Any]]:
    """只暴露评分诊断字段，明确排除报告、专家信息和其他缓存内容。"""
    out = []
    for d in scores.get("dimensions") or []:
        if not d.get("assessed") or d.get("score") is None:
            continue
        out.append(
            {
                "key": d.get("key"),
                "label": d.get("label"),
                "score": d.get("score"),
                "score_basis": d.get("score_basis") or d.get("score_source"),
                "confidence": d.get("dimension_confidence"),
                "rationale": d.get("dimension_rationale"),
                "primary_issue": d.get("primary_issue"),
                "severity": d.get("severity"),
            }
        )
    return out


def build_blind_prompt(evidence: dict[str, Any], scores: dict[str, Any]) -> str:
    """构造不含专家标签、评语和 GB 预测的评分 Prompt。"""
    return render_prompt(
        PROMPT_NAME,
        dimensions=_dimension_context(scores),
        objective_features=_objective_rows(evidence.get("raw_features") or {}),
    )


def _normalize_result(parsed: Any) -> dict[str, Any]:
    if not isinstance(parsed, dict):
        raise ValueError("模型输出不是 JSON 对象")
    try:
        score = float(parsed.get("overall_score_5"))
    except (TypeError, ValueError) as exc:
        raise ValueError("模型未返回有效 overall_score_5") from exc
    if not math.isfinite(score) or not 0 <= score <= 5:
        raise ValueError(f"overall_score_5 越界：{score}")
    confidence = str(parsed.get("confidence") or "medium").strip()
    if confidence not in {"high", "medium", "low"}:
        confidence = "medium"
    return {
        "overall_score_5": round(score, 2),
        "overall_score_100": round(score * 20, 1),
        "confidence": confidence,
        "main_strengths": list(parsed.get("main_strengths") or [])[:3],
        "main_issues": list(parsed.get("main_issues") or [])[:3],
        "decisive_evidence": list(parsed.get("decisive_evidence") or [])[:5],
        "counterevidence_protection": str(
            parsed.get("counterevidence_protection") or ""
        ).strip(),
        "rationale": str(parsed.get("rationale") or "").strip(),
    }


def score_test_set(args: argparse.Namespace) -> tuple[list[str], int]:
    """先完成全部盲评分；此函数绝不读取专家/GB 对照表。"""
    batch = Path(args.dir).resolve()
    split = _load_json(Path(args.split))
    test_ids = [str(x) for x in split.get("test_ids") or []]
    if not test_ids:
        raise SystemExit("split 中没有 test_ids")

    out_dir = Path(args.out_dir).resolve()
    cache_dir = out_dir / "cache"
    fingerprint = _fingerprint(args.prompt_version)
    llm = get_llm()
    failed = 0

    for index, video_id in enumerate(test_ids, start=1):
        result_path = cache_dir / f"{video_id}.json"
        if args.resume and result_path.exists():
            old = _load_json(result_path)
            if old.get("overall_judge_fingerprint") == fingerprint:
                print(f"[{index}/{len(test_ids)}] 复用 {video_id}")
                continue

        evidence_path = batch / "cache" / video_id / "evidence.json"
        scores_path = batch / args.scores_cache / video_id / "scores.json"
        if not evidence_path.exists() or not scores_path.exists():
            print(f"[{index}/{len(test_ids)}] 跳过 {video_id}：缺 evidence 或 scores")
            failed += 1
            continue

        # 注意：到 LLM 请求完成为止，只读取 evidence 和 scores。
        prompt = build_blind_prompt(_load_json(evidence_path), _load_json(scores_path))
        print(f"[{index}/{len(test_ids)}] LLM 综合判分 {video_id}", flush=True)
        try:
            raw = llm.chat(
                [ChatMessage("system", SYSTEM), ChatMessage("user", prompt)]
            )
            result = _normalize_result(_parse_json(raw))
            result.update(
                {
                    "video_id": video_id,
                    "prompt_version": args.prompt_version,
                    "overall_judge_fingerprint": fingerprint,
                }
            )
            _dump_json(result_path, result)
            print(f"  → {result['overall_score_5']:.2f}/5")
        except (ProviderError, ValueError) as exc:
            failed += 1
            _dump_json(
                cache_dir / f"{video_id}.error.json",
                {"video_id": video_id, "error": str(exc)},
            )
            print(f"  失败：{exc}")
    return test_ids, failed


def compare_after_scoring(args: argparse.Namespace, test_ids: list[str]) -> None:
    """盲评分全部落盘后，才读取含专家标签和 GB 预测的宽表。"""
    out_dir = Path(args.out_dir).resolve()
    gb_rows = {r["video_id"]: r for r in _read_csv(Path(args.gb_predictions))}
    if any(
        row.get("score_mapping_version") != SCORE_MAPPING_VERSION
        for row in gb_rows.values()
    ):
        raise SystemExit("GB 对照表使用旧专家分制，请先按修正后的 4 分制重新训练")
    detail_rows = {
        r["video_id"]: r for r in _read_csv(Path(args.expert_detail))
    }
    baseline_cols = [
        "judge_equal_avg_5",
        "pred_obj_reg",
        "pred_llm_reg",
        "pred_llm_cls5",
        "pred_llm_cls8",
    ]
    rows: list[dict[str, Any]] = []

    for video_id in test_ids:
        result_path = out_dir / "cache" / f"{video_id}.json"
        if not result_path.exists() or video_id not in gb_rows:
            continue
        result = _load_json(result_path)
        source = gb_rows[video_id]
        detail = detail_rows.get(video_id, {})
        expert = float(source["expert_score_5"])
        llm_score = float(result["overall_score_5"])
        row: dict[str, Any] = {
            "video_id": video_id,
            "expert_score_5": round(expert, 4),
            "expert_comment": detail.get("comment", ""),
            "llm_overall_score_5": round(llm_score, 4),
            "llm_abs_error_5": round(abs(llm_score - expert), 4),
            "llm_confidence": result.get("confidence", ""),
            "llm_rationale": result.get("rationale", ""),
            "judge_equal_avg_5": round(float(source["llm_overall_5"]), 4),
        }
        row["judge_equal_avg_5_abs_error_5"] = round(
            abs(float(row["judge_equal_avg_5"]) - expert), 4
        )
        for col in baseline_cols[1:]:
            pred = float(source[col])
            row[col] = round(pred, 4)
            row[f"{col}_abs_error_5"] = round(abs(pred - expert), 4)
        rows.append(row)

    _write_csv(out_dir / "comparison.csv", rows)
    if not rows:
        raise SystemExit("没有可比较的完整结果")

    def error_metrics(prediction_column: str) -> dict[str, float]:
        errors = [
            float(row[prediction_column]) - float(row["expert_score_5"])
            for row in rows
        ]
        return {
            "mae": round(sum(abs(e) for e in errors) / len(errors), 4),
            "rmse": round(math.sqrt(sum(e * e for e in errors) / len(errors)), 4),
            "bias": round(sum(errors) / len(errors), 4),
        }

    summary = {
        "n_test": len(rows),
        "prompt_version": args.prompt_version,
        "metrics_5": {
            "llm_overall": error_metrics("llm_overall_score_5"),
            "judge_equal_avg": error_metrics("judge_equal_avg_5"),
            **{col: error_metrics(col) for col in baseline_cols[1:]},
        },
    }
    _dump_json(out_dir / "summary.json", summary)

    print("\n逐人对照（0–5）：")
    print(
        f"{'教师':<10} {'专家':>6} {'LLM总分':>8} {'绝对误差':>8} "
        f"{'等权Judge':>9} {'客+五':>7} {'五维回归':>8} {'5分类':>7} {'8分类':>7}"
    )
    for row in rows:
        print(
            f"{row['video_id']:<10} {row['expert_score_5']:>6.2f} "
            f"{row['llm_overall_score_5']:>8.2f} {row['llm_abs_error_5']:>8.2f} "
            f"{row['judge_equal_avg_5']:>9.2f} {row['pred_obj_reg']:>7.2f} "
            f"{row['pred_llm_reg']:>8.2f} "
            f"{row['pred_llm_cls5']:>7.2f} {row['pred_llm_cls8']:>7.2f}"
        )
    print("\nMAE：", json.dumps(summary, ensure_ascii=False))
    print(f"写 {out_dir / 'comparison.csv'}")
    print(f"写 {out_dir / 'summary.json'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="五维+客观特征 → LLM 独立综合总分")
    parser.add_argument("--dir", required=True, help="数据批次目录")
    parser.add_argument("--scores-cache", required=True, help="五维 scores.json 缓存目录名")
    parser.add_argument("--split", required=True, help="含 test_ids 的划分 JSON")
    parser.add_argument("--gb-predictions", required=True, help="GB 测试集预测宽表")
    parser.add_argument(
        "--expert-detail",
        required=True,
        help="含专家评语的 training_detail.csv；仅在盲评分完成后读取",
    )
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--prompt-version", default="overall-v1")
    parser.add_argument("--resume", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    test_ids, failed = score_test_set(args)
    if failed:
        print(f"盲评分失败 {failed} 人；修复后用 --resume 续跑，暂不生成对照表")
        return 1
    compare_after_scoring(args, test_ids)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
