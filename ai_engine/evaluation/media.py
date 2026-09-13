"""ffmpeg 相关：从视频抽音轨、抽关键帧、读时长。"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from ..config import settings


class MediaError(RuntimeError):
    pass


def _run(cmd: list[str], timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    """跑 ffmpeg/ffprobe。stderr 常带容器里的非 UTF-8 元数据（老 QuickTime/GBK），
    不能用 text=True 的默认 utf-8 严格解码，否则抽音在读输出时就崩。"""
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def ensure_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise MediaError(
            "未找到 ffmpeg。macOS 安装：brew install ffmpeg"
        )


def probe_duration(path: str | Path) -> float:
    """用 ffprobe 读时长（秒）。读不到返回 0。"""
    if not shutil.which("ffprobe"):
        return 0.0
    try:
        out = _run(
            [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", str(path),
            ],
            timeout=60,
        )
        return float(json.loads(out.stdout)["format"]["duration"])
    except Exception:
        return 0.0


def extract_audio(video_path: str | Path, out_dir: Path | None = None) -> str:
    """抽成 16kHz 单声道 WAV —— faster-whisper 和 librosa 都吃这个格式。"""
    ensure_ffmpeg()
    video_path = Path(video_path)
    out_dir = out_dir or settings.upload_dir
    out_path = out_dir / f"{video_path.stem}.wav"

    result = _run(
        [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vn", "-ar", "16000", "-ac", "1", "-f", "wav",
            str(out_path),
        ]
    )
    if result.returncode != 0 or not out_path.exists():
        raise MediaError(f"抽取音频失败：{result.stderr[-500:]}")
    return str(out_path)


def extract_keyframes(
    video_path: str | Path, count: int | None = None, duration: float | None = None
) -> list[dict]:
    """在视频时长内均匀取 count 张帧。

    用均匀采样而不是场景切换检测：教学视频机位基本固定，场景检测会几乎不触发，
    而均匀采样能保证覆盖整堂课的各个阶段。
    """
    ensure_ffmpeg()
    video_path = Path(video_path)
    count = count or settings.section("evaluation").get("keyframe_count", 12)
    duration = duration or probe_duration(video_path)

    if duration <= 0:
        raise MediaError("无法读取视频时长，文件可能已损坏")

    frame_dir = settings.frame_dir / video_path.stem
    frame_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    for i in range(count):
        # 首尾各留 5%，避免抽到片头黑屏和片尾定格
        ratio = 0.05 + (0.90 * i / max(count - 1, 1))
        timestamp = duration * ratio
        out_path = frame_dir / f"frame_{i:02d}.jpg"

        result = _run(
            [
                "ffmpeg", "-y", "-ss", f"{timestamp:.2f}", "-i", str(video_path),
                "-frames:v", "1", "-q:v", "3",
                "-vf", "scale='min(1280,iw)':-2",
                str(out_path),
            ]
        )
        if result.returncode == 0 and out_path.exists():
            frames.append(
                {
                    "index": i,
                    "path": str(out_path),
                    "time_sec": round(timestamp, 1),
                    "timestamp": _fmt_time(timestamp),
                }
            )

    if not frames:
        raise MediaError("关键帧抽取失败，未能生成任何图片")
    return frames


def load_browser_evidence(media_path: str | Path) -> dict | None:
    """读取上传接口生成的浏览器证据清单；普通视频没有该文件。"""
    media_path = Path(media_path)
    manifest_path = media_path.parent / "browser-evidence.json"
    if not manifest_path.is_file():
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        duration = float(manifest["duration_sec"])
        interval = float(manifest["interval_sec"])
        dense = list(manifest["dense_frames"])
        keyframes = list(manifest["keyframes"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise MediaError("浏览器证据清单已损坏") from exc
    if duration <= 0 or interval <= 0 or len(dense) < 2 or not keyframes:
        raise MediaError("浏览器证据清单不完整")
    paths = [Path(item.get("path", "")).resolve() for item in dense + keyframes]
    frame_root = settings.frame_dir.resolve()
    if any(not path.is_relative_to(frame_root) or not path.is_file() for path in paths):
        raise MediaError("浏览器证据画面缺失")
    return manifest


def cleanup_video_artifacts(video_path: str | Path) -> None:
    """删掉本条抽音和关键帧/课件渲染页。原始视频不动。数据集 extract 用完即调。"""
    video_path = Path(video_path)
    wav = settings.upload_dir / f"{video_path.stem}.wav"
    if wav.exists():
        wav.unlink(missing_ok=True)
    frame_dir = settings.frame_dir / video_path.stem
    if frame_dir.exists():
        shutil.rmtree(frame_dir, ignore_errors=True)


def iter_gray_frames(
    video_path: str | Path,
    interval_sec: float = 3.0,
    width: int = 160,
    height: int = 90,
):
    """按固定间隔抽灰度缩略帧，逐帧 yield shape (height, width) 的 uint8 数组。

    这是「密集轨」：只用于本地帧差比对，不送 VLM，所以尺寸压到 160×90，
    走管道读、不落盘。与 extract_keyframes 的「稀疏轨」分开是因为两者成本结构
    完全不同 —— 稀疏轨每帧都要花一次 VLM 调用，密集轨几乎零成本。

    流式 yield 而非一次性返回整个数组：调用方只需要相邻两帧做差，
    没必要把整段视频的帧堆在内存里。这样即使把 interval_sec 调到亚秒级、
    或处理数小时的录像，内存占用也是常数。
    """
    ensure_ffmpeg()
    try:
        import numpy as np
    except ImportError as e:
        raise MediaError("未安装 numpy") from e

    fps = 1.0 / max(interval_sec, 0.1)
    frame_bytes = width * height
    proc = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-i", str(video_path),
            "-vf", f"fps={fps:.6f},scale={width}:{height},format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "-",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    count = 0
    try:
        while chunk := proc.stdout.read(frame_bytes):
            if len(chunk) < frame_bytes:
                break  # 末尾不完整的帧直接丢掉
            count += 1
            yield np.frombuffer(chunk, dtype=np.uint8).reshape(height, width)
    finally:
        # 调用方提前退出时别把 ffmpeg 留成僵尸进程
        if proc.poll() is None:
            proc.kill()
        stderr = proc.stderr.read()
        proc.stdout.close()
        proc.stderr.close()
        proc.wait()

    if count < 2:
        raise MediaError(
            f"密集抽帧失败或帧数不足（得到 {count} 帧）："
            f"{stderr.decode('utf-8', 'ignore')[-300:]}"
        )


def iter_gray_image_files(
    paths: list[str | Path], width: int = 160, height: int = 90
):
    """读取浏览器已抽取的图片，转为与视频密集轨相同的灰度数组。"""
    try:
        import numpy as np
        from PIL import Image
    except ImportError as exc:
        raise MediaError("未安装浏览器证据画面解码依赖") from exc

    count = 0
    for raw_path in paths:
        path = Path(raw_path)
        try:
            with Image.open(path) as image:
                frame = np.asarray(
                    image.convert("L").resize((width, height)), dtype=np.uint8
                ).copy()
        except Exception as exc:
            raise MediaError(f"无法读取浏览器证据画面：{path.name}") from exc
        count += 1
        yield frame
    if count < 2:
        raise MediaError(f"浏览器证据画面不足（得到 {count} 帧）")


def _fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
