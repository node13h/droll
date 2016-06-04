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
