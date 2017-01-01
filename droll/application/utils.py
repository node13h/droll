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

    def get_list(self, var, default=None):
        """
        Split env var value before returning
        Return default if value is not set
        """

        try:
            value = self.env[var]
        except KeyError:
            return default

        if value:
            return value.split(',')
        else:
            return []
