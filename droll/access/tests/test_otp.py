# Copyright (C) 2017 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
