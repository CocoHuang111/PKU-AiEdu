"""客观特征自检：不调任何大模型，验证本地特征链路与提示词渲染。

    python -m scripts.check_features

覆盖阶段 1–6 引入的所有本地计算：词表统计、分段汇总、
ASR 置信度、VLM 标签解析与聚合、大纲/课件评分口径、提示词渲染。
课件切换检测会用 ffmpeg 现造整屏切换、角落小块切换、移动色块三类视频来验证。
说话人分离（阶段 6）默认关闭且需要 HF token，这里只验证开关与降级路径。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from ai_engine.evaluation.judge import _skip_reason
from ai_engine.evaluation.pipeline import (
    _available_modalities,
    _objective_rows,
    build_evidence,
    strip_report_digest,
)
from ai_engine.evaluation.text_features import (
    extract_text_features,
    segment_transcript,
    summarize_segments,
)
from ai_engine.evaluation.timeline_features import extract_timeline_features
from ai_engine.evaluation.transcript_punc import (
    needs_punctuation,
    parse_numbered_lines,
    punctuate_asr_result,
    punctuate_texts,
    rule_punctuate,
)
from ai_engine.evaluation.vision import (
    _parse_courseware_labels,
    _parse_labels,
    _parse_roi_payload,
    aggregate_courseware_features,
    aggregate_vision_features,
    render_label_text,
)
from ai_engine.pedagogy.loader import get_rubric, load_yaml, render_prompt
from ai_engine.providers.base import ASRResult, ASRSegment

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
    check(
        "切换时刻写入 raw 供总览时间轴",
        f.get("slide_change_times") == [6.0, 12.0],
        f"= {f.get('slide_change_times')}",
    )
    check("停留中位时长 = 6 秒", f["dwell_median_sec"] == 6.0, f"= {f['dwell_median_sec']}")
    check(
        "逐次停留已保存",
        f.get("dwell_samples") == [6.0, 6.0, 6.0],
        f"= {f.get('dwell_samples')}",
    )
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

    corner = Path(tmp).with_name("corner_slides.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "lavfi", "-i", "color=c=black:s=320x180:d=18",
         "-f", "lavfi", "-i", "color=c=white:s=60x40:d=6",
         "-f", "lavfi", "-i", "color=c=red:s=60x40:d=6",
         "-f", "lavfi", "-i", "color=c=gray:s=60x40:d=6",
         "-filter_complex",
         "[1][2][3]concat=n=3:v=1[ov];[0][ov]overlay=250:10",
         str(corner)],
        check=True, capture_output=True,
    )
    import numpy as np

    frames = list(media.iter_gray_frames(corner, interval_sec=1.0))
    global_hits = 0
    prev = None
    for fr in frames:
        if prev is not None:
            diff = float(np.abs(fr.astype(np.int16) - prev).mean()) / 255.0
            if diff > 0.08:
                global_hits += 1
        prev = fr.astype(np.int16)
    check(
        "角落小投影整帧平均会漏报",
        global_hits == 0,
        f"整帧命中 {global_hits} 次",
    )
    corner_feat = extract_slide_features(str(corner), interval_sec=1.0)
    check(
        "格子帧差能抓住角落小投影的两次翻页",
        corner_feat["slide_change_count"] == 2,
        f"= {corner_feat['slide_change_count']} 次 {corner_feat.get('slide_change_times')}",
    )
    boxed = extract_slide_features(
        str(corner),
        interval_sec=1.0,
        rois=[{"kind": "slide", "x": 0.78, "y": 0.05, "w": 0.19, "h": 0.23}],
    )
    check(
        "框住角落投影后仍能检出两次翻页",
        boxed["slide_change_count"] == 2,
        f"= {boxed['slide_change_count']} 次",
    )
    missed = extract_slide_features(
        str(corner),
        interval_sec=1.0,
        rois=[{"kind": "slide", "x": 0.02, "y": 0.55, "w": 0.25, "h": 0.30}],
    )
    check(
        "框在没有投影的角落则不计翻页",
        missed["slide_change_count"] == 0,
        f"= {missed['slide_change_count']} 次",
    )

    moving = Path(tmp).with_name("moving_blob.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "lavfi", "-i", "color=c=black:s=320x180:d=12",
         "-f", "lavfi", "-i", "color=c=white:s=40x40:d=12",
         "-filter_complex", "[0][1]overlay=x='10+22*t':y=70",
         str(moving)],
        check=True, capture_output=True,
    )
    moving_feat = extract_slide_features(str(moving), interval_sec=1.0)
    check(
        "持续移动的色块不记成翻页",
        moving_feat["slide_change_count"] == 0,
        f"= {moving_feat['slide_change_count']} 次",
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
        _prefer_usable_courseware,
        is_valid_pptx,
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

    broken = tmp / "broken.pptx"
    broken.write_bytes(b"PK\x03\x04" + b"\xff" * 200)
    check("截断 pptx 判定无效", is_valid_pptx(broken) is False)
    sibling_pdf = tmp / "broken.pdf"
    sibling_pdf.write_bytes(pdf.read_bytes())
    used, warn = _prefer_usable_courseware(broken)
    check("损坏 pptx 改用同名 PDF", used.resolve() == sibling_pdf.resolve() and "改用" in warn)
    pack_fb = prepare_courseware(broken, tmp / "out_fb", max_pages=4)
    check("损坏 pptx 仍能渲染旁边的 PDF", pack_fb["visual"] and pack_fb["pages"])
    check("损坏 pptx 留下 warning", "不是完整 PPTX" in (pack_fb.get("warning") or ""))

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

    print("\n=== 3. ASR 置信度 ===")
    tl = extract_timeline_features(make_segments())
    check("不再输出提问等待指标", not any(k.startswith("wait_") for k in tl))
    check("转写置信度已算出", "asr_confidence" in tl, f"= {tl.get('asr_confidence')}")
    check(
        "低置信占比已算出",
        "asr_low_confidence_ratio" in tl,
        f"= {tl.get('asr_low_confidence_ratio')}%",
    )
    check("无 avg_logprob 时不报置信度", "asr_confidence" not in extract_timeline_features(
        [ASRSegment(0, 5, "测试"), ASRSegment(5, 10, "测试")]
    ))

    print("\n=== 3b. 转写补标点 ===")
    wall = "同学们好今天我们讲卷积神经网络有没有同学记得什么叫感受野"
    check("无标点的中文需要补", needs_punctuation(wall))
    check(
        "已有标点则跳过",
        not needs_punctuation(
            "同学们好。今天我们讲卷积神经网络。首先回顾一下上节课的内容。"
            "有没有同学记得什么叫感受野。"
        ),
    )
    check("英文短句不补中文标点", not needs_punctuation("Hello, this is a lecture."))
    ruled = rule_punctuate(wall)
    check("规则兜底会加上中文标点", bool(re.findall(r"[。？！，]", ruled)), f"= {ruled[:40]}")
    parsed = parse_numbered_lines(
        "1. 同学们好，今天我们讲卷积神经网络。\n2. 有没有同学记得什么叫感受野？\n",
        2,
    )
    check(
        "能解析带行号的补标点输出",
        parsed == ["同学们好，今天我们讲卷积神经网络。", "有没有同学记得什么叫感受野？"],
        f"= {parsed}",
    )
    fake = lambda prompt: (
        "1. 同学们好，今天我们讲卷积神经网络。\n2. 有没有同学记得什么叫感受野？"
    )
    filled = punctuate_texts(
        ["同学们好今天我们讲卷积神经网络", "有没有同学记得什么叫感受野"],
        llm_fn=fake,
    )
    check("LLM 补标点后片段数不变", len(filled) == 2)
    check("问句被补上问号", filled[1].endswith("？"), f"= {filled[1]}")
    rewritten = punctuate_texts(
        ["同学们好今天我们讲卷积神经网络"],
        llm_fn=lambda _: "1. 本节课改讲循环神经网络，内容与原文无关。",
    )
    check(
        "改写内容会被丢掉并走规则兜底",
        "循环神经网络" not in rewritten[0],
        f"= {rewritten[0][:40]}",
    )
    asr = ASRResult(
        text=wall,
        segments=[
            ASRSegment(0.0, 6.0, "同学们好今天我们讲卷积神经网络"),
            ASRSegment(6.0, 12.0, "有没有同学记得什么叫感受野"),
        ],
        language="zh",
        duration=12.0,
    )
    punctuated = punctuate_asr_result(asr, llm_fn=fake)
    check("补标点后时间戳不变", punctuated.segments[0].start == 0.0 and punctuated.segments[1].end == 12.0)
    check("全文由补过标点的片段重拼", "？" in punctuated.text and punctuated.text.startswith("同学们好"))

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

    walk_screen = _parse_labels(
        '{"gaze":"screen","gesture":"none","posture":"walking"}'
    )
    check("走动中未指向屏幕不记成看屏幕", walk_screen["gaze"] == "students")
    point_screen = _parse_labels(
        '{"gaze":"screen","gesture":"pointing","posture":"walking"}'
    )
    check("走动中指向屏幕仍记看屏幕", point_screen["gaze"] == "screen")

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

    boxed, full = _parse_roi_payload(
        '{"slide":{"x":0.62,"y":0.08,"w":0.3,"h":0.4},"blackboard":null}'
    )
    check(
        "能解析投影框",
        len(boxed) == 1 and boxed[0]["kind"] == "slide" and abs(boxed[0]["x"] - 0.62) < 0.01,
        f"= {boxed}",
    )
    boxed, full = _parse_roi_payload(
        '{"slide":{"x":0,"y":0,"w":1,"h":1},"blackboard":null}'
    )
    check("整幅录屏不裁小框", full is True and boxed == [])
    boxed, full = _parse_roi_payload(
        '{"slide":{"x":62,"y":10,"w":30,"h":40},"blackboard":null}'
    )
    check(
        "百分数坐标会换成 0-1",
        boxed and abs(boxed[0]["x"] - 0.62) < 0.02,
        f"x={boxed[0]['x'] if boxed else None}",
    )
    boxed, full = _parse_roi_payload('{"slide":null,"blackboard":null}')
    check("没有投影板书时框为空", boxed == [] and full is False)

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
    check(
        "教学目标与定位已成为独立二级指标",
        indicators["goal_clarity"]["label"] == "教学目标与定位"
        and len(indicators["goal_clarity"]["criteria"]) == 3,
    )

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
    speech = next((r for r in rows["text"] if r["key"] == "speech_rate"), None)
    check("语速行带 ideal，供前端比例条标区间", bool(speech) and speech.get("ideal") == [200, 280])

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
        "不要当成读屏",
        "课件时序特征",
        "系统性偏高",
        "弱代理",
        "只报你有**明确把握**的知识性错误",
        "不要机械要求教师口头宣读教学目标",
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
    check("视觉提示词区分侧面走动与看屏幕", "左右横移" in vision_prompt and "students" in vision_prompt)
    roi_prompt = render_prompt("eval_screen_roi.j2", timestamp="05:00")
    check(
        "投影定位提示词要求 JSON",
        '"slide"' in roi_prompt and "blackboard" in roi_prompt and "0~1" in roi_prompt,
    )
    ev_roi = build_evidence(
        SAMPLE,
        300,
        {"text": tf, "slides": {"slide_change_count": 4, "slide_roi_source": "vlm"}},
    )
    prompt_roi = render_prompt("eval_judge.j2", dimension=method, evidence=ev_roi)
    check("框到投影后提示词说明只比对框内", "框出的投影" in prompt_roi)
    cw_prompt = render_prompt("eval_courseware.j2", page=2, page_count=10)
    check("课件提示词要求 JSON", '"layout"' in cw_prompt and "unclear" in cw_prompt)

    reflect = render_prompt(
        "eval_reflect.j2",
        comment="建议增加互动，PPT 文字偏多。",
        llm_summary="总分 72\n- 教学效果 45：互动少",
        expert_score_line="专家均分 3.35（2–4 分制，约合百分 67.5）",
    )
    check("reflect 面向未来无专家的 Judge", "未来评分员" in reflect and "没有**专家评语" in reflect)
    check("reflect 禁止听感/对齐句式", "禁止出现「专家」" in reflect and "听感" in reflect)
    check("reflect 不要求客观特征表", "不要加入客观特征表" in reflect)
    check("reflect 带入专家均分", "约合百分 67.5" in reflect)
    distill = render_prompt(
        "eval_distill.j2",
        existing_bullets="（无）",
        lessons_numbered="1. 微格纯讲授中互动少只作建议，不作为效果维主缺陷",
    )
    check("distill 面向无专家时的偏好", "没有专家评语时" in distill)
    check("distill 要求问句选定一边", "必须选定一边" in distill)
    judge_lessons = render_prompt(
        "eval_judge.j2",
        dimension=dim,
        evidence=evidence,
        expert_lessons="- 微格纯讲授中互动少只作建议，不作为效果维主缺陷",
    )
    check("Judge 注入历史偏好", "历史评审偏好" in judge_lessons and "主缺陷" in judge_lessons)
    report_prompt = render_prompt(
        "eval_report.j2",
        overall={
            "score": 80,
            "grade": "B",
            "grade_label": "良好",
            "duration_minutes": 20,
            "modalities": ["text"],
            "skipped_indicators": 0,
        },
        dimensions=[],
    )
    check("报告要求诊断摘要两点", "每类恰好 2 条" in report_prompt and "## 〇、诊断摘要" in report_prompt)
    check("提示词写明摘要不进诊断报告", "从诊断报告里拿掉" in report_prompt)
    stripped = strip_report_digest(
        "## 〇、诊断摘要\n\n### 突出优点\n- 示例\n\n## 一、总体评价\n正文\n"
    )
    check("诊断摘要会从报告正文剔除", "诊断摘要" not in stripped and "总体评价" in stripped)

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
