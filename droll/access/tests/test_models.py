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


from unittest.mock import patch

from django.test import TestCase
from django.db import IntegrityError

from .factories import UserFactory
from ..models import User
from .. import otp


class UserTestCase(TestCase):
    def test_model(self):
        user = UserFactory()

        self.assertTrue(user.pk)

    def test_get_full_name(self):
        user = UserFactory.build(email='john.smith@example.com')

        self.assertEqual(user.get_full_name(), 'john.smith@example.com')

    def test_get_short_name(self):
        user = UserFactory.build(email='john.smith@example.com')

        self.assertEqual(user.get_short_name(), 'john.smith@example.com')

    def test_duplicate_email_raises(self):
        UserFactory(email='john.smith@example.com')
        with self.assertRaises(IntegrityError):
            UserFactory(email='john.smith@example.com')

    def test_two_fa_disabled_by_default(self):
        user = UserFactory.build()
        self.assertFalse(user.two_fa_enabled)

    @patch.object(otp, 'generate_secret')
    def test_otp_reset_secret_auto_secret(self, m_generate_secret):
        m_generate_secret.return_value = '43OX5WC634FQO5UY'
        user = UserFactory.build(otp_secret='')
        user.otp_reset_secret()
        self.assertEqual(user.otp_secret, '43OX5WC634FQO5UY')

    def test_otp_reset_secret_manual_secret(self):
        user = UserFactory.build(otp_secret='')
        user.otp_reset_secret('43OX5WC634FQO5UY')
        self.assertEqual(user.otp_secret, '43OX5WC634FQO5UY')

    @patch.object(otp, 'verify')
    def test_otp_verify_success(self, m_verify):
        m_verify.return_value = True
        user = UserFactory.build()
        self.assertTrue(user.otp_verify('000000'))

    @patch.object(otp, 'verify')
    def test_otp_verify_fail(self, m_verify):
        m_verify.return_value = False
        user = UserFactory.build()
        self.assertFalse(user.otp_verify('000000'))


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user('john.smith@example.com', 's3cret')

        self.assertTrue(user.pk)
        self.assertEqual(user.email, 'john.smith@example.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('s3cret'))

    def test_create_user_email_normalized(self):
        User.objects.create_user('john.smith@ExAmPlE.com', 's3cret')
        with self.assertRaises(IntegrityError):
            User.objects.create_user('john.smith@example.com')

    def test_create_user_empty_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('')
