from unittest.mock import MagicMock

from django.test import TestCase

from ..middleware import TwoFactorAuthMiddleware


class TwoFactorAuthMiddlewareTestCase(TestCase):
    def test_process_request_sets_true(self):
        middleware = TwoFactorAuthMiddleware()
        request = MagicMock()
        request.user.otp_verified = False
        request.session = {'twofaflagname': True}
        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            middleware.process_request(request)

        self.assertTrue(request.user.otp_verified)

    def test_process_request_sets_false(self):
        middleware = TwoFactorAuthMiddleware()
        request = MagicMock()
        request.user.otp_verified = False
        request.session = {'twofaflagname': False}
        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            middleware.process_request(request)

        self.assertFalse(request.user.otp_verified)
