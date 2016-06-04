from .utils import two_fa_check


class TwoFactorAuthMiddleware(object):
    """
    Sets the otp_verified property of the request.user to
    the current two-factor auth state
    """

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The two-factor auth middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "the 'access.middleware.TwoFactorAuthMiddleware'."
        )
        assert hasattr(request, 'user'), (
            "The two-factor auth middleware requires the "
            "authentication middleware to be installed. Edit your "
            "MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "the 'access.middleware.TwoFactorAuthMiddleware'."
        )

        request.user.otp_verified = two_fa_check(request)
