"""Real OSS/API/DB smoke in a disposable PostgreSQL container; no AI model run."""
from __future__ import annotations

import asyncio
import io
import hashlib
import json
import os
import uuid
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from urllib.request import urlopen

import httpx
from sqlalchemy import select

from backend.app.models import Base, User, StoredFile, EvalTask, SyllabusTask
from backend.app.core.database import get_sync_engine, session_scope
from backend.app.core.app_settings import get_app_settings
from backend.app.core import db
from backend.app.core.material_storage import resolve_material, object_key, purge_deleted_oss_files
from backend.app.core.storage import get_storage
from backend.app.auth.sessions import create_session
from backend.app.main import app
from backend.app.workers.tasks import run_evaluation


async def check():
    config = get_app_settings()
    if os.getenv("OSS_SMOKE_ISOLATED") != "true" or not config.database_url.endswith("/oss_smoke"):
        raise SystemExit("只允许在显式隔离的 oss_smoke 数据库中运行")
    Base.metadata.create_all(get_sync_engine())
    owner = uuid.uuid4()
    async with session_scope() as session:
        session.add(User(id=owner, display_name="OSS isolated check"))
        await session.flush()
        token = await create_session(session, owner)
    stages = []
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://isolated.invalid",
                                 cookies={config.cookie_name: token}, follow_redirects=False) as client:
        async def new_task():
            response = await client.post("/api/evaluation/tasks", json={"filename": "lesson.mp4"})
            assert response.status_code == 200, "任务创建失败"
            return response.json()["id"]

        async def download(task, payload):
            response = await client.get(f"/api/evaluation/task/{task}/file/video")
            assert response.status_code == 302, "OSS 下载入口未返回授权跳转"
            def read():
                with urlopen(response.headers["location"], timeout=15) as opened:
                    return opened.read(len(payload) + 1)
            assert await asyncio.to_thread(read) == payload, "下载内容不一致"
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://isolated.invalid") as anonymous:
                denied = await anonymous.get(f"/api/evaluation/task/{task}/file/video")
                assert denied.status_code == 401, "匿名下载未拒绝"

        async def process(task, expected, evidence=False):
            submitted = await client.post(f"/api/evaluation/tasks/{task}/submit")
            assert submitted.status_code == 200, "材料提交失败"
            claimed = await db.claim_next_eval_task("isolated-oss-check")
            assert claimed and claimed["id"] == task
            def evaluate(video, *args):
                assert Path(video).read_bytes() == expected
                if evidence:
                    from ai_engine.evaluation.media import load_browser_evidence
                    assert load_browser_evidence(video), "快速材料未恢复完整画面"
                return {"overall": {"score": 80}, "check": "mock-engine"}
            with patch("backend.app.workers.tasks.evaluate_session", side_effect=evaluate), \
                 patch("backend.app.workers.tasks.index_report"):
                await run_evaluation(task, claimed["video_path"], claimed["reference"], claimed["syllabus_path"],
                                     claimed["courseware_path"], claimed["transcript"], claimed["transcript_path"])
            assert (await db.get_task(task))["status"] == "completed", "任务材料恢复失败"
            key = object_key(claimed["video_path"], owner=str(owner), task_id=task)
            assert not get_storage("local").path_for(key).exists(), "解析后未清理本地源文件"

        primary = b"isolated-original-video\n" * 1024
        task = await new_task()
        response = await client.post(f"/api/evaluation/tasks/{task}/materials", files={
            "file": ("lesson.mp4", primary, "video/mp4"),
            "courseware": ("notes.pdf", b"%PDF-test", "application/pdf"),
        })
        assert response.status_code == 200, "原视频材料保存失败"
        await download(task, primary)
        await process(task, primary)
        await download(task, primary)
        stages.append("原视频、课件、授权下载、Worker 恢复和源文件清理")
        info = await client.get(f"/api/evaluation/task/{task}/follow-up")
        assert info.status_code == 200 and info.json()["estimate"]["min_minutes"] > 0
        assert "queue_count" not in info.json()
        absent = await client.post(f"/api/evaluation/task/{task}/email-notification")
        assert absent.status_code == 409, "没有邮箱仍接受发送申请"
        updated = await client.patch("/api/auth/me", json={"email": "smoke@example.org"})
        assert updated.status_code == 200
        requested = await client.post(f"/api/evaluation/task/{task}/email-notification")
        assert requested.status_code == 200 and requested.json()["status"] == "waiting_service"
        from backend.app.core.report_mail import dispatch_reports
        with patch("backend.app.core.report_mail.mail_ready", return_value=True), \
             patch("backend.app.core.report_mail.send_report") as send:
            await dispatch_reports()
            await dispatch_reports()
            send.assert_called_once()
            assert send.call_args.args[0] == "smoke@example.org"
        info = await client.get(f"/api/evaluation/task/{task}/follow-up")
        assert info.json()["notification_status"] == "sent", "发送状态未持久化"
        assert (await client.get("/api/evaluation/task/not-a-uuid/follow-up")).status_code == 404
        stages.append("预计时间、无邮箱拒绝、完善资料、等待邮件配置、模拟发送和发送幂等")

        chunk_task = await new_task()
        response = await client.post(f"/api/evaluation/tasks/{chunk_task}/upload-session", json={
            "mode": "original", "fingerprint": hashlib.sha256(primary).hexdigest(),
            "original_filename": "lesson.mp4", "original_size": len(primary),
        })
        assert response.status_code == 200, "分片会话创建失败"
        session_id = response.json()["session_id"]
        for _ in range(2):
            response = await client.put(f"/api/evaluation/tasks/{chunk_task}/upload-session/parts/video/0",
                                        content=primary, headers={"X-Upload-Session": session_id,
                                        "X-Part-Sha256": hashlib.sha256(primary).hexdigest()})
            assert response.status_code == 200, "分片上传或重复分片失败"
        for _ in range(2):
            response = await client.post(f"/api/evaluation/tasks/{chunk_task}/upload-session/complete",
                                         json={"session_id": session_id})
            assert response.status_code == 200, "分片完成或重复完成失败"
        await download(chunk_task, primary)
        await process(chunk_task, primary)
        stages.append("原视频分片、重复分片与幂等完成、OSS 恢复")

        task_remote = await new_task()
        async def remote(url, **kwargs):
            key = f"{owner}/{task_remote}/{uuid.uuid4().hex}.mp4"
            local = get_storage("local")
            local.save(key, io.BytesIO(primary))
            return SimpleNamespace(path=str(local.path_for(key)), storage_key=key, filename="remote.mp4",
                                   mime_type="video/mp4", size_bytes=len(primary))
        with patch("backend.app.api.evaluation.download_remote_video", side_effect=remote):
            response = await client.post(f"/api/evaluation/tasks/{task_remote}/materials",
                                         data={"video_url": "https://media.example.org/lesson.mp4"})
        assert response.status_code == 200, "网盘落地材料未持久化"
        await download(task_remote, primary)
        await process(task_remote, primary)
        assert (await client.post(f"/api/evaluation/task/{task_remote}/email-notification")).status_code == 200
        with patch("backend.app.core.report_mail.mail_ready", return_value=True), \
             patch("backend.app.core.report_mail.send_report", side_effect=RuntimeError("test-only")) as send:
            await dispatch_reports()
            await dispatch_reports()
            send.assert_called_once()  # second call respects backoff instead of sending again
        info = await client.get(f"/api/evaluation/task/{task_remote}/follow-up")
        assert info.json()["notification_status"] == "pending", "邮件失败后未保留重试状态"
        stages.append("邮件失败退避重试（模拟发送）")
        stages.append("链接导入落地文件转 OSS（下载器模拟）")

        raw = {"version": 1, "original_filename": "lesson.mp4", "original_size": 100,
               "duration_sec": 6, "interval_sec": 3, "audio_codec": "aac",
               "dense_frames": [{"name": f"dense/{i:05d}.jpg", "time_sec": i * 3} for i in range(2)],
               "keyframes": [{"name": f"key/{i:02d}.jpg", "time_sec": .3 + i * .49} for i in range(12)]}
        images = io.BytesIO()
        with zipfile.ZipFile(images, "w") as archive:
            for item in raw["dense_frames"] + raw["keyframes"]:
                archive.writestr(item["name"], b"jpeg-test")
        task_fast = await new_task()
        audio = b"isolated-audio"
        response = await client.post(f"/api/evaluation/tasks/{task_fast}/materials",
                                     data={"evidence_manifest": json.dumps(raw)}, files={
            "evidence_audio": ("audio.m4a", audio, "audio/mp4"),
            "evidence_archive": ("frames.zip", images.getvalue(), "application/zip"),
        })
        assert response.status_code == 200, "快速材料保存失败"
        await process(task_fast, audio, evidence=True)
        stages.append("快速上传音频、画面和清单恢复")

        with patch("backend.app.api.syllabus.run_syllabus_optimization", new=AsyncMock()):
            response = await client.post("/api/syllabus/optimize_file", files={"file": ("outline.txt", b"long outline text", "text/plain")})
        assert response.status_code == 200, "大纲上传失败"
        syllabus_id = response.json()["task_id"]
        async with session_scope() as session:
            source = (await session.get(SyllabusTask, uuid.UUID(syllabus_id))).source_path
        restored = await asyncio.to_thread(resolve_material, source, owner=str(owner), task_id=syllabus_id)
        assert Path(restored).read_bytes() == b"long outline text"
        assert (await client.delete(f"/api/syllabus/task/{syllabus_id}")).status_code == 200
        stages.append("大纲保存、恢复、删除")

        jpeg = b"\xff\xd8jpeg-test\xff\xd9"
        response = await client.post("/api/auth/me/avatar", files={"file": ("avatar.jpg", jpeg, "image/jpeg")})
        assert response.status_code == 200, "头像保存失败"
        response = await client.get("/api/auth/me/avatar")
        assert response.status_code == 200 and response.content == jpeg, "头像读取失败"
        stages.append("头像保存与读取")

        with patch.dict(os.environ, {"UPLOAD_STORAGE_BACKEND": "local"}):
            legacy = await new_task()
            response = await client.post(f"/api/evaluation/tasks/{legacy}/materials", files={"file": ("lesson.mp4", primary, "video/mp4")})
            assert response.status_code == 200
            response = await client.get(f"/api/evaluation/task/{legacy}/file/video")
            assert response.status_code == 200 and response.content == primary
            await download(task, primary)  # new OSS references survive local upload-mode rollback
        stages.append("旧本地文件读取、上传模式回退后 OSS 文件可读")

        for item in (task, chunk_task, task_remote, task_fast, legacy):
            await db.update_task(item, status="cancelled")
            assert (await client.delete(f"/api/evaluation/task/{item}")).status_code == 200
        stages.append("评估任务删除及 OSS 清理")
    print(json.dumps({"business_checks": stages, "engine": "mocked; no ASR/LLM execution"}, ensure_ascii=False), flush=True)
    # Only isolated owners' objects; leave production users and database untouched.
    async with session_scope() as session:
        rows = (await session.scalars(select(StoredFile).where(StoredFile.user_id == owner, StoredFile.storage_backend == "oss"))).all()
        keys = [row.storage_key for row in rows]
    for key in keys:
        await asyncio.to_thread(get_storage("oss").delete, key)
    print("隔离数据库测试材料已清理", flush=True)


async def cleanup():
    config = get_app_settings()
    if os.getenv("OSS_SMOKE_ISOLATED") != "true" or not config.database_url.endswith("/oss_smoke"):
        return
    async with session_scope() as session:
        rows = (await session.scalars(select(StoredFile).where(StoredFile.storage_backend == "oss"))).all()
        keys = [(str(row.user_id), row.storage_key) for row in rows]
    for owner, key in keys:
        if not key.startswith(owner + "/"):
            raise ValueError("隔离对象归属不一致")
        await asyncio.to_thread(get_storage("oss").delete, key)
    print("隔离测试残留对象清理确认完成", flush=True)


async def main():
    try:
        await check()
    finally:
        await cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        detail = str(error) if isinstance(error, AssertionError) else type(error).__name__
        raise SystemExit("隔离业务测试失败：" + detail) from None
