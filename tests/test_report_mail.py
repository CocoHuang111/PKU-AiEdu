import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, AsyncMock, patch
import uuid
from fastapi import HTTPException
from backend.app.core.report_mail import mail_ready, estimate_seconds, send_report, unsubscribe, notification_states, KEY


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
        with patch.dict(os.environ, env, clear=True), patch("backend.app.core.report_mail.smtplib.SMTP", return_value=connection):
            send_report("teacher@example.org", SimpleNamespace(id="test-task"))
        connection.starttls.assert_called_once()
        connection.login.assert_called_once_with("user", "test-only")
        message = connection.send_message.call_args.args[0]
        self.assertEqual(message["To"], "teacher@example.org")
        self.assertIn("/#/evaluation?task=test-task", message.get_content())
        self.assertEqual(len(list(message.iter_attachments())), 0)

    def test_duration_scaled_estimate_includes_queue(self):
        result = estimate_seconds([1200, 2400], 1, 7200, [3600, 7200])
        self.assertEqual(result, {"min_minutes": 35, "max_minutes": 105, "preliminary": False})


class NotificationToggleTests(unittest.IsolatedAsyncioTestCase):
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


if __name__ == "__main__":
    unittest.main()
