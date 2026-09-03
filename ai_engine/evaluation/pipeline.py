"""功能① 教学视频质量评估的编排。

evaluate_video()      完整流水线：视频 → 音频+关键帧 → ASR → 客观特征 → VLM → Judge → 报告
evaluate_transcript() 纯文本快速通道：跳过 ASR 与视觉，用于联调
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable

from ..config import settings
from ..pedagogy.loader import get_rubric, grade_of, render_prompt
from ..providers import ChatMessage, ProviderError, get_asr, get_llm
from . import diarization, media
from .gb import LIVE_PROMPT_VERSION, LIVE_SCORE_SOURCE, predict_overall
from .audio_features import extract_audio_features
from .judge import judge_all, judge_fingerprint
from .slide_features import extract_slide_features
from .text_features import (
    extract_text_features,
    segment_transcript,
    summarize_segments,
)
from .timeline_features import extract_timeline_features
from .materials import MaterialError, load_syllabus_text, prepare_courseware
from .vision import (
    aggregate_courseware_features,
    aggregate_vision_features,
    describe_courseware_pages,
    describe_keyframes,
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


def _feature_rows(features: dict, group: str) -> list[dict]:
    """把原始特征字典转成带中文标签的展示行，同时喂给 Judge 和前端。"""
    spec = get_rubric()["objective_features"].get(group, {})
    rows = []
    for key, meta in spec.items():
        if key not in features:
            continue
        rows.append(
            {
                "key": key,
                "label": meta["label"],
                "value": features[key],
                "unit": meta.get("unit", ""),
            }
        )
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


def _fallback_report(judged: dict, reason: str) -> str:
    """LLM 不可用时，用评分结果拼一份结构化报告，保证链路不断。"""
    overall = judged["overall"]
    lines = [
        f"## 总体评价\n\n综合得分 **{overall['score']}/100**（{overall['grade']} 级 · {overall['grade_label']}）。\n",
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

    judged = apply_live_overall(judge_all(evidence, {"text"}, progress_callback=on_dim))

    progress(85, "report", {})
    report = generate_report(judged)

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
        "keyframes": [],
        "courseware_slides": [],
        "transcript": {
            "full_text": text,
            "duration_sec": duration_sec,
            "language": "zh",
            "segments": [],
        },
        "report": report,
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
) -> dict[str, Any]:
    """视频 → 转写 / 客观特征 / VLM。不打分。返回可序列化的证据包。"""
    eval_conf = settings.section("evaluation")
    video_path = str(video_path)
    video_stem = Path(video_path).stem

    progress(5, "extracting_audio", {})
    audio_path = media.extract_audio(video_path)
    duration = media.probe_duration(video_path)

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
            keyframes = media.extract_keyframes(video_path, duration=duration)
        except media.MediaError as e:
            progress(10, "keyframe_sampling", {"warning": str(e)})

    progress(15, "asr", {})

    def on_asr(done_sec: float, total_sec: float):
        pct = 15 + int(30 * min(done_sec / max(total_sec, 1), 1.0))
        progress(pct, "asr", {"done_sec": round(done_sec), "total_sec": round(total_sec)})

    asr_result = get_asr().transcribe(audio_path, progress_callback=on_asr)
    duration = duration or asr_result.duration

    if not asr_result.text.strip():
        raise RuntimeError(
            "语音识别结果为空。请确认视频含有清晰的中文语音，"
            "或在 config.yaml 中把 asr.model 换成 small / medium 再试。"
        )

    progress(46, "objective_features", {})
    segments = segment_transcript(
        asr_result.segments, eval_conf.get("segment_minutes", 5)
    )

    text_features = extract_text_features(asr_result.text, duration)
    text_features.update(summarize_segments(segments))

    features: dict[str, dict] = {
        "text": text_features,
        "timeline": extract_timeline_features(asr_result.segments),
    }

    if eval_conf.get("audio_enabled", True):
        try:
            features["audio"] = extract_audio_features(
                audio_path, asr_result.segments
            )
        except Exception as e:
            progress(46, "objective_features", {"warning": f"声学特征提取失败: {e}"})

    if eval_conf.get("slide_detection_enabled", True):
        progress(50, "slide_detection", {})
        try:
            features["slides"] = extract_slide_features(
                video_path,
                asr_result.segments,
                interval_sec=eval_conf.get("slide_sample_interval_sec", 3.0),
                change_threshold=eval_conf.get("slide_change_threshold", 0.08),
            )
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
        "video_file": Path(video_path).name,
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
    }


def apply_live_overall(
    judged: dict[str, Any],
    *,
    model_path: Path | str | None = None,
) -> dict[str, Any]:
    """五维仍用 Judge；总分改成 2018 v9 五维 5 分类 GB。等权平均保留备查。"""
    overall = judged["overall"]
    equal_weight = overall.get("score")
    pred = predict_overall(judged.get("dimensions") or [], model_path=model_path)
    overall.update(
        {
            "score": pred["score"],
            **grade_of(pred["score"]),
            "score_source": LIVE_SCORE_SOURCE,
            "equal_weight_score": equal_weight,
            "gb_label": pred["label"],
            "gb_score_5": pred["score_5"],
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
        judged = apply_live_overall(judged)
    progress(92, "report", {})
    report = generate_report(judged)
    progress(100, "done", {})
    return {
        "prompt_version": prompt_version,
        "judge_fingerprint": judge_fingerprint(),
        "overall": judged["overall"],
        "dimensions": judged["dimensions"],
        "report": report,
        "created_at": time.time(),
    }


def _api_result_from_pack(pack: dict[str, Any], scores: dict[str, Any]) -> dict[str, Any]:
    vision_notes = pack.get("vision_notes") or []
    courseware_notes = pack.get("courseware_notes") or []
    return {
        "source": "video",
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
        "created_at": scores.get("created_at", time.time()),
    }


def evaluate_video(
    video_path: str,
    progress: ProgressFn = _noop,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
) -> dict[str, Any]:
    pack = collect_video_evidence(
        video_path,
        progress=progress,
        reference=reference,
        syllabus_path=syllabus_path,
        courseware_path=courseware_path,
    )
    scores = score_from_evidence(
        pack["evidence"],
        pack["available"],
        progress=progress,
        prompt_version=LIVE_PROMPT_VERSION,
        calibrate_overall=True,
    )
    return _api_result_from_pack(pack, scores)


# --------------------------------------------------------------- 报告回流


def index_report(task_id: str, result: dict) -> None:
    """把评估报告摘要写进 eval_reports 语料库，供问答功能引用。"""
    from ..rag import add_chunks, split_text

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
        chunks = split_text(summary)
        add_chunks(
            "eval_reports",
            chunks,
            [
                {
                    "source": f"评估报告-{result.get('video_file', task_id[:8])}",
                    "corpus": "eval_reports",
                    "task_id": task_id,
                    "score": overall["score"],
                    "chunk_index": i,
                }
                for i in range(len(chunks))
            ],
        )
    except Exception as e:
        print(f"[warn] 评估报告入库失败（不影响评估结果）: {e}")
