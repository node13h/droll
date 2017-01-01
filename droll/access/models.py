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


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from . import otp


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, blank=False)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    otp_secret = models.CharField(
        _('OTP secret'), max_length=16, default='', editable=False)
    two_fa_enabled = models.BooleanField(
        _('2FA enabled'), default=False, help_text=_(
            'Designates whether the user has enabled two-factor auth.'))

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def otp_reset_secret(self, new_secret=None):
        """
        Sets new OTP secret. If none supplied - autogenerates one
        """

        if new_secret is None:
            self.otp_secret = otp.generate_secret()
        else:
            self.otp_secret = new_secret

    def otp_verify(self, code):
        return otp.verify(self.otp_secret, code)

    # TODO def otp_generate_url
