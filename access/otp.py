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

    :rtype: str
    :returns: true on success
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
