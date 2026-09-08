"""教学沙龙视频 → 结构化 Markdown 语料。

把 `knowledge/corpora/pku_salon/raw_video/` 下的 mp4 处理成
可直接 `make ingest --corpus pku_salon` 的 Markdown 文件。

约定：
  - 视频文件名前 8 位为标准日期 YYYYMMDD，如 `20240315_互动设计.mp4`
  - 中间产物放在 `.work/`，不入向量库
  - 正式语料输出到 `pku_salon/{date}-{slug}.md`

用法：
    python -m knowledge.process_salon                  # 转写 + 结构化（默认）
    python -m knowledge.process_salon --transcribe   # 只做 Step 1
    python -m knowledge.process_salon --structure    # 只做 Step 2（需已有转写）
    python -m knowledge.process_salon --limit 1      # 试跑一条
    python -m knowledge.process_salon --force        # 忽略缓存重跑
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from ai_engine.config import settings
from ai_engine.evaluation.media import MediaError, ensure_ffmpeg, extract_audio, probe_duration
from ai_engine.pedagogy.loader import render_prompt
from ai_engine.providers import ChatMessage, ProviderError, build_asr, get_llm

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm"}
DATE_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})")


def salon_conf() -> dict:
    return settings.section("salon") or {}


def salon_root() -> Path:
    return settings.corpus_dir("pku_salon")


def raw_video_dir() -> Path:
    rel = salon_conf().get("raw_video_dir", "raw_video")
    d = salon_root() / rel
    d.mkdir(parents=True, exist_ok=True)
    return d


def work_root() -> Path:
    rel = salon_conf().get("work_dir", ".work")
    d = salon_root() / rel
    d.mkdir(parents=True, exist_ok=True)
    return d


def parse_video(path: Path) -> tuple[str, str, str]:
    """返回 (date_yyyymmdd, date_iso, slug)。"""
    stem = path.stem
    if len(stem) < 8:
        raise ValueError(f"文件名太短，前 8 位应为日期 YYYYMMDD：{path.name}")
    m = DATE_RE.match(stem[:8])
    if not m:
        raise ValueError(f"文件名前 8 位不是合法日期 YYYYMMDD：{path.name}")
    y, mo, d = m.groups()
    datetime(int(y), int(mo), int(d))  # 校验 20241399 这类非法日期
    date_yyyymmdd = f"{y}{mo}{d}"
    date_iso = f"{y}-{mo}-{d}"
    slug = stem[8:].lstrip("_-. ").strip() or "沙龙"
    slug = re.sub(r'[\\/:*?"<>|]', "-", slug)
    return date_yyyymmdd, date_iso, slug


def output_md_path(date_yyyymmdd: str, slug: str) -> Path:
    return salon_root() / f"{date_yyyymmdd}-{slug}.md"


def work_dir_for(video: Path) -> Path:
    return work_root() / video.stem


def _asr():
    conf = {**settings.flat_config("asr"), "model": salon_conf().get("asr_model", "small")}
    return build_asr(conf)


def _mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0


def _fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def _group_segments(segments: list, minutes: float) -> list[dict]:
    if not segments:
        return []
    window = minutes * 60.0
    groups: list[dict] = []
    buf: list = []
    start = segments[0].start

    for seg in segments:
        if seg.end - start > window and buf:
            groups.append(
                {
                    "start": buf[0].start,
                    "end": buf[-1].end,
                    "text": "".join(s.text for s in buf),
                }
            )
            buf = []
            start = seg.start
        buf.append(seg)
    if buf:
        groups.append(
            {
                "start": buf[0].start,
                "end": buf[-1].end,
                "text": "".join(s.text for s in buf),
            }
        )
    return groups


def transcribe_video(video: Path, force: bool = False) -> Path:
    """Step 1：抽音频 + ASR，写入 .work/{stem}/transcript.json。"""
    date_yyyymmdd, date_iso, slug = parse_video(video)
    wdir = work_dir_for(video)
    wdir.mkdir(parents=True, exist_ok=True)
    transcript_json = wdir / "transcript.json"

    if (
        transcript_json.exists()
        and not force
        and _mtime(transcript_json) >= _mtime(video)
    ):
        print(f"  [跳过转写] {video.name}（已有 transcript.json）")
        return transcript_json

    ensure_ffmpeg()
    print(f"  [转写] {video.name}  日期 {date_iso}  ASR={salon_conf().get('asr_model', 'small')}")

    audio_path = wdir / "audio.wav"
    if force or not audio_path.exists() or _mtime(audio_path) < _mtime(video):
        extract_audio(video, out_dir=wdir)
        # extract_audio 命名规则是 {stem}.wav，统一到 audio.wav
        produced = wdir / f"{video.stem}.wav"
        if produced.exists() and produced != audio_path:
            produced.rename(audio_path)

    duration = probe_duration(video)

    def on_progress(done: float, total: float) -> None:
        pct = int(100 * min(done / max(total, 1), 1.0))
        filled = round(22 * pct / 100)
        bar = "█" * filled + "░" * (22 - filled)
        mins = f"{int(done // 60)}/{max(int(total // 60), 1)} 分钟"
        print(f"\r    语音识别 [{bar}] {pct:3d}%  {mins}\033[K", end="", flush=True)

    result = _asr().transcribe(str(audio_path), progress_callback=on_progress)
    print()

    if settings.flat_config("asr").get("punctuate", True):
        print("    补标点…")
        try:
            from ai_engine.evaluation.transcript_punc import punctuate_asr_result

            result = punctuate_asr_result(result)
        except Exception as e:
            print(f"    补标点失败，沿用原转写: {e}")

    if not result.text.strip():
        raise RuntimeError(f"转写结果为空：{video.name}")

    payload = {
        "source_video": video.name,
        "date": date_yyyymmdd,
        "date_iso": date_iso,
        "slug": slug,
        "duration_sec": round(duration or result.duration, 1),
        "language": result.language,
        "asr_model": salon_conf().get("asr_model", "small"),
        "created_at": time.time(),
        "full_text": result.text,
        "segments": [
            {"start": s.start, "end": s.end, "text": s.text} for s in result.segments
        ],
    }
    transcript_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"    → {transcript_json.relative_to(salon_root())}  ({len(result.text)} 字)")
    return transcript_json


def _prepare_transcript_text(data: dict) -> str:
    """把分段转写拼成带时间戳的文本，供 LLM 阅读。"""
    minutes = salon_conf().get("segment_minutes", 5)
    max_chars = salon_conf().get("max_transcript_chars", 80000)

    class Seg:
        __slots__ = ("start", "end", "text")

        def __init__(self, d: dict):
            self.start = d["start"]
            self.end = d["end"]
            self.text = d["text"]

    segments = [Seg(s) for s in data.get("segments", [])]
    groups = _group_segments(segments, minutes)

    lines = []
    for g in groups:
        lines.append(f"[{_fmt_time(g['start'])} - {_fmt_time(g['end'])}]")
        lines.append(g["text"].strip())
        lines.append("")

    text = "\n".join(lines).strip()
    if len(text) <= max_chars:
        return text

    head = int(max_chars * 0.65)
    tail = max_chars - head
    return (
        f"{text[:head]}\n\n……（中间省略 {len(text) - max_chars} 字）……\n\n{text[-tail:]}"
    )


def structure_transcript(transcript_json: Path, force: bool = False) -> Path | None:
    """Step 2：LLM 提取教学知识，输出正式 Markdown。"""
    data = json.loads(transcript_json.read_text(encoding="utf-8"))
    date_yyyymmdd = data["date"]
    slug = data["slug"]
    out_path = output_md_path(date_yyyymmdd, slug)

    if (
        out_path.exists()
        and not force
        and _mtime(out_path) >= _mtime(transcript_json)
    ):
        print(f"  [跳过结构化] {out_path.name}（已存在且较新）")
        return out_path

    transcript = _prepare_transcript_text(data)
    duration_min = round(float(data.get("duration_sec", 0)) / 60.0, 1)

    prompt = render_prompt(
        "salon_structure.j2",
        salon_date=data.get("date_iso", date_yyyymmdd),
        source_name=data.get("source_video", transcript_json.stem),
        duration_minutes=duration_min,
        transcript=transcript,
    )

    print(f"  [结构化] {data.get('source_video')} → {out_path.name}")
    try:
        md = get_llm().chat(
            [
                ChatMessage(
                    "system",
                    "你是高校教学知识整理助手。你只输出 Markdown，不输出解释文字。",
                ),
                ChatMessage("user", prompt),
            ]
        ).strip()
    except ProviderError as e:
        raise RuntimeError(
            f"结构化失败：{e}\n"
            "提示：默认走云端 LLM，请配置 .env 的 DASHSCOPE_API_KEY；"
            "或 PKU_MODE=local 使用本地 Ollama。"
        ) from e

    if md.startswith("```"):
        md = re.sub(r"^```[a-zA-Z]*\n?", "", md)
        md = re.sub(r"\n?```$", "", md).strip()

    footer = (
        f"\n\n---\n\n"
        f"> 自动生成 · 来源 `{data.get('source_video')}` · "
        f"ASR `{data.get('asr_model', 'small')}` · "
        f"时长约 {duration_min} 分钟\n"
    )
    out_path.write_text(md + footer, encoding="utf-8")
    print(f"    → {out_path.relative_to(salon_root())}  ({len(md)} 字)")
    return out_path


def iter_videos(limit: int | None = None) -> list[Path]:
    videos = sorted(
        p
        for p in raw_video_dir().iterdir()
        if p.is_file() and p.suffix.lower() in VIDEO_EXT and not p.name.startswith(".")
    )
    if limit:
        videos = videos[:limit]
    return videos


def process_all(
    *,
    transcribe: bool = True,
    structure: bool = True,
    force: bool = False,
    limit: int | None = None,
) -> int:
    videos = iter_videos(limit)
    if not videos:
        print(f"未找到视频：{raw_video_dir()}")
        print("请把 mp4 放进该目录，文件名以 YYYYMMDD 开头。")
        return 1

    print(f"沙龙语料目录: {salon_root()}")
    print(f"待处理视频: {len(videos)} 个\n")

    ok, failed = 0, 0
    for video in videos:
        try:
            transcript_json = None
            if transcribe:
                transcript_json = transcribe_video(video, force=force)
            elif structure:
                transcript_json = work_dir_for(video) / "transcript.json"
                if not transcript_json.exists():
                    raise FileNotFoundError(
                        f"缺少转写文件 {transcript_json}，请先 --transcribe"
                    )

            if structure and transcript_json:
                structure_transcript(transcript_json, force=force)
            ok += 1
        except (ValueError, MediaError, RuntimeError, FileNotFoundError) as e:
            failed += 1
            print(f"  [失败] {video.name}: {e}")

    print(f"\n完成：成功 {ok}，失败 {failed}")
    if ok and structure:
        print("下一步：python -m knowledge.ingest --corpus pku_salon")
    return 0 if failed == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="教学沙龙视频 → Markdown 语料")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--transcribe", action="store_true", help="只做 Step 1：抽音频 + ASR 转写"
    )
    mode.add_argument(
        "--structure", action="store_true", help="只做 Step 2：LLM 提取教学知识"
    )
    parser.add_argument("--force", action="store_true", help="忽略缓存，强制重跑")
    parser.add_argument("--limit", type=int, help="最多处理 N 个视频（试跑用）")
    args = parser.parse_args()

    transcribe = structure = True
    if args.transcribe:
        transcribe, structure = True, False
    elif args.structure:
        transcribe, structure = False, True

    return process_all(
        transcribe=transcribe,
        structure=structure,
        force=args.force,
        limit=args.limit,
    )


if __name__ == "__main__":
    sys.exit(main())
