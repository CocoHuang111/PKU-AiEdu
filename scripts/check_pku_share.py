"""Read or temporarily download an authorized public PKU share, without DB/ASR."""
from __future__ import annotations

import argparse
import asyncio
import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from backend.app.core.cloud_drives import inspect_share, parse_source
from backend.app.core.remote_video import download_remote_video
from backend.app.core.storage import LocalStorageBackend


async def check(url: str, download: bool) -> None:
    if parse_source(url).provider != "pku":
        raise ValueError("检查工具仅接受北大网盘公开分享")
    started = time.monotonic()
    info = await inspect_share(url)
    videos = [entry for entry in info["files"] if entry["is_video"]]
    print(json.dumps({"provider": info["provider"], "files": [
        {key: entry[key] for key in ("name", "size", "is_dir", "is_video")}
        for entry in info["files"]], "inspect_seconds": round(time.monotonic() - started, 2)},
        ensure_ascii=False), flush=True)
    if not download:
        return
    if len(videos) != 1:
        raise ValueError("完整下载检查要求根目录恰好有一个视频")
    with tempfile.TemporaryDirectory(prefix="pku-share-check-") as tmp:
        with patch("backend.app.core.remote_video.get_storage",
                   return_value=LocalStorageBackend(Path(tmp))):
            result = await download_remote_video(url, user_id="diagnostic", task_id="public-share",
                                                share_file_id=videos[0]["id"])
        print(json.dumps({"downloaded_bytes": Path(result.path).stat().st_size,
            "duration_seconds": result.duration_sec,
            "total_seconds": round(time.monotonic() - started, 2), "temporary_copy": True},
            ensure_ascii=False), flush=True)
    print("临时下载副本已自动清理；未创建评估任务或运行 ASR。", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    asyncio.run(check(args.url, args.download))
