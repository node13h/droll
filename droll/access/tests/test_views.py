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


from unittest.mock import MagicMock

# sensitive_post_parameters requires valid HttpRequest
from django.test import TestCase, RequestFactory
from django.conf import settings

from .. import views


class OtpVerifyTestCase(TestCase):
    def test_redirect_unauthenticated(self):
        request = RequestFactory().get('/otp/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        with self.settings(LOGIN_URL='/login/', LOGIN_REDIRECT_URL='/admin/'):
            response = views.otp_verify(request, redirect_field_name='go')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?go=/admin/')

    def test_redirect_unauthenticated_redirect_in_get(self):
        request = RequestFactory().get('/otp/', data={'go': '/admin/'})
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        with self.settings(LOGIN_URL='/login/'):
            response = views.otp_verify(request, redirect_field_name='go')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?go=/admin/')

    def test_redirect_unauthenticated_redirect_in_post(self):
        request = RequestFactory().post('/otp/', data={'go': '/admin/'})
        request._dont_enforce_csrf_checks = True  # Bypass CSRF checks
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        with self.settings(LOGIN_URL='/login/'):
            response = views.otp_verify(request, redirect_field_name='go')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?go=/admin/')

    def test_csrf_protect(self):
        request = RequestFactory().get('/otp/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        response = views.otp_verify(request)
        csrf_token = request.META['CSRF_COOKIE']

        request = RequestFactory().post(
            '/otp/', data={'csrfmiddlewaretoken': csrf_token})
        request.COOKIES[settings.CSRF_COOKIE_NAME] = csrf_token
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False
        request.user.two_fa_enabled = True

        response = views.otp_verify(request)
        self.assertEqual(response.status_code, 302)

    def test_csrf_protect_reject(self):
        request = RequestFactory().post('/otp/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        response = views.otp_verify(request)
        self.assertEqual(response.status_code, 403)

    def test_never_cache(self):
        request = RequestFactory().get('/otp/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        response = views.otp_verify(request)
        self.assertIn('Cache-Control', response)

    def test_sensitive_post_parameters(self):
        request = RequestFactory().get('/otp/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        views.otp_verify(request)
        self.assertEqual(request.sensitive_post_parameters, '__ALL__')

    def test_verify_success(self):
        request = RequestFactory().post('/otp/', data={'go': '/admin/',
                                                       'code': '000000'})
        request._dont_enforce_csrf_checks = True
        request.session = {}
        request.user = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verify.return_value = True

        response = views.otp_verify(request, redirect_field_name='go')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/admin/')

    def test_verify_fail(self):
        request = RequestFactory().post('/otp/', data={'go': '/admin/',
                                                       'code': '000000'})
        request._dont_enforce_csrf_checks = True
        request.user = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verify.return_value = False

        response = views.otp_verify(request, redirect_field_name='go')

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_unsafe_redirect(self):
        request = RequestFactory().post('/otp/', data={'go': 'irc://localhost',
                                                       'code': '000000'})
        request._dont_enforce_csrf_checks = True
        request.session = MagicMock()
        request.user = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True
        request.user.otp_verify.return_value = True

        with self.settings(LOGIN_REDIRECT_URL='/safe/'):
            response = views.otp_verify(request, redirect_field_name='go')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/safe/')

    def test_authenticated_get_context(self):
        request = RequestFactory().get('/otp/', data={'go': '/admin/'})

        request._dont_enforce_csrf_checks = True
        request.user = MagicMock()
        request.user.is_authenticated.return_value = True
        request.user.two_fa_enabled = True

        response = views.otp_verify(request, redirect_field_name='go',
                                    extra_context={'extra': 'context'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertIn('go', response.context_data)
        self.assertIn('site', response.context_data)
        self.assertIn('site_name', response.context_data)
        self.assertIn('extra', response.context_data)
