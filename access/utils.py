from django.conf import settings


def two_fa_pass(request):
    """
    Sets cookie indicating two-factor auth was passed successfully.
    Cookie is used by two_fa_check().

    :param request: HttpRequest object
    """

    request.session[settings.TWO_FA_SESSION_FLAG_NAME] = True


def two_fa_check(request):
    """
    Checks two-factor auth session flag and returns True if set.
    Used by TwoFactorAuthMiddleware to set request.user.otp_verified

    :param request: HttpRequest object

    :rtype: bool
    :returns: True if two-factor auth has been passed else False
    """

    return request.session.get(settings.TWO_FA_SESSION_FLAG_NAME, False)
