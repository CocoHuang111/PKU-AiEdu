"""Queue an identifiable copy of an existing upload through the real worker.

No re-upload, no modification of the source task. Restarting this observer only
resumes observation of its manifest, never creates a duplicate task.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
import uuid
from pathlib import Path

from ai_engine import checkpoints
from ai_engine.config import settings
from backend.app.core import db


async def main(source_id: str, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    manifest = checkpoints.read(manifest_path, source_id)
    if manifest is None:
        async with db.session_scope() as session:
            row = await session.get(db.EvalTask, uuid.UUID(source_id))
            if not row or not row.video_path:
                raise RuntimeError("源视频任务不存在")
            source = {"video_path": row.video_path, "filename": row.filename, "user_id": str(row.user_id)}
        original = Path(source["video_path"])
        task_id = str(uuid.uuid4())
        directory = settings.upload_dir / source["user_id"] / task_id
        directory.mkdir(parents=True, exist_ok=False)
        video = directory / f"{uuid.uuid4().hex}{original.suffix}"
        os.link(original, video)
        # Keep a failed observer restart from creating a second queued test.
        manifest = {
            "task_id": task_id, "source_task": source_id,
            "video_path": str(video), "bytes": video.stat().st_size,
            "filename": source["filename"], "started_at": time.time(),
            "user_id": source["user_id"],
        }
        checkpoints.write(manifest_path, source_id, manifest)
    if await db.get_task(manifest["task_id"]) is None:
        await db.create_task(
            filename=f"[分块优化测试] {manifest['filename']}",
            video_path=manifest["video_path"], user_id=manifest["user_id"],
            task_id=manifest["task_id"],
        )
    print(json.dumps(manifest, ensure_ascii=False), flush=True)
    last = None
    with (output / "events.jsonl").open("a", encoding="utf-8") as stream:
        while True:
            task = await db.get_task(manifest["task_id"])
            if task is None:
                raise RuntimeError("测试任务已被删除，停止观察")
            state = {k: task.get(k) for k in ("status", "progress", "current_step", "step_detail", "attempt_count", "error")}
            if state != last:
                event = {"time": time.time(), "elapsed_sec": round(time.time() - manifest["started_at"], 2), **state}
                line = json.dumps(event, ensure_ascii=False)
                stream.write(line + "\n")
                stream.flush()
                print(line, flush=True)
                last = state
            if task["status"] in ("completed", "failed", "cancelled"):
                result = task.get("result") or {}
                transcript = result.get("transcript") or {}
                summary = {
                    **manifest, "status": task["status"], "error": task.get("error"),
                    "elapsed_sec": round(time.time() - manifest["started_at"], 2),
                    "attempt_count": task["attempt_count"],
                    "duration_sec": transcript.get("duration_sec"),
                    "transcript_chars": len(transcript.get("full_text", "")),
                    "transcript_segments": len(transcript.get("segments", [])),
                    "keyframes": len(result.get("keyframes", [])),
                    "dimensions": len(result.get("dimensions", [])),
                    "report_chars": len(result.get("report", "")),
                    "audio": (result.get("raw_features") or {}).get("audio"),
                    "overall": result.get("overall"),
                }
                checkpoints.write(output / "summary.json", source_id, summary)
                print(json.dumps(summary, ensure_ascii=False), flush=True)
                return
            await asyncio.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_task")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    asyncio.run(main(args.source_task, args.output))
