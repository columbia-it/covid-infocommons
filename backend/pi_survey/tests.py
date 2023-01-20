from django.test import TestCase
from .email import (
    check_enable_send, 
    check_use_ssl, 
    check_use_gmail_api,
    check_enable_log,
    send_email
)
import os
from unittest.mock import MagicMock, patch


class EmailTestCase(TestCase):
    def setUp(self):
        pass

    def test_check_enable_send_not_defined(self):
        """Environment variable SMTP_DISABLE_SEND is not defined"""
        is_enabled = check_enable_send()
        self.assertTrue(is_enabled)

    def test_check_enable_send_ok(self):
        """Environment variable SMTP_DISABLE_SEND is set to false"""
        os.environ["SMTP_DISABLE_SEND"] = False
        is_enabled = check_enable_send()
        self.assertTrue(is_enabled)

    def test_check_enable_send_not_sending(self):
        """Environment variable SMTP_DISABLE_SEND is set to true"""
        os.environ["SMTP_DISABLE_SEND"] = True
        is_enabled = check_enable_send()
        self.assertFalse(is_enabled)

    def test_check_use_ssl_not_defined(self):
        """Environment variable SMTP_USE_SSL is not defined"""
        use_ssl = check_use_ssl()
        self.assertFalse(use_ssl)

    def test_check_use_ssl_ok(self):
        """Environment variable SMTP_USE_SSL is set to true"""
        os.environ["SMTP_USE_SSL"] = True
        use_ssl = check_use_ssl()
        self.assertTrue(use_ssl)

    def test_check_use_ssl_not_using(self):
        """Environment variable SMTP_USE_SSL is set to false"""
        os.environ["SMTP_USE_SSL"] = True
        use_ssl = check_use_ssl()
        self.assertFalse(use_ssl)

    def test_check_use_gmail_api_not_defined(self):
        """Environment variable SMTP_USE_GMAIL_API is not defined"""
        use_gmail_api = check_use_gmail_api()
        self.assertFalse(use_gmail_api)

    def test_check_use_gmail_api_ok(self):
        """Environment variable SMTP_USE_GMAIL_API is set to true"""
        os.environ["SMTP_USE_GMAIL_API"] = True
        use_gmail_api = check_use_gmail_api()
        self.assertTrue(use_gmail_api)

    def test_check_use_gmail_api_not_using(self):
        """Environment variable SMTP_USE_GMAIL_API is set to false"""
        os.environ["SMTP_USE_GMAIL_API"] = False
        use_gmail_api = check_use_gmail_api()
        self.assertFalse(use_gmail_api)

    def test_check_enable_log_not_defined(self):
        """Environment variable SMTP_ENABLE_LOG is not defined"""
        enable_log = check_enable_log()
        self.assertFalse(enable_log)

    def test_check_enable_log_ok(self):
        """Environment variable SMTP_ENABLE_LOG is set to true"""
        os.environ["SMTP_ENABLE_LOG"] = True
        enable_log = check_enable_log()
        self.assertTrue(enable_log)

    def test_check_enable_log_not_using(self):
        """Environment variable SMTP_ENABLE_LOG is set to false"""
        os.environ["SMTP_ENABLE_LOG"] = False
        enable_log = check_enable_log()
        self.assertFalse(enable_log)

    @patch('backend.pi_survey.email._send_message')
    @patch('backend.pi_survey.email.check_enable_send')
    def test_send_email_disable_send(self, mock_check, mock_send):
        """Email is generated but not sent"""
        mock_check.return_value = False
        from_address = 'a@xyz.com'
        to_addresses = ['b@xyz.com', 'c@xyz.com']
        cc_addresses = []
        bcc_addresses = []
        subject = 'Test Sub'
        body = 'Test Body'
        has_error = send_email(
            from_address, to_addresses, cc_addresses,
            bcc_addresses, subject, body
        )
        mock_send.assert_not_called()
        self.assertEqual(has_error, None)
