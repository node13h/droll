from unittest.mock import MagicMock, patch

import pyotp

from django.test import TestCase

from .. import otp


class OtpFunctionsTestCase(TestCase):
    def test_otp_generate_secret(self):
        self.assertEqual(len(otp.generate_secret()), 16)

    @patch.object(pyotp.TOTP, 'verify')
    def test_otp_verify_success(self, m_verify):
        m_verify.return_value = True
        self.assertTrue(otp.verify('secret', 'code'))
        m_verify.assert_called_with('code')

    @patch.object(pyotp.TOTP, 'verify')
    def test_otp_verify_fail(self, m_verify):
        m_verify.return_value = False
        self.assertFalse(otp.verify('secret', 'code'))
        m_verify.assert_called_with('code')

    def test_set_verified(self):
        request = MagicMock()
        request.session = {}

        with self.settings(OTP_SESSION_FLAG_NAME='otp_verified'):
            otp.set_verified(request)

        self.assertEqual(request.session['otp_verified'], True)

    def test_is_verified_true(self):
        request = MagicMock()
        request.session = {'otp_verified': True}

        with self.settings(OTP_SESSION_FLAG_NAME='otp_verified'):
            self.assertTrue(otp.is_verified(request))

    def test_is_verified_false(self):
        request = MagicMock()
        request.session = {'otp_verified': False}

        with self.settings(OTP_SESSION_FLAG_NAME='otp_verified'):
            self.assertFalse(otp.is_verified(request))

    def test_is_verified_missing_false(self):
        request = MagicMock()
        request.session = {}

        with self.settings(OTP_SESSION_FLAG_NAME='otp_verified'):
            self.assertFalse(otp.is_verified(request))
