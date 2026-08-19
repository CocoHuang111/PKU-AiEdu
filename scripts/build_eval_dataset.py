"""构造评估数据集：inventory / extract / reflect / distill / rejudge / merge。

    python -m scripts.build_eval_dataset inventory --root ... --xlsx ... --out dataset/2018_spring
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.eval_dataset.inventory import (  # noqa: E402
    build_inventory,
    read_csv,
    write_csv,
)
from scripts.eval_dataset.progress import CliProgress  # noqa: E402

_progress = CliProgress()


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _cache_dir(batch: Path, video_id: str) -> Path:
    safe = video_id.replace("/", "_").replace("\\", "_")
    return batch / "cache" / safe


def _abs(rel: str | None) -> str | None:
    if not rel:
        return None
    p = Path(rel)
    return str(p if p.is_absolute() else ROOT / p)


def _apply_lessons(lessons_file: str | None) -> None:
    from ai_engine.evaluation.judge import set_expert_lessons

    if not lessons_file:
        set_expert_lessons("")
        return
    text = Path(lessons_file).read_text(encoding="utf-8").strip()
    set_expert_lessons(text)


def cmd_inventory(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    xlsx = Path(args.xlsx).resolve()
    out = Path(args.out).resolve()
    inventory, manifest = build_inventory(
        root,
        xlsx,
        name_col=args.name_col,
        dept_col=args.dept_col,
        score_col=args.score_col,
        comment_col=args.comment_col,
        score_min=args.score_min,
        score_max=args.score_max,
        skip_dir_prefix=args.skip_dir_prefix,
    )
    write_csv(out / "inventory.csv", inventory)
    write_csv(out / "manifest.csv", manifest)
    skips: dict[str, int] = {}
    for r in inventory:
        skips[r["skip"] or "ok"] = skips.get(r["skip"] or "ok", 0) + 1
    print(f"扫描 {len(inventory)} 人，训练候选 {len(manifest)} 人")
    print("纳入/排除：", ", ".join(f"{k}={v}" for k, v in sorted(skips.items())))
    print(f"写 {out / 'inventory.csv'}")
    print(f"写 {out / 'manifest.csv'}")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    from ai_engine.evaluation.media import cleanup_video_artifacts
    from ai_engine.evaluation.pipeline import collect_video_evidence, score_from_evidence

    manifest = read_csv(Path(args.manifest))
    if not manifest:
        print("manifest 为空")
        return 1
    out = Path(args.dir).resolve() if args.dir else Path(args.manifest).resolve().parent
    _apply_lessons(args.lessons)
    rows = manifest[: args.limit] if args.limit else manifest
    failed = 0
    for i, row in enumerate(rows, start=1):
        vid = row["video_id"]
        cache = _cache_dir(out, vid)
        ev_path = cache / "evidence.json"
        sc_path = cache / "scores.json"
        print(f"\n[{i}/{len(rows)}] {vid}", flush=True)
        try:
            if args.resume and ev_path.exists():
                pack = _load_json(ev_path)
                print("  复用 evidence.json")
            else:
                pack = collect_video_evidence(
                    _abs(row["video_path"]) or row["video_path"],
                    progress=_progress,
                    syllabus_path=_abs(row.get("syllabus_path")),
                    courseware_path=_abs(row.get("courseware_path")),
                )
                _progress.finish()
                disk = {
                    "video_id": vid,
                    "video_file": pack["video_file"],
                    "duration_sec": pack["duration_sec"],
                    "has_syllabus": pack["has_syllabus"],
                    "has_courseware": pack["has_courseware"],
                    "evidence": pack["evidence"],
                    "raw_features": pack["raw_features"],
                    "available": pack["available"],
                    "transcript": pack["transcript"],
                }
                _dump_json(ev_path, disk)
                pack = disk
                if not args.keep_media:
                    cleanup_video_artifacts(_abs(row["video_path"]) or row["video_path"])
                    print("  已删本条抽音/关键帧")

            need_score = True
            if args.resume and sc_path.exists():
                old = _load_json(sc_path)
                if old.get("prompt_version") == args.prompt_version:
                    print(f"  复用 scores.json ({args.prompt_version})")
                    need_score = False
            if need_score:
                scores = score_from_evidence(
                    pack["evidence"],
                    pack.get("available") or ["text"],
                    progress=_progress,
                    prompt_version=args.prompt_version,
                )
                _progress.finish()
                _dump_json(sc_path, scores)
        except Exception as e:
            _progress.finish()
            failed += 1
            _dump_json(cache / "error.json", {"error": str(e), "trace": traceback.format_exc()})
            print(f"  失败：{e}", flush=True)
            if not args.keep_media and row.get("video_path"):
                try:
                    cleanup_video_artifacts(_abs(row["video_path"]) or row["video_path"])
                except Exception:
                    pass
    print(f"\n完成 {len(rows) - failed}/{len(rows)}，失败 {failed}")
    return 1 if failed else 0


def _llm_summary(scores: dict[str, Any]) -> str:
    lines = []
    overall = scores.get("overall") or {}
    lines.append(f"总分 {overall.get('score')}（{overall.get('grade_label', '')}）")
    weak: list[tuple[float, str]] = []
    for d in scores.get("dimensions") or []:
        if not d.get("assessed"):
            continue
        lines.append(
            f"- {d.get('label')} {d.get('score')}："
            f"{(d.get('dimension_rationale') or '')[:80]}"
        )
        for ind in d.get("indicators") or []:
            if ind.get("assessed") and ind.get("score") is not None:
                weak.append((float(ind["score"]), f"{ind.get('label')} {ind['score']}"))
    weak.sort()
    if weak:
        lines.append("最低二级：" + "；".join(t[1] for t in weak[:3]))
    return "\n".join(lines)


def cmd_reflect(args: argparse.Namespace) -> int:
    from ai_engine.evaluation.judge import _parse_json
    from ai_engine.pedagogy.loader import render_prompt
    from ai_engine.providers import ChatMessage, get_llm

    batch = Path(args.dir).resolve()
    manifest = read_csv(batch / "manifest.csv")
    llm = get_llm()
    n_ok = n_skip = 0
    for row in manifest:
        vid = row["video_id"]
        comment = (row.get("comment") or "").strip()
        sc_path = _cache_dir(batch, vid) / "scores.json"
        out_path = batch / "lessons" / f"{vid}.json"
        if args.resume and out_path.exists():
            n_skip += 1
            continue
        if not comment:
            n_skip += 1
            continue
        if not sc_path.exists():
            print(f"跳过 {vid}：没有 scores.json")
            n_skip += 1
            continue
        scores = _load_json(sc_path)
        prompt = render_prompt(
            "eval_reflect.j2", comment=comment, llm_summary=_llm_summary(scores)
        )
        raw = llm.chat(
            [
                ChatMessage(
                    "system",
                    "你只输出合法 JSON，对照专家评语与模型摘要，不重新打分。",
                ),
                ChatMessage("user", prompt),
            ]
        )
        try:
            parsed = _parse_json(raw)
        except ValueError:
            parsed = {"drop": False, "lesson": "", "raw": raw[:500], "error": "parse"}
        parsed["video_id"] = vid
        parsed["created_at"] = time.time()
        _dump_json(out_path, parsed)
        n_ok += 1
        lesson = (parsed.get("lesson") or "").strip()
        flag = "drop" if parsed.get("drop") else ("lesson" if lesson else "empty")
        print(f"  {vid}: {flag} {lesson[:40]}")
    print(f"reflect 写入 {n_ok}，跳过 {n_skip}")
    return 0


def _collect_lessons(batch: Path, holdout: int) -> tuple[list[str], list[str]]:
    files = sorted((batch / "lessons").glob("*.json"))
    usable: list[tuple[str, str]] = []
    for p in files:
        data = _load_json(p)
        if data.get("drop"):
            continue
        lesson = str(data.get("lesson") or "").strip()
        if not lesson:
            continue
        usable.append((data.get("video_id") or p.stem, lesson))
    holdout_ids = {vid for vid, _ in usable[-holdout:]} if holdout else set()
    train = [les for vid, les in usable if vid not in holdout_ids]
    held = [les for vid, les in usable if vid in holdout_ids]
    return train, held


def cmd_distill(args: argparse.Namespace) -> int:
    from ai_engine.pedagogy.loader import render_prompt
    from ai_engine.providers import ChatMessage, get_llm

    batch = Path(args.dir).resolve()
    out = Path(args.out) if args.out else batch / "lessons_distilled.md"
    existing = ""
    if args.existing:
        existing = Path(args.existing).read_text(encoding="utf-8").strip()
    train, held = _collect_lessons(batch, args.holdout)
    if not train:
        print("没有可蒸馏的 lesson（全是空或 drop）")
        out.write_text("", encoding="utf-8")
        return 0
    numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(train, start=1))
    prompt = render_prompt(
        "eval_distill.j2",
        existing_bullets=existing or "（无）",
        lessons_numbered=numbered,
    )
    raw = get_llm().chat(
        [
            ChatMessage("system", "你只输出短 Markdown 无序列表，不要前言。"),
            ChatMessage("user", prompt),
        ]
    )
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("markdown", "", 1).strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith(("-", "*"))]
    if not lines:
        # 解析失败时用本年 lesson 去重顶上 8 条，保证有产出
        uniq: list[str] = []
        for les in train:
            if les not in uniq:
                uniq.append(les)
        lines = [f"- {x[:40]}" for x in uniq[:8]]
        text = "\n".join(lines)
        print("警告：模型未输出列表，已用 lesson 去重兜底")
    else:
        text = "\n".join(lines[:8])
    out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"<!-- prompt_version 建议：在此文件人工确认后挂进下一年度 Judge；"
        f"holdout={args.holdout} -->\n"
    )
    out.write_text(header + text + "\n", encoding="utf-8")
    print(f"写 {out}（{len(lines[:8])} 条；蒸馏用 {len(train)} 条，holdout {len(held)} 条）")
    print(text)
    return 0


def cmd_rejudge(args: argparse.Namespace) -> int:
    from ai_engine.evaluation.pipeline import score_from_evidence

    batch = Path(args.dir).resolve()
    manifest = read_csv(batch / "manifest.csv")
    _apply_lessons(args.lessons)
    failed = 0
    n = 0
    for row in manifest:
        vid = row["video_id"]
        cache = _cache_dir(batch, vid)
        ev_path = cache / "evidence.json"
        if not ev_path.exists():
            print(f"跳过 {vid}：没有 evidence.json")
            continue
        n += 1
        pack = _load_json(ev_path)
        print(f"rejudge {vid} → {args.prompt_version}")
        try:
            scores = score_from_evidence(
                pack["evidence"],
                pack.get("available") or ["text"],
                progress=_progress,
                prompt_version=args.prompt_version,
            )
            _progress.finish()
            _dump_json(cache / "scores.json", scores)
        except Exception as e:
            _progress.finish()
            failed += 1
            print(f"  失败：{e}")
    print(f"rejudge {n - failed}/{n}，失败 {failed}")
    return 1 if failed else 0


def _flat_features(raw: dict[str, Any]) -> dict[str, Any]:
    from ai_engine.pedagogy.loader import get_rubric

    spec = get_rubric().get("objective_features") or {}
    out: dict[str, Any] = {}
    for group, keys in spec.items():
        src = (raw or {}).get(group) or {}
        for key in keys:
            out[f"{group}__{key}"] = src.get(key, "")
    return out


def _dim_map(scores: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for d in scores.get("dimensions") or []:
        key = d.get("key")
        out[f"llm_dim_{key}"] = d.get("score") if d.get("assessed") else ""
        out[f"llm_dim_{key}_source"] = d.get("score_source") or ""
        out[f"llm_dim_{key}_rationale"] = d.get("dimension_rationale") or ""
        for ind in d.get("indicators") or []:
            ik = ind.get("key")
            out[f"ind_{ik}"] = ind.get("score") if ind.get("assessed") else ""
            out[f"ind_{ik}_assessed"] = int(bool(ind.get("assessed")))
    return out


def cmd_merge(args: argparse.Namespace) -> int:
    batch = Path(args.dir).resolve()
    manifest = read_csv(batch / "manifest.csv")
    versions: set[str] = set()
    detail_rows: list[dict[str, Any]] = []
    gb_rows: list[dict[str, Any]] = []
    align_rows: list[dict[str, Any]] = []

    for row in manifest:
        vid = row["video_id"]
        cache = _cache_dir(batch, vid)
        ev_path = cache / "evidence.json"
        sc_path = cache / "scores.json"
        if not ev_path.exists() or not sc_path.exists():
            print(f"merge 跳过 {vid}：缺 evidence 或 scores")
            continue
        pack = _load_json(ev_path)
        scores = _load_json(sc_path)
        pv = str(scores.get("prompt_version") or "")
        versions.add(pv)
        overall = (scores.get("overall") or {}).get("score")
        try:
            expert100 = float(row["expert_total_100"]) if row.get("expert_total_100") else None
        except ValueError:
            expert100 = None
        residual = ""
        if expert100 is not None and overall is not None:
            residual = round(expert100 - float(overall), 2)

        lesson_path = batch / "lessons" / f"{vid}.json"
        lesson = {}
        if lesson_path.exists():
            lesson = _load_json(lesson_path)

        base = {
            "video_id": vid,
            "name": row.get("name"),
            "dept": row.get("dept"),
            "folder_rel": row.get("folder_rel"),
            "video_path": row.get("video_path"),
            "syllabus_path": row.get("syllabus_path"),
            "courseware_path": row.get("courseware_path"),
            "has_syllabus": pack.get("has_syllabus"),
            "has_courseware": pack.get("has_courseware"),
            "duration_sec": pack.get("duration_sec"),
            "prompt_version": pv,
            "expert_avg": row.get("expert_avg"),
            "expert_total_100": row.get("expert_total_100"),
            "score_std": row.get("score_std"),
            "llm_overall": overall,
            "residual": residual,
        }
        feats = _flat_features(pack.get("raw_features") or {})
        dims = _dim_map(scores)
        detail = {
            **base,
            "comment": row.get("comment"),
            **{k: row[k] for k in row if k.startswith("expert") and k != "expert_avg"},
            **feats,
            **dims,
        }
        detail_rows.append(detail)

        gb = {
            "video_id": vid,
            "expert_avg": row.get("expert_avg"),
            "expert_total_100": row.get("expert_total_100"),
            "prompt_version": pv,
            **feats,
        }
        for k, v in dims.items():
            if k.startswith("llm_dim_") and not k.endswith("_rationale") and not k.endswith("_source"):
                gb[k] = v
        gb_rows.append(gb)

        align_rows.append(
            {
                "video_id": vid,
                "prompt_version": pv,
                "expert_avg": row.get("expert_avg"),
                "expert_total_100": row.get("expert_total_100"),
                "llm_overall": overall,
                "residual": residual,
                "comment": row.get("comment"),
                "lesson": lesson.get("lesson") or "",
                "drop": lesson.get("drop", ""),
                "agreed": lesson.get("agreed") or "",
                "missed": lesson.get("missed") or "",
                "primary_issue": (lesson.get("missed") or lesson.get("lesson") or "")[:80],
            }
        )

    if len(versions) > 1:
        print(
            f"警告：scores 含多个 prompt_version {sorted(versions)}。"
            "训 GB 前请用同一版本 rejudge。"
        )
    write_csv(batch / "training_detail.csv", detail_rows)
    write_csv(batch / "training_gb.csv", gb_rows)
    write_csv(batch / "alignment.csv", align_rows)
    print(
        f"merge {len(detail_rows)} 条 → training_detail.csv / training_gb.csv / alignment.csv"
        f"（prompt_version={sorted(versions)}）"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="教学视频评估数据集构造")
    sub = p.add_subparsers(dest="cmd", required=True)

    inv = sub.add_parser("inventory", help="扫描文件夹并匹配打分表")
    inv.add_argument("--root", required=True)
    inv.add_argument("--xlsx", required=True)
    inv.add_argument("--out", required=True)
    inv.add_argument("--name-col", default="姓名")
    inv.add_argument("--dept-col", default="院系")
    inv.add_argument("--score-col", default="平均分")
    inv.add_argument("--comment-col", default="评语")
    inv.add_argument("--score-min", type=float, default=2.0)
    inv.add_argument("--score-max", type=float, default=4.0)
    inv.add_argument("--skip-dir-prefix", default="", help="可选；本批不要用来跳过「未通过」")
    inv.set_defaults(func=cmd_inventory)

    ex = sub.add_parser("extract", help="ASR+VLM 证据 + 当前 prompt 打分")
    ex.add_argument("--manifest", required=True)
    ex.add_argument("--dir", default="", help="默认与 manifest 同目录")
    ex.add_argument("--resume", action="store_true")
    ex.add_argument("--limit", type=int, default=0)
    ex.add_argument("--prompt-version", default="v0")
    ex.add_argument("--lessons", default="", help="可选：已确认的蒸馏要点文件，注入 Judge")
    ex.add_argument("--keep-media", action="store_true", help="保留抽音和关键帧（默认删）")
    ex.set_defaults(func=cmd_extract)

    rf = sub.add_parser("reflect", help="逐课对照评语，写出 lesson")
    rf.add_argument("--dir", required=True)
    rf.add_argument("--resume", action="store_true")
    rf.set_defaults(func=cmd_reflect)

    ds = sub.add_parser("distill", help="把本年 lesson 压成 5–8 条")
    ds.add_argument("--dir", required=True)
    ds.add_argument("--out", default="")
    ds.add_argument("--existing", default="", help="以往年份已确认清单")
    ds.add_argument("--holdout", type=int, default=0, help="最后 N 人的 lesson 不参与蒸馏")
    ds.set_defaults(func=cmd_distill)

    rj = sub.add_parser("rejudge", help="只重跑 Judge+报告")
    rj.add_argument("--dir", required=True)
    rj.add_argument("--prompt-version", required=True)
    rj.add_argument("--lessons", default="")
    rj.set_defaults(func=cmd_rejudge)

    mg = sub.add_parser("merge", help="写出 training_detail / training_gb / alignment")
    mg.add_argument("--dir", required=True)
    mg.set_defaults(func=cmd_merge)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
