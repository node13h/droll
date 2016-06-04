from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.conf import settings


def otp_required(view=None, verify_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect to the OTP verify URL if two-factor auth is enabled, user is
    authenticated and OTP was not verified.
    In other cases - call the original view

    Use to protect the views with OTP (additionally to normal auth)

    :param view: The decorated viev. None to act as normal decorator
    :param str verify_url: OTP verify URL to redirect to
    :param str redirect_field_name: URL query argument to use to forward original URL

    :returns: decorator
    """

    if verify_url is None:
        verify_url = settings.OTP_VERIFY_URL

    def test_func(user):
        return not user.is_authenticated() or (not user.two_fa_enabled or
                                               user.otp_verified)

    decorator = user_passes_test(
        test_func, login_url=verify_url, redirect_field_name=redirect_field_name)

    return decorator if view is None else decorator(view)
