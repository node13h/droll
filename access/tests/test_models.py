from django.test import TestCase
from django.db import IntegrityError

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
