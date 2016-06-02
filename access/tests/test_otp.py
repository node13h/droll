from unittest import TestCase
from unittest.mock import patch

import pyotp

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
