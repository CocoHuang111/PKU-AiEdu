"""客观特征自检：不调任何大模型，验证本地特征链路与提示词渲染。

    python -m scripts.check_features

覆盖阶段 1–6 引入的所有本地计算：词表统计、分段汇总、提问等待时间、
ASR 置信度、VLM 标签解析与聚合、大纲/课件评分口径、提示词渲染。
课件切换检测会用 ffmpeg 现造一段切换时刻已知的视频来验证。
说话人分离（阶段 6）默认关闭且需要 HF token，这里只验证开关与降级路径。
"""

from __future__ import annotations

import sys
from pathlib import Path

from ai_engine.evaluation.judge import _skip_reason
from ai_engine.evaluation.pipeline import (
    _available_modalities,
    _objective_rows,
    build_evidence,
)
from ai_engine.evaluation.text_features import (
    extract_text_features,
    segment_transcript,
    summarize_segments,
)
from ai_engine.evaluation.timeline_features import extract_timeline_features
from ai_engine.evaluation.vision import (
    _parse_courseware_labels,
    _parse_labels,
    aggregate_courseware_features,
    aggregate_vision_features,
    render_label_text,
)
from ai_engine.pedagogy.loader import get_rubric, load_yaml, render_prompt
from ai_engine.providers.base import ASRSegment

PASS, FAIL = "  ✓", "  ✗"
failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{PASS if ok else FAIL} {label}{f'  {detail}' if detail else ''}")
    if not ok:
        failures.append(label)


SAMPLE = (
    "同学们好，今天我们讲卷积神经网络。首先回顾一下上节课的内容。"
    "有没有同学记得什么叫感受野？这位同学你来说。"
    "很好。那么为什么加深网络反而会让训练误差上升呢？大家想一想。"
    "我们打个比方，这就好比传声筒游戏。接下来看一个案例，"
    "2024 年 ImageNet 上最新的研究成果表明，残差连接能缓解这个问题。"
    "在实际应用中，比如说自动驾驶的感知模块就大量用到它。"
    "那个，这个这个，我们再分析一下它的梯度是怎么传播的。"
    "老师我有个问题，残差连接会不会增加参数量？这是个好问题。"
    "最后总结一下，本节课的重点是残差结构的设计动机。"
)


def make_segments() -> list[ASRSegment]:
    """构造带时间戳的片段：第 2 段以提问收尾，之后留白 4.2 秒。"""
    return [
        ASRSegment(0.0, 12.0, "同学们好，今天我们讲卷积神经网络。", -0.22, 0.01),
        ASRSegment(12.0, 24.0, "有没有同学记得什么叫感受野？", -0.31, 0.02),
        ASRSegment(28.2, 40.0, "很好，感受野就是输出对应输入的区域。", -0.28, 0.01),
        ASRSegment(40.0, 52.0, "那么为什么加深网络会让误差上升呢？", -0.75, 0.03),
        ASRSegment(53.0, 65.0, "我们打个比方，这就好比传声筒游戏。", -0.30, 0.01),
    ]


