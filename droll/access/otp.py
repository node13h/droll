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


from django.conf import settings

import pyotp


def generate_secret():
    """
    Generate random OTP secret

    :rtype: str
    :returns: 16-character string
    """

    return pyotp.random_base32()


def verify(secret, code):
    """
    Verify time-based code

    :param str secret: OTP secret string
    :param str code: The code to be verified

    :rtype: bool
    :returns: true on success
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code)


def set_verified(request):
    """
    Sets cookie indicating OTP verification check was passed successfully.
    Cookie is used by is_verified().

    :param request: HttpRequest object
    """

    request.session[settings.OTP_SESSION_FLAG_NAME] = True


def is_verified(request):
    """
    Checks OTP verification state session flag and returns True if set.

    :param request: HttpRequest object

    :rtype: bool
    :returns: True if OTP verification was passed
    """

    return request.session.get(settings.OTP_SESSION_FLAG_NAME, False)
