import os


class Env(object):
    """
    Get/set environment variables
    """

    true_values = ('true', '1', 'yes', 'on')

    def __init__(self):
        self.env = os.environ

    def __setitem__(self, key, value):
        """
        Assign value to env var. Convert boolean or integer values to string
        representations
        """
        if type(value) is bool:
            self.env[key] = self.true_values[0] if value else ''
        elif type(value) is int:
            self.env[key] = str(value)
        else:
            self.env[key] = value

    def __delitem__(self, key):
        """
        Delete env var
        """

        del self.env[key]

    def get(self, var, default=None):
        """
        Return raw env var value or default if not set
        """

        try:
            value = self.env[var]
        except KeyError:
            return default

        return value

    def get_int(self, var, default=None):
        """
        Cast env var value to integer before returning.
        Return default if value is invalid or not set
        """

        try:
            value = self.env[var]
        except KeyError:
            return default

        try:
            return int(value)
        except ValueError:
            return default

    def get_bool(self, var, default=False):
        """
        Cast env var value to boolean before returning.
        Return default if value is not set
        """
        try:
            value = self.env[var]
        except KeyError:
            return default

        return value.lower() in self.true_values
