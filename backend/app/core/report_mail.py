"""Opt-in report links and retryable SMTP delivery. No credentials or URLs in logs."""
from __future__ import annotations

import asyncio
import os
import smtplib
import ssl
import statistics
import subprocess
import uuid
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import HTTPException
from sqlalchemy import select
from .database import session_scope
from ..models import EvalTask, User, UserProfile, UserSettings
from .report_export import render_report_pdf

KEY = "eval_report_mail"


def mail_ready():
    try:
        url = urlsplit(os.getenv("APP_PUBLIC_URL", ""))
        port_valid = 1 <= int(os.getenv("SMTP_PORT", "587")) <= 65535
    except ValueError:
        return False
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_FROM") and
                url.scheme == "https" and url.netloc and not url.username and not url.password and
                os.getenv("SMTP_SECURITY", "starttls") in {"ssl", "starttls"} and port_valid and
                (not os.getenv("SMTP_USERNAME") or bool(os.getenv("SMTP_PASSWORD"))))


def estimate_seconds(samples, tasks_ahead, duration=None, historical_durations=None):
    valid = [float(n) for n in samples if isinstance(n, (int, float)) and 60 <= n <= 86400]
    try:
        fallback = min(86400, max(300, int(os.getenv("EVALUATION_ESTIMATE_SECONDS", "7200"))))
    except ValueError:
        fallback = 7200
    typical = statistics.median(valid) if valid else fallback
    rates = [float(s) / float(d) for s, d in zip(samples, historical_durations or [])
             if isinstance(s, (int, float)) and 60 <= s <= 86400
             and isinstance(d, (int, float)) and 0 < d <= 86400]
    own = max(60, statistics.median(rates) * duration) if rates and duration else typical
    total = typical * tasks_ahead + own
    return {"min_minutes": max(1, round(total * .5 / 60)),
            "max_minutes": max(2, round(total * 1.5 / 60)),
            "preliminary": not bool(valid)}


def local_video_duration(path):
    # Never download an OSS source just to estimate, nor run ASR on this endpoint.
    if not path or '://' in path or not Path(path).is_file():
        return None
    try:
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                'format=duration', '-of', 'default=nw=1:nk=1', path],
                               capture_output=True, text=True, timeout=5, check=True)
        value = float(probe.stdout.strip())
        return value if 0 < value <= 86400 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


async def follow_up(task_id, owner):
    async with session_scope() as session:
        task = await session.get(EvalTask, uuid.UUID(task_id))
        if task is None or task.user_id != uuid.UUID(owner):
            raise HTTPException(404, "任务不存在")
        profile = await session.get(UserProfile, task.user_id)
        preferences = await session.get(UserSettings, task.user_id)
        notification = ((preferences.settings or {}).get(KEY, {}).get(task_id, {})
                        if preferences else {})
        return {"status": task.status,
                "has_email": bool(profile and profile.email.strip()), "mail_ready": mail_ready(),
                "notification_status": notification.get("status", "")}


async def subscribe(task_id, owner):
    uid = uuid.UUID(owner)
    async with session_scope() as session:
        # Serialize first-time settings creation and JSON updates for this user.
        await session.scalar(select(User).where(User.id == uid).with_for_update())
        task = await session.get(EvalTask, uuid.UUID(task_id))
        if task is None or task.user_id != uid:
            raise HTTPException(404, "任务不存在")
        if task.status in {"failed", "cancelled", "upload_failed"}:
            raise HTTPException(409, "该任务未完成评估，不能发送报告")
        profile = await session.get(UserProfile, uid)
        if not profile or not profile.email.strip():
            raise HTTPException(409, "请先完善个人资料中的邮箱")
        row = await session.scalar(select(UserSettings).where(UserSettings.user_id == uid).with_for_update())
        if row is None:
            row = UserSettings(user_id=uid, settings={})
            session.add(row)
        values = dict(row.settings or {})
        requests = dict(values.get(KEY) or {})
        existing = requests.get(task_id, {})
        if existing.get("status") == "sent":
            return {"status": "sent"}
        # Keep pending requests, cap terminal history to avoid unlimited profile JSON growth.
        requests = {k: v for k, v in requests.items() if v.get("status") not in {"sent", "cancelled"}}
        if len(requests) >= 100 and task_id not in requests:
            raise HTTPException(409, "待发送通知过多，请稍后重试")
        state = "pending" if mail_ready() else "waiting_service"
        requests[task_id] = {"status": state, "attempts": 0, "requested_at": datetime.now(timezone.utc).isoformat()}
        values[KEY] = requests
        row.settings = values
        row.updated_at = datetime.now(timezone.utc)
        return {"status": state}


async def notification_states(owner):
    async with session_scope() as session:
        row = await session.get(UserSettings, uuid.UUID(owner))
        return (row.settings or {}).get(KEY, {}) if row else {}