def check_slides() -> None:
    """用 ffmpeg 现造一段「黑 6 秒 → 白 6 秒 → 灰 6 秒」的视频，切换时刻已知。"""
    import shutil
    import subprocess
    import tempfile

    from ai_engine.evaluation import media
    from ai_engine.evaluation.slide_features import _scan_frames, extract_slide_features

    if not shutil.which("ffmpeg"):
        check("ffmpeg 可用（跳过课件检测自检）", False, "未安装 ffmpeg")
        return

    tmp = Path(tempfile.mkdtemp()) / "three_slides.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "lavfi", "-i", "color=c=black:s=320x180:d=6",
         "-f", "lavfi", "-i", "color=c=white:s=320x180:d=6",
         "-f", "lavfi", "-i", "color=c=gray:s=320x180:d=6",
         "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0", str(tmp)],
        check=True, capture_output=True,
    )

    total, changes, blank = _scan_frames(
        media.iter_gray_frames(tmp, interval_sec=1.0), 0.08
    )
    check("流式抽帧帧数正确", total == 18, f"= {total}")
    check("切换位置正确（第 6、12 秒）", changes == [6, 12], f"= {changes}")

    segs = [
        ASRSegment(0.0, 6.0, "首先我们看第一部分。"),
        ASRSegment(6.0, 12.0, "接下来讲第二部分。"),
        ASRSegment(12.0, 18.0, "最后总结一下。"),
    ]
    f = extract_slide_features(tmp, segs, interval_sec=1.0, change_threshold=0.08)
    check("切换次数 = 2", f["slide_change_count"] == 2, f"= {f['slide_change_count']}")
    check("停留中位时长 = 6 秒", f["dwell_median_sec"] == 6.0, f"= {f['dwell_median_sec']}")
    check(
        "停留不足 20 秒占比 = 100%",
        f["dwell_short_ratio"] == 100.0,
        f"= {f['dwell_short_ratio']}%",
    )
    check("有过渡话语时同步率 = 100%", f["slide_sync_ratio"] == 100.0, f"= {f['slide_sync_ratio']}%")

    no_transition = extract_slide_features(
        tmp, [ASRSegment(0.0, 18.0, "嗯这个数值是这样的。")],
        interval_sec=1.0, change_threshold=0.08,
    )
    check("无过渡话语时同步率 = 0%", no_transition["slide_sync_ratio"] == 0.0)

    no_asr = extract_slide_features(tmp, [], interval_sec=1.0, change_threshold=0.08)
    check("无转写时不报同步率（缺测 ≠ 实测为 0）", "slide_sync_ratio" not in no_asr)

    loose = extract_slide_features(tmp, segs, interval_sec=1.0, change_threshold=0.99)
    check(
        "阈值调大后切换更少（方向正确）",
        loose["slide_change_count"] < f["slide_change_count"],
        f"0.99 → {loose['slide_change_count']} 次",
    )

    try:
        list(media.iter_gray_frames("/etc/hosts", interval_sec=1.0))
        check("非视频文件抛可读错误", False, "未抛异常")
    except media.MediaError:
        check("非视频文件抛可读错误", True)
    except Exception as e:
        check("非视频文件抛可读错误", False, type(e).__name__)


def check_materials() -> None:
    import tempfile

    import fitz

    from ai_engine.evaluation.materials import (
        _pick_indices,
        load_syllabus_text,
        prepare_courseware,
    )

    check("_pick_indices 均匀抽样", _pick_indices(10, 3) == [0, 5, 9])
    check("页数不足时全取", _pick_indices(2, 16) == [0, 1])

    tmp = Path(tempfile.mkdtemp())
    syllabus = tmp / "syllabus.txt"
    syllabus.write_text("本节课：残差连接与感受野\n进度：第 3 讲", encoding="utf-8")
    text = load_syllabus_text(syllabus)
    check("大纲文本抽出中文", "残差连接" in text)

    pdf = tmp / "lesson.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Residual connection and receptive field")
    doc.save(str(pdf))
    doc.close()

    pack = prepare_courseware(pdf, tmp / "out", max_pages=4)
    check("课件 PDF 渲染出页面", pack["visual"] and len(pack["pages"]) == 1)
    check("课件抽出文本", "Residual" in pack["text"])
    check("渲染文件存在", Path(pack["pages"][0]["path"]).is_file())

    labels = _parse_courseware_labels(
        '{"layout":"clear","density":"moderate","content":"diagram",'
        '"readable":"high","note":"残差结构示意图"}'
    )
    notes = [{"ok": True, "labels": labels}]
    feat = aggregate_courseware_features(notes)
    check("课件版式清楚占比 100", feat["cw_layout_clear_ratio"] == 100.0)
    check("课件可读性高占比 100", feat["cw_readable_high_ratio"] == 100.0)
    check("失败页不进分母", aggregate_courseware_features([{"ok": False, "labels": {}}]) == {})
    registered = set(get_rubric()["objective_features"]["courseware"])
    missing = sorted(k for k in feat if k not in registered)
    check("课件特征已在 rubric 登记", not missing, f"缺标签: {missing}" if missing else "")


