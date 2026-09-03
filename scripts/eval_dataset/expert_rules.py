"""专家评分表规则学习：长表清洗、原子观点抽取、候选规则统计与冻结。

原始 xlsx 只读。所有中间产物由 CLI 写入 ``dataset/expert_rules``，生产侧只读取
人工确认后的 ``ai_engine/pedagogy/expert_rules.yaml``。
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml

from .inventory import write_csv
from .xlsx import read_sheet_rows


ISSUE_TAXONOMY: dict[str, str] = {
    "goal_unclear": "教学目标或本节定位不清",
    "content_incomplete": "内容或知识闭环不完整",
    "logic_weak": "内容组织、衔接或逻辑不清",
    "summary_weak": "总结或收束不足",
    "depth_or_focus_weak": "重点难点、深度或详略不当",
    "accuracy_problem": "知识内容存在明确错误",
    "practice_link_weak": "理论联系实际不足",
    "frontier_weak": "学科前沿融入不足",
    "questioning_weak": "问题设计不足",
    "interaction_weak": "课堂互动不足",
    "inspiration_weak": "启发或思维引导不足",
    "ppt_overloaded": "课件文字或信息过载",
    "ppt_readability_weak": "课件布局、字号或可读性不足",
    "ppt_blackboard_coordination": "课件、板书与讲授配合不足",
    "read_slides": "照读课件或看稿过多",
    "fluency_weak": "讲解不够熟练或流畅",
    "pace_weak": "语速、节奏或时间控制不当",
    "expression_weak": "表达不清、不准确或冗余",
    "engagement_weak": "感染力、激情或生动性不足",
    "bearing_weak": "教态、表情、目光或动作不足",
    "classroom_management_weak": "课堂组织或管理不足",
    "audio_quality": "录音或声音质量问题",
    "video_quality": "画面、机位或拍摄质量问题",
    "other": "其他尚未归类问题",
}

DIMENSION_KEYS = {
    "teaching_attitude",
    "teaching_content",
    "teaching_method",
    "teaching_effect",
    "teaching_quality",
    "recording_only",
    "unknown",
}

PRODUCTION_DIMENSION_KEYS = {
    "teaching_attitude",
    "teaching_content",
    "teaching_method",
    "teaching_effect",
    "teaching_quality",
}

_META_WORDS = (
    "专家",
    "评语",
    "模型",
    "对齐",
    "听感",
    "参考评审",
    "综合考虑",
    "校准尺度",
    "勿打穿",
)


def _clean_row(row: dict[str, str]) -> dict[str, str]:
    return {str(k).strip(): str(v or "").strip() for k, v in row.items()}


def _float(value: Any) -> float | None:
    try:
        text = str(value or "").strip()
        return float(text) if text else None
    except (TypeError, ValueError):
        return None


def _score_100(score: float | None) -> float | None:
    if score is None:
        return None
    # 原表明确为满分 4 分、2 分及格；2 分对应百分制 50 分，不是 0 分。
    return round(score / 4.0 * 100.0, 2)


def _score_band(score: float | None) -> str:
    if score is None:
        return "unknown"
    if score < 3.0:
        return "low"
    if score < 3.5:
        return "middle"
    return "high"


def _review_text(strengths: str, issues: str) -> str:
    parts = []
    if strengths.strip():
        parts.append(f"突出优点：{strengths.strip()}")
    if issues.strip():
        parts.append(f"需要改进：{issues.strip()}")
    return "\n".join(parts)


def _record(
    *,
    batch: str,
    row_no: int,
    name: str,
    scope: str,
    score: float | None,
    teacher_avg: float | None,
    strengths: str = "",
    issues: str = "",
    review_text: str = "",
    expert_id: str = "",
    source_file: str,
    suffix: str = "",
) -> dict[str, Any]:
    body = review_text.strip() or _review_text(strengths, issues)
    safe_suffix = suffix or (expert_id if expert_id else scope)
    record_id = f"{batch}_{row_no:04d}_{safe_suffix}".replace("/", "_")
    return {
        "record_id": record_id,
        "teacher_id": f"{batch}:{name}",
        "source_batch": batch,
        "source_file": source_file,
        "source_row": row_no,
        "name": name,
        "review_scope": scope,
        "expert_id": expert_id,
        "score_raw": score if score is not None else "",
        "score_100": _score_100(score) if score is not None else "",
        "score_band": _score_band(score),
        "teacher_avg": teacher_avg if teacher_avg is not None else "",
        "strengths_text": strengths.strip(),
        "issues_text": issues.strip(),
        "review_text": body,
        "has_comment": bool(body),
        "use_for_rule_learning": bool(body and score is not None),
    }


def _normalize_2018(path: Path) -> list[dict[str, Any]]:
    out = []
    for i, raw in enumerate(read_sheet_rows(path), start=2):
        row = _clean_row(raw)
        name = row.get("姓名", "")
        score = _float(row.get("平均分"))
        if not name or score is None:
            continue
        out.append(
            _record(
                batch="2018",
                row_no=i,
                name=name,
                scope="aggregate",
                score=score,
                teacher_avg=score,
                review_text=row.get("评语", ""),
                source_file=path.name,
            )
        )
    return out


def _normalize_2019(path: Path) -> list[dict[str, Any]]:
    out = []
    for i, raw in enumerate(read_sheet_rows(path), start=2):
        row = _clean_row(raw)
        name = row.get("姓名", "")
        score = _float(row.get("平均分"))
        if not name or score is None:
            continue
        out.append(
            _record(
                batch="2019",
                row_no=i,
                name=name,
                scope="aggregate",
                score=score,
                teacher_avg=score,
                strengths=row.get("整体优点", ""),
                issues=row.get("需要改进", ""),
                source_file=path.name,
            )
        )
    return out


def _normalize_2022(path: Path) -> list[dict[str, Any]]:
    rows = [_clean_row(r) for r in read_sheet_rows(path, keep_blank_names=True)]
    current_name = ""
    current_avg: float | None = None
    out = []
    for i, row in enumerate(rows, start=2):
        if row.get("姓名"):
            current_name = row["姓名"]
            current_avg = _float(row.get("平均分数"))
        elif _float(row.get("平均分数")) is not None:
            current_avg = _float(row.get("平均分数"))
        score = _float(row.get("总体评价（满分4分，2分及格）"))
        expert = row.get("专家", "")
        if not current_name or score is None:
            continue
        out.append(
            _record(
                batch="2022",
                row_no=i,
                name=current_name,
                scope="individual",
                expert_id=expert,
                score=score,
                teacher_avg=current_avg,
                strengths=row.get("突出优点", ""),
                issues=row.get("需要改进", ""),
                source_file=path.name,
            )
        )
    return out


def _normalize_2024(path: Path) -> list[dict[str, Any]]:
    rows = [_clean_row(r) for r in read_sheet_rows(path, keep_blank_names=True)]
    current_name = ""
    current_avg: float | None = None
    out = []
    for i, row in enumerate(rows, start=2):
        if row.get("姓名"):
            current_name = row["姓名"]
            current_avg = _float(row.get("平均分"))
        elif _float(row.get("平均分")) is not None:
            current_avg = _float(row.get("平均分"))
        score = _float(row.get("分数"))
        expert = row.get("专家账号", "")
        remark = row.get("备注", "")
        if current_name and score is not None:
            out.append(
                _record(
                    batch="2024",
                    row_no=i,
                    name=current_name,
                    scope="individual",
                    expert_id=expert,
                    score=score,
                    teacher_avg=current_avg,
                    review_text=remark,
                    source_file=path.name,
                )
            )
        summary = row.get("汇总评语-ZX", "")
        if current_name and current_avg is not None and summary:
            out.append(
                _record(
                    batch="2024",
                    row_no=i,
                    name=current_name,
                    scope="aggregate",
                    score=current_avg,
                    teacher_avg=current_avg,
                    review_text=summary,
                    source_file=path.name,
                    suffix="summary",
                )
            )
    return out


def discover_workbooks(source_dir: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in sorted(source_dir.glob("*.xlsx")):
        if path.name.startswith((".~", "~$")):
            continue
        name = path.name
        if "2018" in name:
            found["2018"] = path
        elif "2019" in name:
            found["2019"] = path
        elif "2022" in name:
            found["2022"] = path
        elif "24春" in name or "2024" in name:
            found["2024"] = path
    missing = [year for year in ("2018", "2019", "2022", "2024") if year not in found]
    if missing:
        raise FileNotFoundError(f"缺少评分表：{', '.join(missing)}；目录={source_dir}")
    return found


def _add_evaluator_calibration(rows: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        score = _float(row.get("score_raw"))
        if score is None:
            continue
        evaluator = row["expert_id"] or "aggregate"
        groups[(row["source_batch"], evaluator)].append(score)
    for row in rows:
        score = _float(row.get("score_raw"))
        evaluator = row["expert_id"] or "aggregate"
        values = sorted(groups.get((row["source_batch"], evaluator), []))
        if score is None or not values:
            row["evaluator_mean"] = ""
            row["evaluator_delta"] = ""
            row["evaluator_percentile"] = ""
            continue
        mean = statistics.fmean(values)
        less = sum(v < score for v in values)
        equal = sum(v == score for v in values)
        percentile = (less + 0.5 * equal) / len(values)
        row["evaluator_mean"] = round(mean, 4)
        row["evaluator_delta"] = round(score - mean, 4)
        row["evaluator_percentile"] = round(percentile, 4)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ingest_expert_reviews(source_dir: Path, out_dir: Path) -> list[dict[str, Any]]:
    books = discover_workbooks(source_dir)
    rows = []
    rows.extend(_normalize_2018(books["2018"]))
    rows.extend(_normalize_2019(books["2019"]))
    rows.extend(_normalize_2022(books["2022"]))
    rows.extend(_normalize_2024(books["2024"]))
    _add_evaluator_calibration(rows)
    rows.sort(key=lambda r: (r["source_batch"], r["source_row"], r["record_id"]))

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "expert_reviews_long.csv", rows)
    manifest = {
        "created_at": time.time(),
        "sources": {
            year: {"file": path.name, "sha256": _sha256(path)}
            for year, path in books.items()
        },
        "counts": {
            "records": len(rows),
            "usable_reviews": sum(bool(r["use_for_rule_learning"]) for r in rows),
            "teachers": len({r["teacher_id"] for r in rows}),
            "by_batch_scope": dict(
                Counter(f"{r['source_batch']}:{r['review_scope']}" for r in rows)
            ),
        },
    }
    (out_dir / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return rows


def read_long_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _format_duration(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}小时{minutes:02d}分"
    if minutes:
        return f"{minutes}分{secs:02d}秒"
    return f"{secs}秒"


def _normalize_mention(item: dict[str, Any]) -> dict[str, Any] | None:
    polarity = str(item.get("polarity") or "").strip()
    if polarity not in {"strength", "issue"}:
        return None
    issue_key = str(item.get("issue_key") or "other").strip()
    if issue_key not in ISSUE_TAXONOMY:
        issue_key = "other"
    dimension = str(item.get("dimension_key") or "unknown").strip()
    if dimension not in DIMENSION_KEYS:
        dimension = "unknown"
    modalities = item.get("observable_modalities") or []
    if not isinstance(modalities, list):
        modalities = []
    modalities = [m for m in modalities if m in {"text", "audio", "vision", "courseware", "speakers"}]
    return {
        "polarity": polarity,
        "issue_key": issue_key,
        "normalized_label": str(item.get("normalized_label") or ISSUE_TAXONOMY[issue_key]).strip(),
        "dimension_key": dimension,
        "indicator_key": str(item.get("indicator_key") or "").strip(),
        "stance": str(item.get("stance") or "neutral").strip(),
        "observable_modalities": modalities,
        "format_dependent": bool(item.get("format_dependent")),
        "executable": bool(item.get("executable", True)),
        "observable_condition": str(item.get("observable_condition") or "").strip(),
        "evidence_phrase": str(item.get("evidence_phrase") or "").strip()[:120],
    }


def extract_mentions(
    work_dir: Path, *, resume: bool = False, limit: int = 0
) -> tuple[int, int, int]:
    """逐条调用 LLM，产出可恢复的 mentions/*.json 和合并 JSONL。"""
    from ai_engine.evaluation.judge import _parse_json
    from ai_engine.pedagogy.loader import render_prompt
    from ai_engine.providers import ChatMessage, ProviderError, get_llm

    rows = [
        r
        for r in read_long_csv(work_dir / "expert_reviews_long.csv")
        if str(r.get("use_for_rule_learning", "")).lower() in {"true", "1"}
    ]
    if limit:
        rows = rows[:limit]
    out_dir = work_dir / "mentions"
    out_dir.mkdir(parents=True, exist_ok=True)
    llm = get_llm()
    ok = skipped = failed = 0
    valid_cache: set[str] = set()
    if resume:
        for row in rows:
            path = out_dir / f"{row['record_id']}.json"
            if not path.exists():
                continue
            try:
                old = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not old.get("error"):
                valid_cache.add(row["record_id"])
    pending_total = len(rows) - len(valid_cache)
    print(
        f"待分析 {len(rows)} 条：已有有效缓存 {len(valid_cache)}，"
        f"本次需调用 LLM {pending_total} 条。",
        flush=True,
    )
    call_durations: list[float] = []
    attempted = 0
    for index, row in enumerate(rows, start=1):
        out_path = out_dir / f"{row['record_id']}.json"
        label = row.get("name") or row["record_id"]
        expert = row.get("expert_id") or row.get("review_scope") or ""
        if row["record_id"] in valid_cache:
            skipped += 1
            print(f"[{index}/{len(rows)}] 复用缓存  {label} · {expert}", flush=True)
            continue
        attempted += 1
        print(f"[{index}/{len(rows)}] 正在分析  {label} · {expert} ...", flush=True)
        started = time.monotonic()
        prompt = render_prompt(
            "expert_review_extract.j2",
            row=row,
            taxonomy=ISSUE_TAXONOMY,
        )
        try:
            raw = llm.chat(
                [
                    ChatMessage(
                        "system",
                        "你只输出合法 JSON。拆分原子观点，不生成评分规则，不臆测未写出的缺点。",
                    ),
                    ChatMessage("user", prompt),
                ]
            )
            parsed = _parse_json(raw)
            items = parsed.get("mentions", []) if isinstance(parsed, dict) else []
            mentions = [m for x in items if isinstance(x, dict) if (m := _normalize_mention(x))]
            result = {"record": row, "mentions": mentions, "created_at": time.time()}
        except ValueError:
            result = {"record": row, "mentions": [], "error": "parse", "raw": raw[:1000]}
            failed += 1
        except ProviderError as exc:
            result = {"record": row, "mentions": [], "error": "provider", "detail": str(exc)}
            failed += 1
        _dump_json(out_path, result)
        elapsed = time.monotonic() - started
        call_durations.append(elapsed)
        remaining = max(0, pending_total - attempted)
        eta = statistics.fmean(call_durations) * remaining if call_durations else 0
        if not result.get("error"):
            ok += 1
            print(
                f"             完成：{len(result['mentions'])} 个观点，"
                f"耗时 {_format_duration(elapsed)}，预计剩余 {_format_duration(eta)}",
                flush=True,
            )
        else:
            detail = str(result.get("detail") or result.get("error") or "")[:120]
            print(
                f"             失败：{detail}；已写错误缓存，下次 --resume 会重试。",
                flush=True,
            )
    combine_mentions(work_dir)
    return ok, skipped, failed


def combine_mentions(work_dir: Path) -> int:
    files = sorted((work_dir / "mentions").glob("*.json"))
    lines = []
    for path in files:
        try:
            lines.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            continue
    with (work_dir / "expert_mentions.jsonl").open("w", encoding="utf-8") as f:
        for item in lines:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return len(lines)


def _median(values: Iterable[float]) -> float | None:
    vals = list(values)
    return round(statistics.median(vals), 4) if vals else None


def build_rule_candidates(work_dir: Path) -> list[dict[str, Any]]:
    path = work_dir / "expert_mentions.jsonl"
    grouped: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            record = data.get("record") or {}
            for mention in data.get("mentions") or []:
                if mention.get("polarity") != "issue" or not mention.get("executable"):
                    continue
                grouped[mention.get("issue_key", "other")].append((record, mention))

    candidates = []
    for issue_key, pairs in sorted(grouped.items()):
        by_teacher: dict[str, list[float]] = defaultdict(list)
        record_scores = []
        deltas = []
        examples = []
        dimensions = Counter()
        for record, mention in pairs:
            score = _float(record.get("score_raw"))
            if score is None:
                continue
            by_teacher[record["teacher_id"]].append(score)
            record_scores.append(score)
            delta = _float(record.get("evaluator_delta"))
            if delta is not None:
                deltas.append(delta)
            dimensions[mention.get("dimension_key", "unknown")] += 1
            phrase = mention.get("evidence_phrase") or ""
            if phrase and len(examples) < 8:
                examples.append(
                    {
                        "score": score,
                        "band": _score_band(score),
                        "text": phrase,
                        "condition": mention.get("observable_condition", ""),
                    }
                )
        teacher_scores = [statistics.fmean(v) for v in by_teacher.values()]
        n_teachers = len(teacher_scores)
        high_share = sum(v >= 3.5 for v in teacher_scores) / n_teachers if n_teachers else 0.0
        low_share = sum(v < 3.0 for v in teacher_scores) / n_teachers if n_teachers else 0.0
        if n_teachers < 3 or len(record_scores) < 5:
            severity = "insufficient_evidence"
        elif high_share >= 0.5 and low_share <= 0.2:
            severity = "improvement_only"
        elif low_share >= 0.5 and high_share <= 0.2:
            severity = "major_issue"
        else:
            severity = "context_dependent"
        candidates.append(
            {
                "issue_key": issue_key,
                "label": ISSUE_TAXONOMY.get(issue_key, issue_key),
                "primary_dimension": dimensions.most_common(1)[0][0] if dimensions else "unknown",
                "n_records": len(record_scores),
                "n_teachers": n_teachers,
                "median_score": _median(teacher_scores),
                "high_score_share": round(high_share, 4),
                "low_score_share": round(low_share, 4),
                "mean_evaluator_delta": round(statistics.fmean(deltas), 4) if deltas else None,
                "suggested_severity": severity,
                "examples": examples,
            }
        )
    csv_rows = [{k: v for k, v in c.items() if k != "examples"} for c in candidates]
    write_csv(work_dir / "rule_candidates.csv", csv_rows)
    _dump_json(work_dir / "rule_candidates.json", candidates)
    return candidates


def _rule_is_actionable(rule: dict[str, Any]) -> bool:
    text = json.dumps(rule, ensure_ascii=False)
    if any(word in text for word in _META_WORDS):
        return False
    required = ("rule_id", "target_dimension", "phenomenon", "scoring_action")
    return all(str(rule.get(k) or "").strip() for k in required)


def _production_rule_errors(rule: dict[str, Any]) -> list[str]:
    errors = []
    rule_id = str(rule.get("rule_id") or "<unknown>")
    for field in ("target_dimension", "primary_dimension"):
        value = str(rule.get(field) or "").strip()
        if value not in PRODUCTION_DIMENSION_KEYS:
            errors.append(f"{rule_id}.{field}={value!r} 不是合法五维 key")
    invalid_exclusions = sorted(
        set(rule.get("must_not_penalize_dimensions") or []) - PRODUCTION_DIMENSION_KEYS
    )
    if invalid_exclusions:
        errors.append(
            f"{rule_id}.must_not_penalize_dimensions 含非法 key: {invalid_exclusions}"
        )
    return errors


def _remove_legacy_score_floor(rule: dict[str, Any]) -> None:
    """把旧候选规则中的 70 分软地板迁移为可累计的证据规则。"""
    action = str(rule.get("scoring_action") or "")
    action = action.replace(
        "不可作为导致该维度低于70分的唯一理由",
        "通常只产生2–5分影响，但不存在70分或其他固定下限；"
        "同一维度多个相互独立且证据充分的问题必须累计",
    )
    action = action.replace(
        "允许导致该维度低于70分",
        "一个严重问题或与本维其他独立问题累计时，允许导致该维度低于60分",
    )
    rule["scoring_action"] = action


def distill_rule_candidates(work_dir: Path) -> list[dict[str, Any]]:
    from ai_engine.evaluation.judge import _parse_json
    from ai_engine.pedagogy.loader import render_prompt
    from ai_engine.providers import ChatMessage, get_llm

    candidates = build_rule_candidates(work_dir)
    usable = [c for c in candidates if c["suggested_severity"] != "insufficient_evidence"]
    if not usable:
        raise ValueError("没有达到最小支持量的规则候选，不能调用 distill")
    prompt = render_prompt(
        "expert_rule_distill.j2",
        candidates_json=json.dumps(usable, ensure_ascii=False, indent=2),
    )
    raw = get_llm().chat(
        [
            ChatMessage(
                "system",
                "你只输出合法 JSON。规则必须在未来没有专家分数和评语时仅凭视频证据执行。",
            ),
            ChatMessage("user", prompt),
        ]
    )
    parsed = _parse_json(raw)
    items = parsed.get("rules", []) if isinstance(parsed, dict) else []
    support_by_key = {c["issue_key"]: c for c in usable}
    rules = []
    for item in items:
        if not isinstance(item, dict):
            continue
        item["approved"] = False
        support = support_by_key.get(str(item.get("support_issue_key") or ""))
        if support:
            item["support"] = {
                "n_records": support["n_records"],
                "n_teachers": support["n_teachers"],
                "median_score": support["median_score"],
                "high_score_share": support["high_score_share"],
                "low_score_share": support["low_score_share"],
                "suggested_severity": support["suggested_severity"],
            }
        if _rule_is_actionable(item):
            rules.append(item)
    payload = {
        "version": "candidate-v1",
        "created_at": time.time(),
        "approved_required": True,
        "rules": rules,
    }
    (work_dir / "rules_candidate.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    _write_audit(work_dir, candidates, rules)
    return rules


def _write_audit(
    work_dir: Path, candidates: list[dict[str, Any]], rules: list[dict[str, Any]]
) -> None:
    lines = [
        "# 专家评分规则审计",
        "",
        "候选严重程度只描述评语被明确提及时的分数条件，不把未提及解释为不存在。",
        "所有规则默认未批准，人工确认 `approved: true` 后才能冻结到 Judge。",
        "",
        "## 问题统计",
        "",
        "| 问题 | 教师数 | 中位分 | 高分占比 | 低分占比 | 初判 |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for c in candidates:
        lines.append(
            f"| {c['label']} | {c['n_teachers']} | {c['median_score']} | "
            f"{c['high_score_share']:.1%} | {c['low_score_share']:.1%} | {c['suggested_severity']} |"
        )
    lines.extend(["", "## 待审核规则", ""])
    for rule in rules:
        lines.append(f"- [ ] `{rule.get('rule_id')}` {rule.get('scoring_action')}")
    (work_dir / "rule_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def freeze_approved_rules(candidate_path: Path, out_path: Path) -> int:
    data = yaml.safe_load(candidate_path.read_text(encoding="utf-8")) or {}
    approved = []
    validation_errors = []
    seen_ids: set[str] = set()
    for source_rule in data.get("rules") or []:
        if source_rule.get("approved") is not True or not _rule_is_actionable(source_rule):
            continue
        rule = dict(source_rule)
        rule.setdefault("applicable_when", [])
        rule.setdefault("not_observable_when", [])
        rule.setdefault("minor_when", [])
        rule.setdefault("major_when", [])
        rule.setdefault("severity", "context_dependent")
        rule.setdefault("primary_dimension", rule.get("target_dimension"))
        rule.setdefault("must_not_penalize_dimensions", [])
        _remove_legacy_score_floor(rule)
        validation_errors.extend(_production_rule_errors(rule))
        rule_id = str(rule.get("rule_id") or "")
        if rule_id in seen_ids:
            validation_errors.append(f"重复 rule_id: {rule_id}")
        seen_ids.add(rule_id)
        approved.append(rule)
    if not approved:
        raise ValueError("没有 approved: true 的可执行规则；请先审核 rules_candidate.yaml")
    if validation_errors:
        raise ValueError("冻结规则校验失败：\n- " + "\n- ".join(validation_errors))
    payload = {
        "version": f"frozen-{int(time.time())}",
        "source": candidate_path.name,
        "definition_source": "evaluation_criterion.md",
        "rules": approved,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    return len(approved)