async def unsubscribe(task_id, owner):
    uid = uuid.UUID(owner)
    async with session_scope() as session:
        await session.scalar(select(User).where(User.id == uid).with_for_update())
        row = await session.scalar(select(UserSettings).where(UserSettings.user_id == uid).with_for_update())
        task = await session.get(EvalTask, uuid.UUID(task_id))
        if task is None or task.user_id != uid:
            raise HTTPException(404, "任务不存在")
        if task.status not in {'queued', 'processing', 'uploading'}:
            raise HTTPException(409, "仅未完成的任务可以修改邮件通知")
        if row:
            values = dict(row.settings or {})
            requests = dict(values.get(KEY) or {})
            requests[task_id] = {"status": "cancelled"}
            values[KEY] = requests
            row.settings = values
            row.updated_at = datetime.now(timezone.utc)
        return {"status": "cancelled"}


def send_report(email, task, name='', staff_id=''):
    # Generate the same PDF as the download endpoint before contacting SMTP.
    payload = {'filename': task.filename, 'result': task.result,
               'created_at': task.created_at.timestamp() if task.created_at else None,
               'has_script': bool(task.transcript or task.transcript_path),
               'has_syllabus': bool(task.syllabus_path), 'has_courseware': bool(task.courseware_path)}
    pdf, filename = render_report_pdf(payload)
    message = EmailMessage()
    message["From"] = os.environ["SMTP_FROM"]
    message["To"] = email
    message["Subject"] = "北大问教：视频评估报告已完成"
    message["Message-ID"] = f"<askedu-report-{task.id}@{urlsplit(os.environ['APP_PUBLIC_URL']).hostname}>"
    link = os.environ["APP_PUBLIC_URL"].rstrip("/") + f"/#/evaluation?task={task.id}"
    salutation = f"尊敬的{name.strip()}老师" + (f"（工号{staff_id.strip()}）" if staff_id.strip() else '') + '：'
    message.set_content(
        f"{salutation}\n\n您的{task.filename or '教学视频'}视频评估任务已完成，报告见附件；"
        f"更多详细解析请登录{link}（报告链接需登录本人账号访问）。\n\n"
        "感谢您的耐心等待和对北大问教系统的支持！如使用过程中存在不便体验或相关问题，"
        "欢迎随时邮件beidawenjiao@163.com，非常感谢您的宝贵意见！")
    message.add_attachment(pdf, maintype='application', subtype='pdf', filename=filename)
    security = os.getenv("SMTP_SECURITY", "starttls")
    port = int(os.getenv("SMTP_PORT", "465" if security == "ssl" else "587"))
    context = ssl.create_default_context()
    if security == "ssl":
        client = smtplib.SMTP_SSL(os.environ["SMTP_HOST"], port, timeout=15, context=context)
    elif security == "starttls":
        client = smtplib.SMTP(os.environ["SMTP_HOST"], port, timeout=15)
    else:
        raise ValueError("SMTP 必须使用 TLS")
    with client:
        if security == "starttls":
            client.ehlo()
            client.starttls(context=context)
            client.ehlo()
        if os.getenv("SMTP_USERNAME"):
            client.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        client.send_message(message)


async def dispatch_reports():
    if not mail_ready():
        return
    async with session_scope() as session:
        rows = (await session.scalars(select(UserSettings).where(UserSettings.settings.has_key(KEY))
                                     .order_by(UserSettings.updated_at).with_for_update(skip_locked=True).limit(20))).all()
        for row in rows:
            values = dict(row.settings or {})
            requests = {k: dict(v) for k, v in (values.get(KEY) or {}).items()}
            profile = await session.get(UserProfile, row.user_id)
            for task_id, item in requests.items():
                if item.get("status") not in {"pending", "waiting_service", "needs_email"}:
                    continue
                now = datetime.now(timezone.utc)
                if item.get("retry_at") and datetime.fromisoformat(item["retry_at"]) > now:
                    continue
                task = await session.get(EvalTask, uuid.UUID(task_id))
                if task is None or task.user_id != row.user_id or task.status in {"failed", "cancelled", "upload_failed"}:
                    item["status"] = "cancelled"
                    continue
                if task.status != "completed":
                    continue
                if not profile or not profile.email.strip():
                    item["status"] = "needs_email"
                    continue
                try:
                    await asyncio.to_thread(send_report, profile.email, task, profile.name or '', profile.staff_id or '')
                except Exception:
                    attempts = item.get("attempts", 0) + 1
                    item.update(attempts=attempts, status="failed" if attempts >= 5 else "pending",
                                retry_at=(now + timedelta(minutes=2 ** attempts)).isoformat())
                    print("[mail] 报告通知发送失败，将按重试策略处理", flush=True)
                else:
                    item.update(status="sent", sent_at=now.isoformat())
            values[KEY] = requests
            row.settings = values
            row.updated_at = datetime.now(timezone.utc)