def main() -> int:
    print("\n=== 1. 词表与文本特征 ===")
    lex = load_yaml("feature_lexicon.yaml")
    for group in (
        "case_markers",
        "recency_markers",
        "bloom_higher_markers",
        "bloom_lower_markers",
        "discipline_markers",
    ):
        check(f"词表 {group} 已定义", bool(lex.get(group)), f"{len(lex.get(group, []))} 条")
    check(
        "点名词已从 interaction_markers 移出",
        "请回答" not in lex["interaction_markers"]
        and "请回答" in lex["discipline_markers"],
    )

    tf = extract_text_features(SAMPLE, 300)
    for key in (
        "case_count",
        "recency_count",
        "year_ref_count",
        "discipline_count",
        "higher_order_question_ratio",
        "classified_question_count",
    ):
        check(f"新增特征 {key}", key in tf, f"= {tf.get(key)}")
    check("案例引入被识别", tf["case_count"] >= 2, f"= {tf['case_count']}")
    check("年份引用被识别", tf["year_ref_count"] == 1, f"= {tf['year_ref_count']}")
    check("前沿表述被识别", tf["recency_count"] >= 1, f"= {tf['recency_count']}")
    check("纪律/点名被识别", tf["discipline_count"] >= 1, f"= {tf['discipline_count']}")
    check(
        "高阶问题占比在 0-100",
        0 <= tf["higher_order_question_ratio"] <= 100,
        f"= {tf['higher_order_question_ratio']}%",
    )

    print("\n=== 2. 分段汇总 ===")
    chunks = segment_transcript(make_segments(), minutes_per_chunk=0.3)
    check("分段成功", len(chunks) >= 2, f"{len(chunks)} 段")
    summary = summarize_segments(chunks)
    for key in ("speech_rate_cv", "question_gini", "question_free_segment_ratio"):
        check(f"汇总特征 {key}", key in summary, f"= {summary.get(key)}")
    check("单段时不做汇总", summarize_segments(chunks[:1]) == {})
    check(
        "基尼系数在 0-1",
        0.0 <= summary["question_gini"] <= 1.0,
        f"= {summary['question_gini']}",
    )

    print("\n=== 3. 提问等待时间与 ASR 置信度 ===")
    tl = extract_timeline_features(make_segments())
    check("等待时间有样本", tl.get("wait_time_sample_count", 0) >= 1, f"= {tl.get('wait_time_sample_count')}")
    check("平均等待时间已算出", "wait_time_mean" in tl, f"= {tl.get('wait_time_mean')}s")
    check(
        "4.2 秒留白被判为有效等待",
        tl.get("wait_time_effective_ratio", 0) > 0,
        f"= {tl.get('wait_time_effective_ratio')}%",
    )
    check("转写置信度已算出", "asr_confidence" in tl, f"= {tl.get('asr_confidence')}")
    check(
        "低置信占比已算出",
        "asr_low_confidence_ratio" in tl,
        f"= {tl.get('asr_low_confidence_ratio')}%",
    )
    check("无 avg_logprob 时不报置信度", "asr_confidence" not in extract_timeline_features(
        [ASRSegment(0, 5, "测试"), ASRSegment(5, 10, "测试")]
    ))

    print("\n=== 4. VLM 结构化标签 ===")
    raw = (
        '```json\n{"gaze":"students","gesture":"pointing","posture":"walking",'
        '"board_present":"slide","board_content":"mixed","board_readable":"high",'
        '"students_visible":24,"heads_up":"high","hands_raised":"no",'
        '"note":"教师侧身指向投影"}\n```'
    )
    labels = _parse_labels(raw)
    check("代码块包裹的 JSON 能解析", labels["gaze"] == "students")
    check("人数解析正确", labels["students_visible"] == 24)
    check("标签渲染成中文", "看学生" in render_label_text(labels))

    bad = _parse_labels('{"gaze":"看学生","students_visible":"很多"}')
    check("表外取值归为 unclear", bad["gaze"] == "unclear", f"= {bad['gaze']}")
    check("非法人数归为 None", bad["students_visible"] is None)

    notes = [
        {"ok": True, "labels": labels},
        {"ok": True, "labels": _parse_labels('{"gaze":"script","board_readable":"low","heads_up":"unclear"}')},
        {"ok": False, "labels": {}},
    ]
    vf = aggregate_vision_features(notes)
    check("聚合只统计成功帧", vf["frames_analyzed"] == 2, f"= {vf['frames_analyzed']}")
    check("看学生占比 = 50%", vf["gaze_students_ratio"] == 50.0, f"= {vf['gaze_students_ratio']}%")
    check("看讲稿占比 = 50%", vf["gaze_script_ratio"] == 50.0, f"= {vf['gaze_script_ratio']}%")
    check(
        "unclear 留在分母",
        vf["heads_up_unclear_ratio"] == 50.0,
        f"= {vf['heads_up_unclear_ratio']}%",
    )
    check("全部失败时返回空", aggregate_vision_features([{"ok": False, "labels": {}}]) == {})

    print("\n=== 5. rubric 与代码对齐 ===")
    rubric = get_rubric()
    groups = rubric["objective_features"]
    for g in ("text", "audio", "timeline", "vision", "slides", "speakers", "courseware"):
        check(f"objective_features.{g} 已定义", g in groups, f"{len(groups.get(g, {}))} 项")

    indicators = {i["key"]: i for d in rubric["dimensions"] for i in d["indicators"]}
    check("语速笔误已修为语调", any(
        "语调积极" in c for c in indicators["teacher_bearing"]["criteria"]
    ))
    check("教学资源融合已统一", indicators["resource_integration"]["label"] == "教学资源融合")
    check(
        "高阶问题已移到重点难点设计",
        any("高阶" in c for c in indicators["key_difficulty"]["criteria"])
        and not any("高阶" in c for c in indicators["frontier"]["criteria"]),
    )
    check("知识准确性已降权", indicators["accuracy"]["weight"] < 1.0, f"= {indicators['accuracy']['weight']}")
    check("内容完整性不强制参照", indicators["completeness"].get("requires_reference") is not True)

    # 三级观测点必须以 evaluation_criterion.md 为准，不允许 rubric 自行扩写
    from ai_engine.config import settings as _settings

    criterion_text = (_settings.root / "evaluation_criterion.md").read_text(encoding="utf-8")
    allowed = {
        line[1:].strip()
        for line in criterion_text.splitlines()
        if line.startswith("- ")
    }
    extras = sorted(
        {
            c
            for ind in indicators.values()
            for c in ind["criteria"]
            if c not in allowed
        }
    )
    check("rubric 三级观测点未超出指标文档", not extras, f"多出: {extras}" if extras else "")
    for extra_phrase in ("课堂秩序良好", "承接关系", "显性呈现", "难点有拆解", "对学生反馈"):
        check(
            f"已删除扩写「{extra_phrase}」",
            not any(extra_phrase in c for ind in indicators.values() for c in ind["criteria"]),
        )

    # 代码算出来的 key 必须在 rubric 里有标签，否则前端和 Judge 都看不到
    declared = set(groups["text"]) | set(groups["timeline"]) | set(groups["vision"])
    computed = set(tf) | set(summary) | set(tl) | set(vf)
    missing = sorted(
        k
        for k in computed - declared
        if k not in {"duration_minutes", "total_chars", "sentence_count",
                     "open_question_count", "question_count", "filler_count",
                     "higher_order_question_count", "segment_count"}
    )
    check("无未登记的特征 key", not missing, f"缺标签: {missing}" if missing else "")

    print("\n=== 6. 大纲对照与缺参照 ===")
    ev_no_ref = build_evidence(SAMPLE, 300, {"text": tf})
    ev_ref = build_evidence(SAMPLE, 300, {"text": tf}, reference="1. 残差连接\n2. 感受野")
    check(
        "无大纲时内容完整性仍可评",
        _skip_reason(indicators["completeness"], ev_no_ref, {"text"}) is None,
    )
    check(
        "有大纲时内容完整性可评",
        _skip_reason(indicators["completeness"], ev_ref, {"text"}) is None,
    )
    check(
        "模态缺失仍然跳过",
        _skip_reason(indicators["blackboard"], ev_ref, {"text"}) == "",
    )
    check("大纲文本进了证据包", "残差连接" in ev_ref["reference"] and ev_ref["has_syllabus"])
    check("无大纲时 has_syllabus 为假", ev_no_ref["has_syllabus"] is False)

    print("\n=== 7. 模态点亮与输出结构 ===")
    check("只有文本时 = {text}", _available_modalities({"text": tf}) == {"text"})
    check(
        "帧差检测点亮 vision（无需 VLM）",
        "vision" in _available_modalities({"text": tf, "slides": {"slide_change_count": 9}}),
    )
    check(
        "说话人分离点亮 audio",
        "audio" in _available_modalities({"text": tf, "speakers": {"speaker_count": 2}}),
    )
    check(
        "上传课件点亮 vision",
        "vision" in _available_modalities(
            {"text": tf, "courseware": {"cw_readable_high_ratio": 80.0}}
        ),
    )
    rows = _objective_rows({"text": tf, "timeline": tl, "vision": vf})
    check("输出结构含全部 7 组", len(rows) == 7, f"= {sorted(rows)}")
    check("空分组渲染为空列表", rows["speakers"] == [] and rows["courseware"] == [])

    print("\n=== 8. 提示词渲染 ===")
    dim = next(d for d in rubric["dimensions"] if d["key"] == "teaching_content")
    evidence = build_evidence(
        SAMPLE,
        300,
        {"text": tf, "timeline": tl, "vision": vf, "slides": {"slide_change_count": 9}},
        vision_notes=[{"ok": True, "timestamp": "05:00", "description": "看学生 · 指向板书"}],
        reference="1. 残差连接的设计动机\n2. 感受野",
    )
    prompt = render_prompt("eval_judge.j2", dimension=dim, evidence=evidence)
    for marker in (
        "三级指标",
        "本节课内容完整闭环",
        "残差连接的设计动机",
        "对照这份大纲",
        "时序特征",
        "视觉观测统计",
        "课件时序特征",
        "系统性偏高",
        "弱代理",
        "只报你有**明确把握**的知识性错误",
        "根据这些关键帧判断",
    ):
        check(f"提示词含「{marker[:12]}」", marker in prompt)
    check(
        "有大纲时不再禁止按大纲覆盖面打分",
        "不要用整门课程的大纲覆盖面来打分" not in prompt,
    )
    evidence_no_ref_prompt = build_evidence(SAMPLE, 300, {"text": tf})
    prompt_no_ref = render_prompt(
        "eval_judge.j2", dimension=dim, evidence=evidence_no_ref_prompt
    )
    check(
        "无大纲时改为评转写闭环",
        "没有课程大纲时" in prompt_no_ref and "知识闭环" in prompt_no_ref,
    )
    check("提示词列出全部二级指标", all(i["label"] in prompt for i in dim["indicators"]))

    method = next(d for d in rubric["dimensions"] if d["key"] == "teaching_method")
    ev_cw = build_evidence(
        SAMPLE,
        300,
        {"text": tf, "courseware": {"cw_readable_high_ratio": 80.0}},
        has_courseware=True,
        courseware_text="第 1 页 残差连接示意图",
        courseware_notes=[{"ok": True, "page": 1, "description": "版式清楚 · 可读性高"}],
        courseware_visual=True,
    )
    prompt_cw = render_prompt("eval_judge.j2", dimension=method, evidence=ev_cw)
    check("有课件时以上传课件为准", "一律以上传课件为准" in prompt_cw)
    check("有课件时不拿关键帧评版式", "根据这些关键帧判断" not in prompt_cw)

    vision_prompt = render_prompt("eval_vision.j2", timestamp="05:00")
    check("视觉提示词要求 JSON", '"gaze"' in vision_prompt and "unclear" in vision_prompt)
    cw_prompt = render_prompt("eval_courseware.j2", page=2, page_count=10)
    check("课件提示词要求 JSON", '"layout"' in cw_prompt and "unclear" in cw_prompt)

    print("\n=== 9. 课件切换检测 ===")
    check_slides()

    print("\n=== 10. 说话人分离开关 ===")
    from ai_engine.evaluation import diarization

    check("默认关闭", diarization.is_enabled() is False)
    try:
        diarization.extract_speaker_features("/nonexistent.wav")
        check("缺 token/依赖时抛可读错误", False, "未抛异常")
    except Exception as e:
        check(
            "缺 token/依赖时抛可读错误",
            isinstance(e, diarization.DiarizationError),
            type(e).__name__,
        )

    print("\n=== 11. 大纲与课件材料 ===")
    check_materials()

    print()
    if failures:
        print(f"✗ {len(failures)} 项未通过：")
        for f in failures:
            print(f"    - {f}")
        return 1
    print("✓ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
