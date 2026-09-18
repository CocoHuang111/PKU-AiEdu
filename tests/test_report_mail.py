import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from backend.app.core.report_mail import mail_ready, estimate_seconds, send_report


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


if __name__ == "__main__":
    unittest.main()
