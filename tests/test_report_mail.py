import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, AsyncMock, patch
import uuid
from fastapi import HTTPException
from backend.app.core.report_mail import mail_ready, estimate_seconds, send_report, unsubscribe, subscribe, notification_states, dispatch_reports, KEY
from backend.app.models import SyllabusTask


class ReportMailTests(unittest.TestCase):
    def test_no_service_or_insecure_configuration_is_not_ready(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(mail_ready())
        env = {"SMTP_HOST": "smtp.example.org", "SMTP_FROM": "service@example.org", "APP_PUBLIC_URL": "https://ask.example.org"}
        with patch.dict(os.environ, env, clear=True):
            self.assertTrue(mail_ready())
            for key, value in [("SMTP_SECURITY", "plain"), ("SMTP_PORT", "oops"), ("APP_PUBLIC_URL", "http://example.org")]:
                with patch.dict(os.environ, {key: value}):
                    self.assertFalse(mail_ready())

    def test_estimate_filters_mock_and_invalid_times_and_includes_wait(self):
        with patch.dict(os.environ, {"EVALUATION_ESTIMATE_SECONDS": "7200"}):
            self.assertEqual(estimate_seconds([None, .1, -4], 0), {"min_minutes": 60, "max_minutes": 180, "preliminary": True})
        result = estimate_seconds([1200, 1800, 2400], 1)
        self.assertEqual(result, {"min_minutes": 30, "max_minutes": 90, "preliminary": False})

    def test_report_is_a_login_required_link_and_tls_is_required(self):
        env = {"SMTP_HOST": "smtp.example.org", "SMTP_FROM": "service@example.org",
               "APP_PUBLIC_URL": "https://ask.example.org", "SMTP_SECURITY": "starttls",
               "SMTP_USERNAME": "user", "SMTP_PASSWORD": "test-only"}
        connection = MagicMock()
        connection.__enter__.return_value = connection
        task = SimpleNamespace(id='test-task', filename='课堂.mp4', result={'report': '# 报告'},
                               created_at=None, transcript=None, transcript_path=None,
                               syllabus_path=None, courseware_path=None)
        with patch.dict(os.environ, env, clear=True), patch("backend.app.core.report_mail.smtplib.SMTP", return_value=connection), patch('backend.app.core.report_mail.render_report_pdf', return_value=(b'%PDF-test', '课堂.pdf')):
            send_report("teacher@example.org", task, '张三', '1234')
        connection.starttls.assert_called_once()
        connection.login.assert_called_once_with("user", "test-only")
        message = connection.send_message.call_args.args[0]
        self.assertEqual(message["To"], "teacher@example.org")
        body = message.get_body(preferencelist=('plain',)).get_content()
        self.assertIn("/#/evaluation?task=test-task", body)
        self.assertIn('尊敬的张三老师（工号1234）：', body)
        self.assertIn('您的课堂.mp4视频评估任务已完成，报告见附件', body)
        attachments = list(message.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_content_type(), 'application/pdf')
        self.assertEqual(attachments[0].get_payload(decode=True), b'%PDF-test')
        with patch.dict(os.environ, env, clear=True), patch("backend.app.core.report_mail.smtplib.SMTP", return_value=connection), patch('backend.app.core.report_mail.render_report_pdf', return_value=(b'%PDF-test', '课堂.pdf')):
            send_report('teacher@example.org', task)
        body = connection.send_message.call_args.args[0].get_body(preferencelist=('plain',)).get_content()
        self.assertIn('尊敬的老师：', body)
        self.assertNotIn('工号', body)

    def test_duration_scaled_estimate_includes_queue(self):
        result = estimate_seconds([1200, 2400], 1, 7200, [3600, 7200])
        self.assertEqual(result, {"min_minutes": 35, "max_minutes": 105, "preliminary": False})


class NotificationToggleTests(unittest.IsolatedAsyncioTestCase):
    async def test_dispatch_syllabus_uses_syllabus_task_and_marks_sent(self):
        uid, tid = uuid.uuid4(), uuid.uuid4()
        row = SimpleNamespace(user_id=uid, settings={KEY: {'syllabus:' + str(tid): {'status': 'pending'}}})
        task = SimpleNamespace(user_id=uid, status='completed')
        profile = SimpleNamespace(email='teacher@example.org', name='李', staff_id='123')
        session = MagicMock()
        records = MagicMock()
        records.all.return_value = [row]
        session.scalars = AsyncMock(return_value=records)
        session.get = AsyncMock(side_effect=[profile, task])
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=session)
        context.__aexit__ = AsyncMock(return_value=False)
        with patch('backend.app.core.report_mail.session_scope', return_value=context), patch('backend.app.core.report_mail.mail_ready', return_value=True), patch('backend.app.core.report_mail.send_report') as send:
            await dispatch_reports()
        send.assert_called_once_with(profile.email, task, '李', '123', 'syllabus')
        self.assertEqual(session.get.call_args.args, (SyllabusTask, tid))
        self.assertEqual(row.settings[KEY]['syllabus:' + str(tid)]['status'], 'sent')

    async def test_syllabus_subscription_is_namespaced_and_can_disable(self):
        uid, tid = uuid.uuid4(), uuid.uuid4()
        row = SimpleNamespace(settings={KEY: {'existing-video': {'status': 'pending'}}})
        task = SimpleNamespace(user_id=uid, status='queued')
        session = MagicMock()
        session.scalar = AsyncMock(side_effect=[None, row, None, row])
        session.get = AsyncMock(side_effect=[task, SimpleNamespace(email='teacher@example.org'), task])
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=session)
        context.__aexit__ = AsyncMock(return_value=False)
        with patch('backend.app.core.report_mail.session_scope', return_value=context), patch('backend.app.core.report_mail.mail_ready', return_value=True):
            result = await subscribe(str(tid), str(uid), 'syllabus')
            self.assertEqual(result['status'], 'pending')
            self.assertEqual(row.settings[KEY]['syllabus:' + str(tid)]['status'], 'pending')
            await unsubscribe(str(tid), str(uid), 'syllabus')
        self.assertEqual(session.get.call_args.args[0], SyllabusTask)
        self.assertEqual(row.settings[KEY]['existing-video']['status'], 'pending')
        self.assertEqual(row.settings[KEY]['syllabus:' + str(tid)]['status'], 'cancelled')

    async def test_disable_persists_and_preserves_other_settings(self):
        uid, tid = uuid.uuid4(), uuid.uuid4()
        row = SimpleNamespace(settings={'other': True, KEY: {str(tid): {'status': 'pending'}}})
        task = SimpleNamespace(user_id=uid, status='processing')
        session = MagicMock()
        session.scalar = AsyncMock(side_effect=[None, row])
        session.get = AsyncMock(return_value=task)
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=session)
        context.__aexit__ = AsyncMock(return_value=False)
        with patch('backend.app.core.report_mail.session_scope', return_value=context):
            result = await unsubscribe(str(tid), str(uid))
        self.assertEqual(result['status'], 'cancelled')
        self.assertTrue(row.settings['other'])
        self.assertEqual(row.settings[KEY][str(tid)]['status'], 'cancelled')

    async def test_disable_rejects_other_owner_and_finished_task(self):
        uid, tid = uuid.uuid4(), uuid.uuid4()
        for task, code in [(SimpleNamespace(user_id=uuid.uuid4(), status='queued'), 404),
                           (SimpleNamespace(user_id=uid, status='completed'), 409)]:
            session = MagicMock()
            session.scalar = AsyncMock(return_value=None)
            session.get = AsyncMock(return_value=task)
            context = MagicMock()
            context.__aenter__ = AsyncMock(return_value=session)
            context.__aexit__ = AsyncMock(return_value=False)
            with patch('backend.app.core.report_mail.session_scope', return_value=context):
                with self.assertRaises(HTTPException) as error:
                    await unsubscribe(str(tid), str(uid))
            self.assertEqual(error.exception.status_code, code)

    def test_syllabus_mail_has_pdf_and_task_link(self):
        env = {'SMTP_HOST': 'smtp.example.org', 'SMTP_FROM': 'service@example.org',
               'APP_PUBLIC_URL': 'https://ask.example.org', 'SMTP_SECURITY': 'ssl'}
        client = MagicMock()
        task = SimpleNamespace(id='test-task', filename='课程大纲.docx',
                               result={'xml': '# 优化大纲', 'course_name': '测试课程'})
        with patch.dict(os.environ, env, clear=True), patch('ai_engine.syllabus.export_syllabus', return_value=(b'%PDF-test', 'application/pdf', '.pdf')), patch('backend.app.core.report_mail.smtplib.SMTP_SSL', return_value=client):
            send_report('teacher@example.org', task, '李', '123', 'syllabus')
        message = client.send_message.call_args.args[0]
        body = message.get_body(preferencelist=('plain',)).get_content()
        self.assertIn('/#/syllabus?task=test-task', body)
        self.assertIn('大纲优化任务已完成', body)
        self.assertEqual(list(message.iter_attachments())[0].get_content_type(), 'application/pdf')


if __name__ == "__main__":
    unittest.main()
