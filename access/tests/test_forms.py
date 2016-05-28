from django.test import TestCase

from ..forms import UserCreationForm, UserChangeForm


class UserCreationFormTestCase(TestCase):
    def test_class(self):
        form = UserCreationForm()
        self.assertFalse(form.is_valid())


class UserChangeFormTestCase(TestCase):
    def test_class(self):
        form = UserChangeForm()
        self.assertFalse(form.is_valid())
