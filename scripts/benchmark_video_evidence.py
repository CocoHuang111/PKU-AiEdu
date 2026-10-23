"""Benchmark a compact evidence package for long-video evaluation.

This is a local-only prototype. It does not call the upload API or any model.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path


def run(command: list[str]) -> float:
    started = time.perf_counter()
    subprocess.run(command, check=True)
    return time.perf_counter() - started


def probe(video: Path) -> dict:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,sample_rate,channels",
            "-of",
            "json",
            str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def tree_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def copied_audio_path(output: Path, metadata: dict) -> Path:
    audio_stream = next(
        (
            stream
            for stream in metadata.get("streams", [])
            if stream.get("codec_type") == "audio"
        ),
        {},
    )
    extension = {
        "aac": "m4a",
        "alac": "m4a",
        "mp3": "mp3",
        "opus": "webm",
        "vorbis": "webm",
        "flac": "flac",
        "pcm_s16le": "wav",
        "pcm_s24le": "wav",
    }.get(audio_stream.get("codec_name"), "mka")
    return output / f"audio-original.{extension}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--keyframes", type=int, default=12)
    parser.add_argument("--audio-kbps", type=int, default=48)
    args = parser.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required")
    if not args.video.is_file():
        raise SystemExit(f"video not found: {args.video}")
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory must be empty: {args.output}")

    args.output.mkdir(parents=True, exist_ok=True)
    dense_dir = args.output / "dense_frames"
    keyframe_dir = args.output / "keyframes"
    dense_dir.mkdir()
    keyframe_dir.mkdir()

    metadata = probe(args.video)
    duration = float(metadata["format"]["duration"])
    source_size = int(metadata["format"]["size"])
    original_audio = copied_audio_path(args.output, metadata)

    timings: dict[str, float] = {}
    timings["audio_copy_sec"] = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(args.video),
            "-map",
            "0:a:0",
            "-vn",
            "-c:a",
            "copy",
            str(original_audio),
        ]
    )
    timings["audio_compact_sec"] = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(args.video),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "libopus",
            "-b:a",
            f"{args.audio_kbps}k",
            str(args.output / "audio-compact.opus"),
        ]
    )
    timings["visual_frames_sec"] = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(args.video),
            "-filter_complex",
            (
                "[0:v:0]split=2[dense][key];"
                f"[dense]fps=1/{args.interval},scale=160:90,format=gray[dense_out];"
                f"[key]fps={args.keyframes}/{duration},"
                "scale='min(1280,iw)':-2[key_out]"
            ),
            "-map",
            "[dense_out]",
            "-q:v",
            "5",
            str(dense_dir / "frame-%05d.jpg"),
            "-map",
            "[key_out]",
            "-q:v",
            "3",
            str(keyframe_dir / "frame-%02d.jpg"),
        ]
    )

    compact_audio = args.output / "audio-compact.opus"
    visual_size = tree_size(dense_dir) + tree_size(keyframe_dir)
    report = {
        "source": {
            "path": str(args.video),
            "duration_sec": duration,
            "size_bytes": source_size,
            "metadata": metadata,
        },
        "outputs": {
            "original_audio_bytes": original_audio.stat().st_size,
            "compact_audio_bytes": compact_audio.stat().st_size,
            "dense_frames_bytes": tree_size(dense_dir),
            "dense_frame_count": len(list(dense_dir.glob("*.jpg"))),
            "keyframes_bytes": tree_size(keyframe_dir),
            "keyframe_count": len(list(keyframe_dir.glob("*.jpg"))),
            "compact_package_bytes": compact_audio.stat().st_size + visual_size,
            "copy_audio_package_bytes": original_audio.stat().st_size + visual_size,
        },
        "timings": {key: round(value, 3) for key, value in timings.items()},
    }
    report["ratios"] = {
        "compact_package_percent": round(
            report["outputs"]["compact_package_bytes"] / source_size * 100, 3
        ),
        "copy_audio_package_percent": round(
            report["outputs"]["copy_audio_package_bytes"] / source_size * 100, 3
        ),
    }
    report_path = args.output / "benchmark.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
