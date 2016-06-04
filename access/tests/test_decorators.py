from unittest.mock import MagicMock

from django.test import TestCase
from django.http import HttpResponseRedirect

from .. import decorators


def dummy_view(request):
    return 'SIGNATURE'


class DecoratorsTestCase(TestCase):
    def test_otp_required_pass_unauthenticated(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = False
        request.user.two_fa_enabled = True
        request.user.otp_verified = False

        decorated_view = decorators.otp_required()(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    def test_otp_required_pass_verified(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verified = True

        decorated_view = decorators.otp_required()(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    def test_otp_required_pass_two_fa_disabled(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = False
        request.user.otp_verified = False

        decorated_view = decorators.otp_required()(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')

    def test_otp_required_pass_not_verified(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verified = False
        request.build_absolute_uri.return_value = 'http://localhost/'
        request.get_full_path.return_value = '/?key=value'

        decorated_view = decorators.otp_required(
            verify_url='/otp/verify', redirect_field_name='go')(dummy_view)
        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], '/otp/verify?go=/%3Fkey%3Dvalue')

    def test_otp_required_pass_not_verified_default_verify_url(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verified = False
        request.build_absolute_uri.return_value = 'http://localhost/'
        request.get_full_path.return_value = '/?key=value'

        with self.settings(OTP_VERIFY_URL='/otp_verify'):
            decorated_view = decorators.otp_required(redirect_field_name='go')(dummy_view)

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], '/otp_verify?go=/%3Fkey%3Dvalue')

    def test_otp_required_pass_view_as_argument(self):
        request = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verified = True

        decorated_view = decorators.otp_required(dummy_view)

        self.assertEqual(decorated_view(request), 'SIGNATURE')
