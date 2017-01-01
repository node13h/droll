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
