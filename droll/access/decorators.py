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


from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import otp


def verified_otp_required(view=None, *, verify_url=None,
                          redirect_field_name=REDIRECT_FIELD_NAME,
                          pass_unauthenticated=False):
    """
    Redirect to the OTP verify URL if two-factor auth is enabled, user is
    authenticated and OTP was not yet verified. Unauthenticated requests
    can optionally be excluded from being redirected (in case the decorated
    view already does authentication enforcement.
    In other cases - call the original view

    Use to protect the views with OTP (additionally to normal auth)

    | Example 1
    |
    | @login_required
    | @verified_otp_required
    | def view(request):
    |     ...

    | Example 2
    |
    | @verified_otp_required(pass_unauthenticated=True)
    | @login_required
    | def view(request):
    |     ...

    :param view: If supplied - returns decoorated version of it. Allows for
        parentheses to be omitted if used as a decorator without arguments
    :param str verify_url: OTP verification URL to redirect to
    :param str redirect_field_name: URL query argument to use to save
        the original URL
    :param bool pass_unauthenticated: Set to True to exclude the
        unauthenticated requests from checking

    :returns: view decorator or decorated view
    """

    if verify_url is None:
        verify_url = settings.OTP_VERIFY_URL

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            def no_need_to_check_otp(user):
                if not user.is_authenticated():
                    if pass_unauthenticated:
                        return True
                    else:
                        raise ImproperlyConfigured(
                            'To be able to use verified_otp_required decorator '
                            'with unauthenticated users set the '
                            'pass_unauthenticated argument value to True')
                return not user.two_fa_enabled or otp.is_verified(request)

            # Wrap the original view_func
            otp_verified_view_func = user_passes_test(
                no_need_to_check_otp, login_url=verify_url,
                redirect_field_name=redirect_field_name)(view_func)

            return otp_verified_view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator if view is None else decorator(view)
