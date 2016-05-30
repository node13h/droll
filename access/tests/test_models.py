from django.test import TestCase
from django.db import IntegrityError

import pyotp

from .factories import UserFactory
from ..models import User


class UserTestCase(TestCase):
    def test_model(self):
        user = UserFactory()

        self.assertTrue(user.pk)

    def test_get_full_name(self):
        user = UserFactory(email='john.smith@example.com')

        self.assertEqual(user.get_full_name(), 'john.smith@example.com')

    def test_get_short_name(self):
        user = UserFactory(email='john.smith@example.com')

        self.assertEqual(user.get_short_name(), 'john.smith@example.com')

    def test_duplicate_email_raises(self):
        UserFactory(email='john.smith@example.com')
        with self.assertRaises(IntegrityError):
            UserFactory(email='john.smith@example.com')

    def test_two_fa_disabled_by_default(self):
        user = UserFactory()
        self.assertFalse(user.two_fa_enabled)

    def test_otp_reset_secret_auto_secret(self):
        user = UserFactory()
        user.otp_reset_secret()
        self.assertEqual(len(user.otp_secret), 16)

    def test_otp_reset_secret_manual_secret(self):
        user = UserFactory()
        user.otp_reset_secret('43OX5WC634FQO5UY')
        self.assertEqual(user.otp_secret, '43OX5WC634FQO5UY')

    def test_otp_verify(self):
        user = UserFactory()
        user.otp_reset_secret('43OX5WC634FQO5UY')
        totp = pyotp.TOTP('43OX5WC634FQO5UY')
        user.otp_verify(totp.now())
        self.assertTrue(user.otp_verified)

    def test_otp_verify_bad_code(self):
        user = UserFactory()
        user.otp_reset_secret('43OX5WC634FQO5UY')
        user.otp_verify('BAD-CODE')
        self.assertFalse(user.otp_verified)

    def test_otp_verified_false_by_default(self):
        user = UserFactory.build()
        self.assertFalse(user.otp_verified)


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
