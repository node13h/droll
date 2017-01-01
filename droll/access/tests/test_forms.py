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
from django.core.exceptions import ImproperlyConfigured

from .. import otp
from .. import forms
from .factories import UserFactory


class UserCreationFormTestCase(TestCase):
    def test_class(self):
        form = forms.UserCreationForm()
        self.assertFalse(form.is_valid())


class UserChangeFormTestCase(TestCase):
    def test_class(self):
        form = forms.UserChangeForm()
        self.assertFalse(form.is_valid())


class OtpFormTestCase(TestCase):
    def test_class(self):
        request = MagicMock()
        form = forms.OtpForm(request)
        self.assertFalse(form.is_valid())

    @patch.object(otp, 'verify')
    def test_valid_code(self, m_verify):
        m_verify.return_value = True
        request = MagicMock()
        request.user = UserFactory.build()
        form = forms.OtpForm(request, {'code': '000000'})
        self.assertTrue(form.is_valid())

    @patch.object(otp, 'verify')
    def test_wrong_code(self, m_verify):
        m_verify.return_value = False
        request = MagicMock()
        request.user = UserFactory.build()
        form = forms.OtpForm(request, {'code': '000000'})
        self.assertFalse(form.is_valid())

    @patch.object(otp, 'verify')
    def test_invalid_code(self, m_verify):
        m_verify.return_value = True
        request = MagicMock()
        request.user = UserFactory.build()
        form = forms.OtpForm(request, {'code': '0'})
        self.assertFalse(form.is_valid())

    def test_unauthenticated_fails(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = False
        with self.assertRaises(ImproperlyConfigured):
            forms.OtpForm(request)
