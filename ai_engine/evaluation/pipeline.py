"""功能① 教学视频质量评估的编排。

evaluate_session()    统一入口：视频 / 讲稿 / 大纲 / 课件任意组合
evaluate_video()      完整流水线：视频 → 音频+关键帧 → ASR（有讲稿则跳过）→ Judge
evaluate_transcript() 纯文本通道：只喂转写，跳过 ASR 与视觉
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any, Callable

from ..config import settings
from .. import checkpoints
from ..pedagogy.loader import get_rubric, grade_of, render_prompt
from ..providers import ASRResult, ChatMessage, ProviderError, get_asr, get_llm
from . import diarization, media
from .exceptions import EvaluationCancelled
from .gb import LIVE_PROMPT_VERSION, LIVE_SCORE_SOURCE, predict_overall
from .audio_features import extract_audio_features_isolated
from .judge import judge_all, judge_fingerprint
from .slide_features import extract_slide_features, extract_slide_features_from_images
from .text_features import (
    CHINESE_CHAR,
    extract_text_features,
    segment_transcript,
    summarize_segments,
)
from .timeline_features import extract_timeline_features
from .transcript_punc import punctuate_asr_result
from .materials import MaterialError, load_script_text, load_syllabus_text, prepare_courseware
from .vision import (
    aggregate_courseware_features,
    aggregate_vision_features,
    describe_courseware_pages,
    describe_keyframes,
    locate_content_rois,
)

ProgressFn = Callable[[int, str, dict], None]

# 证据分组 → 该分组能点亮哪个模态。缺失分组对应的指标会被标为未评估，
# 而不是硬塞给模型瞎猜。
FEATURE_GROUP_MODALITY = {
    "text": "text",
    "timeline": "text",
    "audio": "audio",
    "speakers": "audio",
    "vision": "vision",
    "slides": "vision",
    "courseware": "vision",
}

MAX_REFERENCE_CHARS = 12000


def _noop(progress: int, step: str, detail: dict | None = None) -> None:
    pass


def _estimate_duration_sec(text: str) -> float:
    """没有视频时按约 200 字/分钟估课堂时长，至少 5 分钟，避免速率被吹爆。"""
    chars = len(CHINESE_CHAR.findall(text or ""))
    return max(chars / 200.0 * 60.0, 300.0)


def _resolve_script(
    transcript_text: str | None,
    transcript_path: str | None,
    progress: ProgressFn = _noop,
) -> str | None:
    text = (transcript_text or "").strip() or None
    if text:
        return text
    if not transcript_path:
        return None
    progress(14, "parse_materials", {"kind": "transcript"})
    try:
        return load_script_text(transcript_path)
    except MaterialError as e:
        raise RuntimeError(str(e)) from e


def _feature_rows(features: dict, group: str) -> list[dict]:
    """把原始特征字典转成带中文标签的展示行，同时喂给 Judge 和前端。"""
    spec = get_rubric()["objective_features"].get(group, {})
    rows = []
    for key, meta in spec.items():
        if key not in features:
            continue
        row = {
            "key": key,
            "label": meta["label"],
            "value": features[key],
            "unit": meta.get("unit", ""),
        }
        if meta.get("ideal"):
            row["ideal"] = list(meta["ideal"])
        rows.append(row)
    return rows


def build_evidence(
    transcript: str,
    duration_sec: float,
    features: dict[str, dict],
    vision_notes: list[dict] | None = None,
    reference: str | None = None,
    max_transcript_chars: int = 12000,
    has_courseware: bool = False,
    courseware_text: str = "",
    courseware_notes: list[dict] | None = None,
    courseware_visual: bool = False,
) -> dict[str, Any]:
    """组装喂给 Judge 的证据包。转写过长时首尾截取，保留开场和收尾。

    features 是 {分组名: 特征字典}，分组名与 rubric 的 objective_features 对齐。
    """
    text = transcript
    if len(text) > max_transcript_chars:
        head = max_transcript_chars * 2 // 3
        tail = max_transcript_chars - head
        text = f"{text[:head]}\n\n……（中间省略 {len(transcript) - max_transcript_chars} 字）……\n\n{text[-tail:]}"

    ref = (reference or "").strip()
    if len(ref) > MAX_REFERENCE_CHARS:
        ref = ref[:MAX_REFERENCE_CHARS] + "\n……（已截断）"

    cw_text = (courseware_text or "").strip()
    if len(cw_text) > MAX_REFERENCE_CHARS:
        cw_text = cw_text[:MAX_REFERENCE_CHARS] + "\n……（已截断）"

    return {
        "duration_minutes": round(duration_sec / 60.0, 1),
        "total_chars": features.get("text", {}).get("total_chars", 0),
        "transcript": text,
        "reference": ref,
        "has_syllabus": bool(ref),
        "has_courseware": bool(has_courseware),
        "courseware_text": cw_text,
        "courseware_visual": bool(courseware_visual),
        "text_features": _feature_rows(features.get("text", {}), "text"),
        "audio_features": _feature_rows(features.get("audio", {}), "audio"),
        "timeline_features": _feature_rows(features.get("timeline", {}), "timeline"),
        "vision_features": _feature_rows(features.get("vision", {}), "vision"),
        "slide_features": _feature_rows(features.get("slides", {}), "slides"),
        "slide_roi_used": (features.get("slides") or {}).get("slide_roi_source") == "vlm",
        "speaker_features": _feature_rows(features.get("speakers", {}), "speakers"),
        "courseware_features": _feature_rows(features.get("courseware", {}), "courseware"),
        "vision_notes": [
            {"timestamp": n["timestamp"], "description": n["description"]}
            for n in (vision_notes or [])
            if n.get("ok")
        ],
        "courseware_notes": [
            {"page": n.get("page", n.get("index", 0) + 1), "description": n["description"]}
            for n in (courseware_notes or [])
            if n.get("ok")
        ],
    }


def _available_modalities(features: dict[str, dict]) -> set[str]:
    """哪些模态真的拿到了数据。text 恒有（转写是入口条件）。"""
    available = {"text"}
    for group, modality in FEATURE_GROUP_MODALITY.items():
        if features.get(group):
            available.add(modality)
    return available


def _objective_rows(features: dict[str, dict]) -> dict[str, list[dict]]:
    return {
        group: _feature_rows(features.get(group, {}), group)
        for group in FEATURE_GROUP_MODALITY
    }


def generate_report(judged: dict) -> str:
    prompt = render_prompt(
        "eval_report.j2",
        overall=judged["overall"],
        dimensions=judged["dimensions"],
    )
    try:
        return get_llm().chat(
            [
                ChatMessage(
                    "system", "你是资深的高校教师发展中心专家，擅长撰写教学诊断报告。"
                ),
                ChatMessage("user", prompt),
            ]
        ).strip()
    except ProviderError as e:
        return _fallback_report(judged, str(e))


_DIGEST_KEYS = (("突出优点", "strengths"), ("主要问题", "issues"), ("改进建议", "suggestions"))


def _digest_span(report: str) -> tuple[int, int] | None:
    if not report:
        return None
    m = re.search(r"^##\s+(?:[〇零0]、\s*)?诊断摘要\s*$", report, re.M)
    if not m:
        return None
    rest = report[m.end() :]
    nxt = re.search(r"^##\s+", rest, re.M)
    end = m.end() + nxt.start() if nxt else len(report)
    return m.start(), end


def parse_report_digest(report: str) -> dict[str, list[str]]:
    """抽出模型输出里「诊断摘要」三类各至多 2 条短句。没有该节则返回空。"""
    digest = {key: [] for _, key in _DIGEST_KEYS}
    span = _digest_span(report)
    if not span:
        return digest
    start, end = span
    heading = re.search(r"^##\s+(?:[〇零0]、\s*)?诊断摘要\s*$", report[start:end], re.M)
    body = report[start + (heading.end() if heading else 0) : end]
    current = None
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            current = next((key for label, key in _DIGEST_KEYS if label in title), None)
            continue
        if not current or not re.match(r"^(?:\d+[\.、．)]|[-*])\s+", line):
            continue
        item = re.sub(r"^(?:\d+[\.、．)]|[-*])\s+", "", line)
        item = item.replace("**", "").strip(" 。！？；;")
        if item and item not in digest[current] and "短句" not in item:
            digest[current].append(item)
        if len(digest[current]) >= 2:
            current = None
    return digest


def strip_report_digest(report: str) -> str:
    """从诊断报告正文去掉「〇、诊断摘要」。摘要只走 digest 字段。"""
    span = _digest_span(report)
    if not span:
        return (report or "").strip()
    start, end = span
    return (report[:start].rstrip() + "\n\n" + report[end:].lstrip()).strip()


def fallback_digest(judged: dict) -> dict[str, list[str]]:
    """报告里没有摘要节时，用最高分指标、主问题和建议各补 2 条。"""
    inds = [
        i
        for d in judged.get("dimensions") or []
        for i in d.get("indicators") or []
        if i.get("assessed")
    ]
    strengths = [
        f"{i['label']} {i['score']} 分"
        for i in sorted(inds, key=lambda x: x.get("score") or 0, reverse=True)[:2]
    ]
    issues = []
    for d in judged.get("dimensions") or []:
        issue = (d.get("primary_issue") or "").strip()
        if d.get("assessed") and issue and issue != "当前证据未发现显著问题":
            issues.append(issue[:22])
        if len(issues) >= 2:
            break
    suggestions = []
    for i in inds:
        tip = (i.get("suggestion") or "").strip()
        if tip and tip != "保持":
            suggestions.append(re.split(r"[。！？]", tip, maxsplit=1)[0][:22])
        if len(suggestions) >= 2:
            break
    return {"strengths": strengths, "issues": issues, "suggestions": suggestions}


def attach_report(judged: dict) -> tuple[str, dict[str, list[str]]]:
    raw = generate_report(judged)
    digest = parse_report_digest(raw)
    if not (digest["strengths"] or digest["issues"] or digest["suggestions"]):
        digest = fallback_digest(judged)
    return strip_report_digest(raw), digest


def _fallback_report(judged: dict, reason: str) -> str:
    """LLM 不可用时，用评分结果拼一份结构化报告，保证链路不断。"""
    overall = judged["overall"]
    lines = [
        f"## 一、总体评价\n\n综合得分 **{overall['score']}/100**（{overall['grade']} 级 · {overall['grade_label']}）。\n",
        f"> 注：文字报告生成失败（{reason}），以下为根据评分结果自动汇总的结构化摘要。\n",
        "## 五维得分\n",
    ]
    for d in judged["dimensions"]:
        score = f"{d['score']} 分（{d['grade']}）" if d["assessed"] else "未评估"
        extra = f"：{d['dimension_rationale']}" if d.get("dimension_rationale") else ""
        lines.append(f"- **{d['label']}**：{score}{extra}")

    lines.append("\n## 最需要改进的方面\n")
    weakest = sorted(
        (
            i
            for d in judged["dimensions"]
            for i in d["indicators"]
            if i["assessed"]
        ),
        key=lambda i: i["score"],
    )[:5]
    for ind in weakest:
        lines.append(f"- **{ind['label']}**（{ind['score']} 分）：{ind['suggestion']}")
    return "\n".join(lines)


# --------------------------------------------------------------- 纯文本通道


def evaluate_transcript(
    text: str,
    duration_sec: float = 2700,
    progress: ProgressFn = _noop,
    reference: str | None = None,
) -> dict[str, Any]:
    progress(20, "objective_features", {})
    features = {"text": extract_text_features(text, duration_sec)}

    progress(30, "llm_judge", {})
    evidence = build_evidence(text, duration_sec, features, reference=reference)

    def on_dim(done: int, total: int, label: str):
        progress(30 + int(50 * done / total), "llm_judge", {"dimension": label})

    judged = apply_live_overall(
        judge_all(evidence, {"text"}, progress_callback=on_dim),
        raw_features=features,
    )

    progress(85, "report", {})
    report, digest = attach_report(judged)

    progress(100, "done", {})
    has_syllabus = bool((reference or "").strip())
    return {
        "source": "transcript",
        "prompt_version": LIVE_PROMPT_VERSION,
        "overall": judged["overall"],
        "dimensions": judged["dimensions"],
        "objective_features": _objective_rows(features),
        "raw_features": features,
        "has_reference": has_syllabus,
        "has_syllabus": has_syllabus,
        "has_courseware": False,
        "transcript_source": "script",
        "keyframes": [],
        "courseware_slides": [],
        "transcript": {
            "full_text": text,
            "duration_sec": duration_sec,
            "language": "zh",
            "segments": [],
        },
        "report": report,
        "digest": digest,
        "created_at": time.time(),
    }


# --------------------------------------------------------------- 完整通道


def _jsonable(value: Any) -> Any:
    """把 numpy 标量等转成 JSON 可写类型，便于 evidence.json 落盘。"""
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if hasattr(value, "item") and callable(value.item):
        try:
            return value.item()
        except Exception:
            return value
    if isinstance(value, float):
        return round(value, 6)
    return value


def collect_video_evidence(
    video_path: str,
    progress: ProgressFn = _noop,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript_text: str | None = None,
    transcript_path: str | None = None,
) -> dict[str, Any]:
    """视频 → 转写 / 客观特征 / VLM。不打分。返回可序列化的证据包。

    有讲稿时当作转写，跳过 ASR；没有真实时间戳就不做 timeline。
    """
    eval_conf = settings.section("evaluation")
    video_path = str(video_path)
    video_stem = Path(video_path).stem
    browser_evidence = media.load_browser_evidence(video_path)

    progress(5, "extracting_audio", {})
    audio_path = media.extract_audio(video_path)
    duration = (
        float(browser_evidence["duration_sec"])
        if browser_evidence
        else media.probe_duration(video_path)
    )

    syllabus_text = (reference or "").strip() or None
    if syllabus_path:
        progress(7, "parse_materials", {"kind": "syllabus"})
        try:
            syllabus_text = load_syllabus_text(syllabus_path)
        except MaterialError as e:
            raise RuntimeError(str(e)) from e

    courseware_pack: dict[str, Any] | None = None
    if courseware_path:
        progress(8, "parse_materials", {"kind": "courseware"})
        try:
            courseware_pack = prepare_courseware(
                courseware_path, settings.frame_dir / video_stem
            )
        except MaterialError as e:
            # 课件是选填。解析失败按无课件口径继续，不要把整堂课（含已抽的音）判死。
            progress(8, "parse_materials", {"warning": str(e)})
            courseware_pack = None
        if courseware_pack and courseware_pack.get("warning"):
            progress(8, "parse_materials", {"warning": courseware_pack["warning"]})

    keyframes: list[dict] = []
    vlm_enabled = eval_conf.get("vlm_enabled", True)
    if vlm_enabled:
        progress(10, "keyframe_sampling", {})
        try:
            if browser_evidence:
                keyframes = [
                    {
                        "index": index,
                        "path": item["path"],
                        "time_sec": round(float(item["time_sec"]), 1),
                        "timestamp": media._fmt_time(float(item["time_sec"])),
                    }
                    for index, item in enumerate(browser_evidence["keyframes"])
                ]
            else:
                keyframes = media.extract_keyframes(video_path, duration=duration)
        except media.MediaError as e:
            progress(10, "keyframe_sampling", {"warning": str(e)})

    script = _resolve_script(transcript_text, transcript_path, progress)
    transcript_source = "script" if script else "asr"

    if script:
        progress(15, "asr", {"source": "script"})
        duration = duration or _estimate_duration_sec(script)
        asr_result = ASRResult(
            text=script, segments=[], language="zh", duration=float(duration)
        )
    else:
        progress(15, "asr", {})

        def on_asr(done_sec: float, total_sec: float):
            pct = 15 + int(25 * min(done_sec / max(total_sec, 1), 1.0))
            progress(
                pct, "asr", {"done_sec": round(done_sec), "total_sec": round(total_sec)}
            )

        asr_result = get_asr().transcribe(audio_path, progress_callback=on_asr)
        duration = duration or asr_result.duration
        asr_conf = settings.flat_config("asr")
        if asr_conf.get("punctuate", True):
            progress(40, "asr", {"phase": "punctuate"})

            def on_punctuation(done, total, detail):
                progress(40 + int(5 * done / max(total, 1)), "asr", {
                    "phase": "punctuate", "done": done, "total": total, **detail,
                })

            try:
                asr_result = punctuate_asr_result(
                    asr_result, progress_callback=on_punctuation,
                    budget_seconds=float(asr_conf.get("punctuation_budget_seconds", 180)),
                    checkpoint_dir=Path(audio_path).with_suffix(".punctuation-checkpoint"),
                )
            except EvaluationCancelled:
                raise
            except Exception as e:
                progress(45, "asr", {"warning": f"转写补标点失败，沿用原转写: {e}"})

    if not asr_result.text.strip():
        raise RuntimeError(
            "语音识别结果为空。请确认视频含有清晰的中文语音，"
            "或改传讲稿，或在 config.yaml 中把 asr.model 换成 small / medium 再试。"
        )

    progress(46, "objective_features", {})
    segments = segment_transcript(
        asr_result.segments, eval_conf.get("segment_minutes", 5)
    )

    text_features = extract_text_features(asr_result.text, duration)
    text_features.update(summarize_segments(segments))

    features: dict[str, dict] = {
        "text": text_features,
    }
    if asr_result.segments:
        features["timeline"] = extract_timeline_features(asr_result.segments)

    if eval_conf.get("audio_enabled", True):
        def on_audio(phase, done, total):
            fraction = min(done / max(total, 1), 1.0)
            pct = (47 + int(2 * fraction)) if phase == "pitch" else (46 + int(fraction))
            if phase == "cached":
                pct = 49
            progress(pct, "objective_features", {
                "phase": phase, "done_sec": round(done), "total_sec": round(total),
            })
        try:
            features["audio"] = extract_audio_features_isolated(
                audio_path, progress_callback=on_audio,
            )
        except EvaluationCancelled:
            raise
        except Exception as e:
            progress(46, "objective_features", {"warning": f"声学特征提取失败: {e}"})

    if eval_conf.get("slide_detection_enabled", True):
        progress(50, "slide_detection", {})
        rois: list[dict] = []
        roi_meta: dict[str, Any] = {"boxes": [], "source": "none"}
        try:
            if (
                eval_conf.get("slide_roi_enabled", True)
                and vlm_enabled
                and keyframes
            ):
                progress(50, "slide_detection", {"phase": "roi"})
                roi_meta = locate_content_rois(
                    keyframes,
                    max_attempts=int(eval_conf.get("slide_roi_max_frames", 2)),
                )
                rois = list(roi_meta.get("boxes") or [])
        except Exception as e:
            progress(50, "slide_detection", {"warning": f"投影区域定位失败: {e}"})
            roi_meta = {"boxes": [], "source": "none"}
        try:
            if browser_evidence:
                slides = extract_slide_features_from_images(
                    [item["path"] for item in browser_evidence["dense_frames"]],
                    asr_result.segments,
                    interval_sec=float(browser_evidence["interval_sec"]),
                    change_threshold=eval_conf.get("slide_change_threshold", 0.08),
                    rois=rois,
                )
            else:
                slides = extract_slide_features(
                    video_path,
                    asr_result.segments,
                    interval_sec=eval_conf.get("slide_sample_interval_sec", 3.0),
                    change_threshold=eval_conf.get("slide_change_threshold", 0.08),
                    rois=rois,
                )
            slides["slide_roi_source"] = roi_meta.get("source") or "none"
            if rois:
                slides["slide_roi_boxes"] = rois
            features["slides"] = slides
        except Exception as e:
            progress(50, "slide_detection", {"warning": f"课件切换检测失败: {e}"})

    if diarization.is_enabled():
        progress(53, "diarization", {})
        try:
            features["speakers"] = diarization.extract_speaker_features(audio_path)
        except Exception as e:
            progress(53, "diarization", {"warning": f"说话人分离失败: {e}"})

    vision_notes: list[dict] = []
    courseware_notes: list[dict] = []
    cw_pages = (courseware_pack or {}).get("pages") or []
    vlm_total = (len(keyframes) if (vlm_enabled and keyframes) else 0) + (
        len(cw_pages) if (vlm_enabled and cw_pages) else 0
    )
    vlm_done = 0

    def on_vlm_item(_done: int, _total: int):
        nonlocal vlm_done
        vlm_done += 1
        progress(
            58 + int(12 * vlm_done / max(vlm_total, 1)),
            "vlm_describe",
            {"done": vlm_done, "total": vlm_total},
        )

    if vlm_enabled and keyframes:
        progress(58, "vlm_describe", {"total": vlm_total or len(keyframes)})
        try:
            vision_notes = describe_keyframes(keyframes, progress_callback=on_vlm_item)
            features["vision"] = aggregate_vision_features(vision_notes)
        except ProviderError as e:
            progress(70, "vlm_describe", {"warning": str(e)})

    if vlm_enabled and cw_pages:
        progress(58, "vlm_describe", {"total": vlm_total, "kind": "courseware"})
        try:
            courseware_notes = describe_courseware_pages(
                cw_pages, progress_callback=on_vlm_item
            )
            cw_feat = aggregate_courseware_features(courseware_notes)
            if cw_feat:
                features["courseware"] = cw_feat
        except ProviderError as e:
            progress(70, "vlm_describe", {"warning": f"课件页面分析失败: {e}"})

    features = {k: v for k, v in features.items() if v}
    has_cw = bool(courseware_pack)
    evidence = build_evidence(
        asr_result.text,
        duration,
        features,
        vision_notes,
        syllabus_text,
        has_courseware=has_cw,
        courseware_text=(courseware_pack or {}).get("text") or "",
        courseware_notes=courseware_notes,
        courseware_visual=bool((courseware_pack or {}).get("visual")),
    )
    return {
        "video_file": (
            browser_evidence.get("original_filename")
            if browser_evidence
            else Path(video_path).name
        ),
        "duration_sec": round(float(duration), 1),
        "has_syllabus": bool((syllabus_text or "").strip()),
        "has_courseware": has_cw,
        "evidence": _jsonable(evidence),
        "raw_features": _jsonable(features),
        "available": sorted(_available_modalities(features)),
        "transcript": {
            "full_text": asr_result.text,
            "duration_sec": round(float(duration), 1),
            "language": asr_result.language,
            "segments": _jsonable(segments),
        },
        "vision_notes": vision_notes,
        "courseware_notes": courseware_notes,
        "source": "video",
        "upload_mode": "browser_evidence" if browser_evidence else "original_video",
        "transcript_source": transcript_source,
    }


def apply_live_overall(
    judged: dict[str, Any],
    *,
    raw_features: dict[str, Any] | None = None,
    model_path: Path | str | None = None,
) -> dict[str, Any]:
    """五维仍用 Judge；总分改成四年 v7.1 客观特征+五维 5 分类 GB。等权平均保留备查。"""
    overall = judged["overall"]
    equal_weight = overall.get("score")
    pred = predict_overall(
        judged.get("dimensions") or [],
        raw_features=raw_features,
        model_path=model_path,
    )
    overall.update(
        {
            "score": pred["score"],
            **grade_of(pred["score"]),
            "score_source": LIVE_SCORE_SOURCE,
            "equal_weight_score": equal_weight,
            "gb_label": pred["label"],
            "gb_score_5": pred["score_5"],
            "gb_score_4": pred.get("score_4"),
            "gb_variant": pred["variant"],
        }
    )
    judged["overall"] = overall
    return judged


def score_from_evidence(
    evidence: dict[str, Any],
    available: set[str] | list[str],
    progress: ProgressFn = _noop,
    prompt_version: str = "v0",
    calibrate_overall: bool = False,
    raw_features: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """只打分 + 写报告。rejudge 读 evidence.json 走这条，不碰视频。

    calibrate_overall 只给线上评估：数据集 rejudge 必须关，避免总分污染训练表。
    """
    avail = set(available) if available else _available_modalities({})

    def on_dim(done: int, total: int, label: str):
        progress(72 + int(18 * done / total), "llm_judge", {"dimension": label})

    progress(72, "llm_judge", {})
    judged = judge_all(evidence, avail, progress_callback=on_dim)
    if calibrate_overall:
        judged = apply_live_overall(judged, raw_features=raw_features)
    progress(92, "report", {})
    report, digest = attach_report(judged)
    progress(100, "done", {})
    return {
        "prompt_version": prompt_version,
        "judge_fingerprint": judge_fingerprint(),
        "overall": judged["overall"],
        "dimensions": judged["dimensions"],
        "report": report,
        "digest": digest,
        "created_at": time.time(),
    }


def _api_result_from_pack(pack: dict[str, Any], scores: dict[str, Any]) -> dict[str, Any]:
    vision_notes = pack.get("vision_notes") or []
    courseware_notes = pack.get("courseware_notes") or []
    return {
        "source": pack.get("source", "video"),
        "transcript_source": pack.get("transcript_source", "asr"),
        "video_file": pack.get("video_file", ""),
        "overall": scores["overall"],
        "dimensions": scores["dimensions"],
        "objective_features": _objective_rows(pack.get("raw_features") or {}),
        "raw_features": pack.get("raw_features") or {},
        "has_reference": pack.get("has_syllabus", False),
        "has_syllabus": pack.get("has_syllabus", False),
        "has_courseware": pack.get("has_courseware", False),
        "keyframes": [
            {
                "index": n["index"],
                "timestamp": n["timestamp"],
                "time_sec": n["time_sec"],
                "description": n["description"],
                "labels": n.get("labels") or {},
                "url": f"/api/evaluation/frame/{Path(n['path']).parent.name}/{Path(n['path']).name}",
            }
            for n in vision_notes
        ],
        "courseware_slides": [
            {
                "index": n["index"],
                "page": n.get("page", n["index"] + 1),
                "description": n["description"],
                "labels": n.get("labels") or {},
                "url": f"/api/evaluation/frame/{Path(n['path']).parent.name}/{Path(n['path']).name}",
            }
            for n in courseware_notes
        ],
        "transcript": pack.get("transcript") or {},
        "report": scores.get("report", ""),
        "digest": scores.get("digest") or {},
        "created_at": scores.get("created_at", time.time()),
    }


def collect_script_evidence(
    transcript_text: str,
    progress: ProgressFn = _noop,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    work_stem: str = "script",
) -> dict[str, Any]:
    """无视频：讲稿当转写，再解析大纲 / 课件。"""
    eval_conf = settings.section("evaluation")
    text = (transcript_text or "").strip()
    if len(text) < 10:
        raise RuntimeError("讲稿过短或为空，请上传更完整的讲稿，或改传教学视频。")

    duration = _estimate_duration_sec(text)
    syllabus_text = (reference or "").strip() or None
    if syllabus_path:
        progress(7, "parse_materials", {"kind": "syllabus"})
        try:
            syllabus_text = load_syllabus_text(syllabus_path)
        except MaterialError as e:
            raise RuntimeError(str(e)) from e

    courseware_pack: dict[str, Any] | None = None
    if courseware_path:
        progress(8, "parse_materials", {"kind": "courseware"})
        try:
            courseware_pack = prepare_courseware(
                courseware_path, settings.frame_dir / work_stem
            )
        except MaterialError as e:
            progress(8, "parse_materials", {"warning": str(e)})
            courseware_pack = None
        if courseware_pack and courseware_pack.get("warning"):
            progress(8, "parse_materials", {"warning": courseware_pack["warning"]})

    progress(20, "objective_features", {})
    features: dict[str, dict] = {"text": extract_text_features(text, duration)}

    courseware_notes: list[dict] = []
    cw_pages = (courseware_pack or {}).get("pages") or []
    vlm_enabled = eval_conf.get("vlm_enabled", True)
    if vlm_enabled and cw_pages:
        progress(58, "vlm_describe", {"total": len(cw_pages), "kind": "courseware"})
        vlm_done = 0

        def on_vlm_item(_done: int, _total: int):
            nonlocal vlm_done
            vlm_done += 1
            progress(
                58 + int(12 * vlm_done / max(len(cw_pages), 1)),
                "vlm_describe",
                {"done": vlm_done, "total": len(cw_pages)},
            )

        try:
            courseware_notes = describe_courseware_pages(
                cw_pages, progress_callback=on_vlm_item
            )
            cw_feat = aggregate_courseware_features(courseware_notes)
            if cw_feat:
                features["courseware"] = cw_feat
        except ProviderError as e:
            progress(70, "vlm_describe", {"warning": f"课件页面分析失败: {e}"})

    features = {k: v for k, v in features.items() if v}
    has_cw = bool(courseware_pack)
    evidence = build_evidence(
        text,
        duration,
        features,
        None,
        syllabus_text,
        has_courseware=has_cw,
        courseware_text=(courseware_pack or {}).get("text") or "",
        courseware_notes=courseware_notes,
        courseware_visual=bool((courseware_pack or {}).get("visual")),
    )
    return {
        "video_file": "",
        "duration_sec": round(float(duration), 1),
        "has_syllabus": bool((syllabus_text or "").strip()),
        "has_courseware": has_cw,
        "evidence": _jsonable(evidence),
        "raw_features": _jsonable(features),
        "available": sorted(_available_modalities(features)),
        "transcript": {
            "full_text": text,
            "duration_sec": round(float(duration), 1),
            "language": "zh",
            "segments": [],
        },
        "vision_notes": [],
        "courseware_notes": courseware_notes,
        "source": "transcript",
        "transcript_source": "script",
    }


def evaluate_session(
    video_path: str | None = None,
    progress: ProgressFn = _noop,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript_text: str | None = None,
    transcript_path: str | None = None,
) -> dict[str, Any]:
    """四个材料入口的统一评估。产品入口要求视频；讲稿选填，有则当作转写。"""
    script = _resolve_script(transcript_text, transcript_path, progress)
    if video_path:
        options = {"version": 2, "evaluation": settings.section("evaluation"),
                   "asr": settings.section("asr"), "reference": reference, "script": script}
        for name, path in (("syllabus", syllabus_path), ("courseware", courseware_path)):
            options[name] = checkpoints.identity(path, {}) if path else None
        signature = checkpoints.identity(video_path, options)
        checkpoint = Path(video_path).with_suffix(".evaluation-checkpoint.json")
        pack = checkpoints.read(checkpoint, signature)
        if pack is None:
            pack = collect_video_evidence(
                video_path,
                progress=progress,
                reference=reference,
                syllabus_path=syllabus_path,
                courseware_path=courseware_path,
                transcript_text=script,
            )
            audio = pack.get("raw_features", {}).get("audio", {})
            if not settings.section("evaluation").get("audio_enabled", True) or audio.get("pitch_available"):
                checkpoints.write(checkpoint, signature, pack)
        else:
            progress(70, "vlm_describe", {"phase": "cached", "warning": "已恢复完整解析检查点，继续生成评估报告"})
    else:
        pack = collect_script_evidence(
            script or "",
            progress=progress,
            reference=reference,
            syllabus_path=syllabus_path,
            courseware_path=courseware_path,
            work_stem=Path(transcript_path).stem if transcript_path else f"script_{int(time.time())}",
        )
    scores = score_from_evidence(
        pack["evidence"],
        pack["available"],
        progress=progress,
        prompt_version=LIVE_PROMPT_VERSION,
        calibrate_overall=True,
        raw_features=pack.get("raw_features"),
    )
    return _api_result_from_pack(pack, scores)


def evaluate_video(
    video_path: str,
    progress: ProgressFn = _noop,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript_text: str | None = None,
    transcript_path: str | None = None,
) -> dict[str, Any]:
    return evaluate_session(
        video_path,
        progress=progress,
        reference=reference,
        syllabus_path=syllabus_path,
        courseware_path=courseware_path,
        transcript_text=transcript_text,
        transcript_path=transcript_path,
    )


# --------------------------------------------------------------- 报告回流


def index_report(task_id: str, result: dict, user_id: str | None = None) -> None:
    """把评估报告摘要写进 eval_reports 语料库，供问答功能引用。"""
    from ..rag import add_chunks, delete_eval_report_chunks, split_text

    overall = result["overall"]
    dims = "、".join(
        f"{d['label']}{d['score']}分" for d in result["dimensions"] if d["assessed"]
    )
    summary = (
        f"教学视频评估报告（{result.get('video_file', '未命名')}）\n"
        f"综合得分 {overall['score']}/100，等级 {overall['grade']}（{overall['grade_label']}）。\n"
        f"五维得分：{dims}。\n\n"
        f"{result['report']}"
    )

    try:
        delete_eval_report_chunks(task_id, user_id)
        chunks = split_text(summary)
        add_chunks(
            "eval_reports",
            chunks,
            [
                {
                    "source": f"评估报告-{result.get('video_file', task_id[:8])}",
                    "corpus": "eval_reports",
                    "task_id": task_id,
                    "user_id": user_id or "",
                    "access_scope": "private",
                    "score": overall["score"],
                    "chunk_index": i,
                }
                for i in range(len(chunks))
            ],
        )
    except Exception as e:
        print(f"[warn] 评估报告入库失败（不影响评估结果）: {e}")
