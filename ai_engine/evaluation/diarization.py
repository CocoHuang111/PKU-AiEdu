"""说话人分离：区分教师与学生的发言，让「教学效果」维度有真实依据。

**默认关闭**（config.yaml 的 evaluation.diarization_enabled）。开启需要：
  pip install -r requirements-local.txt      # 装 pyannote.audio
  在 .env 里设 HF_TOKEN，并在 HuggingFace 上接受模型的使用条款

代价很实在：CPU 上跑 45 分钟音频约 10–20 分钟，会明显拉长整条流水线。
但不开启时，「学生发言次数」只能靠「我觉得」「老师我」这类词表粗估，
而教师讲课时说「我觉得」的频率远高于学生，那个数字是系统性高估的。
"""

from __future__ import annotations

import os

from ..config import settings


class DiarizationError(RuntimeError):
    pass


def is_enabled() -> bool:
    return bool(settings.section("evaluation").get("diarization_enabled", False))


def _load_pipeline():
    conf = settings.section("diarization")
    token = os.getenv(conf.get("hf_token_env", "HF_TOKEN"), "")
    if not token:
        raise DiarizationError(
            "说话人分离需要 HuggingFace token："
            f"请在 .env 里设置 {conf.get('hf_token_env', 'HF_TOKEN')}，"
            "并在模型页面接受使用条款。"
        )
    try:
        from pyannote.audio import Pipeline
    except ImportError as e:
        raise DiarizationError(
            "未安装 pyannote.audio：pip install -r requirements-local.txt"
        ) from e

    pipeline = Pipeline.from_pretrained(
        conf.get("model", "pyannote/speaker-diarization-3.1"),
        use_auth_token=token,
    )
    if pipeline is None:
        raise DiarizationError(
            "pyannote 模型加载失败：通常是 token 无效或未接受模型使用条款。"
        )
    return pipeline


def extract_speaker_features(audio_path: str) -> dict[str, float]:
    """跑分离并汇总。主讲人 = 总发言时长占比最高的说话人，其余归为学生。"""
    diarization = _load_pipeline()(audio_path)

    turns = [
        (float(seg.start), float(seg.end), str(label))
        for seg, _, label in diarization.itertracks(yield_label=True)
        if float(seg.end) > float(seg.start)
    ]
    if not turns:
        raise DiarizationError("说话人分离没有产出任何片段")

    totals: dict[str, float] = {}
    for start, end, label in turns:
        totals[label] = totals.get(label, 0.0) + (end - start)

    teacher = max(totals, key=lambda k: totals[k])
    speech_total = sum(totals.values())

    student_turns = [t for t in turns if t[2] != teacher]
    student_dur = sum(end - start for start, end, _ in student_turns)

    # 轮次交替：按时间排序后，教师↔学生的身份切换次数。
    # 这才是「有来有回的交流」的直接证据，比数关键词可靠得多。
    ordered = sorted(turns, key=lambda t: t[0])
    roles = [t[2] == teacher for t in ordered]
    exchanges = sum(1 for a, b in zip(roles, roles[1:]) if a != b)

    return {
        "speaker_count": len(totals),
        "teacher_speech_ratio": round(100.0 * totals[teacher] / speech_total, 1),
        "student_speech_ratio": round(100.0 * student_dur / speech_total, 1),
        "student_turn_count": len(student_turns),
        "student_turn_mean_sec": round(student_dur / len(student_turns), 1)
        if student_turns
        else 0.0,
        "turn_exchange_count": exchanges,
    }
