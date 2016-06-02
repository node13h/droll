from django.test import TestCase
from unittest.mock import MagicMock

from .. import utils


class UtilsFunctionsTestCase(TestCase):
    def test_two_fa_pass(self):
        request = MagicMock()
        request.session = {}

        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            utils.two_fa_pass(request)

        self.assertEqual(request.session['twofaflagname'], True)

    def test_two_fa_check_true(self):
        request = MagicMock()
        request.session = {'twofaflagname': True}

        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            self.assertTrue(utils.two_fa_check(request))

    def test_two_fa_check_false(self):
        request = MagicMock()
        request.session = {'twofaflagname': False}

        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            self.assertFalse(utils.two_fa_check(request))

    def test_two_fa_check_missing_false(self):
        request = MagicMock()
        request.session = {}

        with self.settings(TWO_FA_SESSION_FLAG_NAME='twofaflagname'):
            self.assertFalse(utils.two_fa_check(request))
