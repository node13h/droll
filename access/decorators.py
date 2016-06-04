from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.conf import settings


def otp_required(view=None, verify_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    if verify_url is None:
        verify_url = settings.OTP_VERIFY_URL

    def test_func(user):
        return not user.is_authenticated() or (not user.two_fa_enabled or
                                               user.otp_verified)

    decorator = user_passes_test(
        test_func, login_url=verify_url, redirect_field_name=redirect_field_name)

    return decorator if view is None else decorator(view)
