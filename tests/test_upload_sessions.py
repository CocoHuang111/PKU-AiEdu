from __future__ import annotations

import asyncio
import hashlib
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from fastapi import HTTPException

from backend.app.core.upload_sessions import (
    complete_session,
    create_session,
    save_part,
    session_status,
)
from backend.app.core.app_settings import get_app_settings
from ai_engine.config import settings


async def _chunks(data: bytes, width: int = 3):
    for offset in range(0, len(data), width):
        yield data[offset : offset + width]


class UploadSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.previous_root = os.environ.get("UPLOAD_ROOT")
        os.environ["UPLOAD_ROOT"] = self.temp.name
        get_app_settings.cache_clear()
        self.previous_settings_root = settings.root
        settings.root = Path(self.temp.name)
        self.user_id = "11111111-1111-1111-1111-111111111111"
        self.task_id = "22222222-2222-2222-2222-222222222222"
        self.payload = b"a resumable classroom video"
        self.fingerprint = hashlib.sha256(b"fingerprint").hexdigest()

    def tearDown(self) -> None:
        if self.previous_root is None:
            os.environ.pop("UPLOAD_ROOT", None)
        else:
            os.environ["UPLOAD_ROOT"] = self.previous_root
        settings.root = self.previous_settings_root
        get_app_settings.cache_clear()
        self.temp.cleanup()

    def _create(self) -> dict:
        return create_session(
            self.user_id,
            self.task_id,
            mode="original",
            fingerprint=self.fingerprint,
            original_filename="lesson.mp4",
            original_size=len(self.payload),
        )

    def test_original_upload_is_resumable_and_assembled(self) -> None:
        session = self._create()
        digest = hashlib.sha256(self.payload).hexdigest()
        first = asyncio.run(
            save_part(
                self.user_id,
                self.task_id,
                kind="video",
                index=0,
                session_token=session["session_id"],
                expected_sha256=digest,
                chunks=_chunks(self.payload),
            )
        )
        self.assertFalse(first["duplicate"])

        resumed = self._create()
        self.assertEqual(resumed["received"]["video"][0]["index"], 0)
        duplicate = asyncio.run(
            save_part(
                self.user_id,
                self.task_id,
                kind="video",
                index=0,
                session_token=session["session_id"],
                expected_sha256=digest,
                chunks=_chunks(self.payload),
            )
        )
        self.assertTrue(duplicate["duplicate"])

        result = complete_session(
            self.user_id,
            self.task_id,
            session_token=session["session_id"],
        )
        self.assertEqual(Path(result["path"]).read_bytes(), self.payload)
        self.assertEqual(result["original_filename"], "lesson.mp4")

    def test_bad_part_hash_is_not_committed(self) -> None:
        session = self._create()
        with self.assertRaises(HTTPException):
            asyncio.run(
                save_part(
                    self.user_id,
                    self.task_id,
                    kind="video",
                    index=0,
                    session_token=session["session_id"],
                    expected_sha256="0" * 64,
                    chunks=_chunks(self.payload),
                )
            )
        self.assertEqual(session_status(self.user_id, self.task_id)["received"]["video"], [])

    def test_different_file_cannot_reuse_session(self) -> None:
        self._create()
        with self.assertRaises(HTTPException):
            create_session(
                self.user_id,
                self.task_id,
                mode="original",
                fingerprint="f" * 64,
                original_filename="lesson.mp4",
                original_size=len(self.payload),
            )

    def test_evidence_batches_are_combined_and_extracted(self) -> None:
        manifest = {
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
        session = create_session(
            self.user_id,
            self.task_id,
            mode="evidence",
            fingerprint=self.fingerprint,
            original_filename="lesson.mp4",
            original_size=manifest["original_size"],
            audio_filename="lesson.audio.m4a",
            audio_mime="audio/mp4",
        )
        audio = b"fragmented audio bytes"
        names = [item["name"] for item in manifest["dense_frames"] + manifest["keyframes"]]
        archives = []
        for group in (names[:7], names[7:]):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as bundle:
                for name in group:
                    bundle.writestr(name, b"\xff\xd8evidence\xff\xd9")
            archives.append(buffer.getvalue())

        values = [("audio", 0, audio), ("frames", 0, archives[0]), ("frames", 1, archives[1])]
        for kind, index, value in values:
            asyncio.run(
                save_part(
                    self.user_id,
                    self.task_id,
                    kind=kind,
                    index=index,
                    session_token=session["session_id"],
                    expected_sha256=hashlib.sha256(value).hexdigest(),
                    chunks=_chunks(value),
                )
            )
        result = complete_session(
            self.user_id,
            self.task_id,
            session_token=session["session_id"],
            audio_parts=1,
            frame_parts=2,
            raw_manifest=manifest,
        )
        self.assertEqual(Path(result["path"]).read_bytes(), audio)
        saved_manifest = json.loads(
            (Path(result["path"]).parent / "browser-evidence.json").read_text()
        )
        self.assertEqual(len(saved_manifest["dense_frames"]), 2)
        self.assertEqual(len(saved_manifest["keyframes"]), 12)
        self.assertTrue(
            all(
                Path(item["path"]).is_file()
                for group in ("dense_frames", "keyframes")
                for item in saved_manifest[group]
            )
        )


if __name__ == "__main__":
    unittest.main()
