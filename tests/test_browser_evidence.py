from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from fastapi import HTTPException

from backend.app.core.browser_evidence import _extract_archive, parse_manifest


def _jpeg(color: int) -> bytes:
    # 上传层只负责压缩包结构和大小；图片能否解码由 Worker 的 Pillow 再验证。
    return b"\xff\xd8" + bytes([color]) * 16 + b"\xff\xd9"


def _manifest() -> dict:
    return {
        "version": 1,
        "original_filename": "lesson.mp4",
        "original_size": 10_000_000,
        "duration_sec": 6,
        "interval_sec": 3,
        "audio_codec": "aac",
        "dense_frames": [
            {"name": "dense/00000.jpg", "time_sec": 0},
            {"name": "dense/00001.jpg", "time_sec": 3},
        ],
        "keyframes": [
            {"name": f"key/{index:02d}.jpg", "time_sec": 0.3 + index * 0.49}
            for index in range(12)
        ],
    }


class BrowserEvidenceTests(unittest.TestCase):
    def test_manifest_and_archive_are_mapped_to_server_paths(self) -> None:
        manifest = parse_manifest(json.dumps(_manifest()))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "evidence.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                for name in manifest["expected_names"]:
                    bundle.writestr(name, _jpeg(128))
            frame_root = root / "frames"
            _extract_archive(str(archive), frame_root, manifest)

            self.assertNotIn("expected_names", manifest)
            self.assertEqual(len(manifest["dense_frames"]), 2)
            self.assertEqual(len(manifest["keyframes"]), 12)
            self.assertTrue(Path(manifest["dense_frames"][0]["path"]).is_file())

    def test_manifest_rejects_missing_dense_frame(self) -> None:
        manifest = _manifest()
        manifest["dense_frames"].pop()
        with self.assertRaises(HTTPException):
            parse_manifest(json.dumps(manifest))

    def test_archive_rejects_unlisted_file(self) -> None:
        manifest = parse_manifest(json.dumps(_manifest()))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "evidence.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                for name in manifest["expected_names"]:
                    bundle.writestr(name, _jpeg(128))
                bundle.writestr("../unexpected.jpg", _jpeg(0))
            with self.assertRaises(HTTPException):
                _extract_archive(str(archive), root / "frames", manifest)


if __name__ == "__main__":
    unittest.main()
