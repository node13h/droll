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

from django.test import TestCase
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import REDIRECT_FIELD_NAME

from .. import decorators
from .. import otp
from droll.core.tests.utils import dummy_view


class DecoratorsTestCase(TestCase):
    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_pass_unauthenticated(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = False
        request.user.two_fa_enabled = True
        m_is_verified.return_value = False

        decorated_view = decorators.verified_otp_required(
            pass_unauthenticated=True)(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_unauthenticated_raises_by_default(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = False
        request.user.two_fa_enabled = True
        m_is_verified.return_value = False

        decorated_view = decorators.verified_otp_required()(dummy_view)

        with self.assertRaises(ImproperlyConfigured):
            decorated_view(request)

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_pass_verified(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        m_is_verified.return_value = True

        decorated_view = decorators.verified_otp_required()(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_pass_two_fa_disabled(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = False
        m_is_verified.return_value = False

        decorated_view = decorators.verified_otp_required()(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_redirect_not_verified(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        m_is_verified.return_value = False
        request.build_absolute_uri.return_value = 'http://localhost/'
        request.get_full_path.return_value = '/?key=value'

        decorated_view = decorators.verified_otp_required(
            verify_url='/otp/verify', redirect_field_name='go')(dummy_view)
        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], '/otp/verify?go=/%3Fkey%3Dvalue')

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_default_verify_url(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        m_is_verified.return_value = False
        request.build_absolute_uri.return_value = 'http://localhost/'
        request.get_full_path.return_value = '/?key=value'

        with self.settings(OTP_VERIFY_URL='/otp_verify'):
            decorated_view = decorators.verified_otp_required(
                redirect_field_name='go')(dummy_view)

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], '/otp_verify?go=/%3Fkey%3Dvalue')

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_default_redirect_field_name(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        m_is_verified.return_value = False
        request.build_absolute_uri.return_value = 'http://localhost/'
        request.get_full_path.return_value = '/?key=value'

        decorated_view = decorators.verified_otp_required(
            verify_url='/otp/verify')(dummy_view)

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(
            response['Location'],
            '/otp/verify?{}=/%3Fkey%3Dvalue'.format(REDIRECT_FIELD_NAME))

    @patch.object(otp, 'is_verified')
    def test_verified_otp_required_view_as_an_argument(self, m_is_verified):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        m_is_verified.return_value = True

        decorated_view = decorators.verified_otp_required((dummy_view))

        self.assertEqual(decorated_view(request), 'SIGNATURE')
