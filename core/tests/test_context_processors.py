from unittest.mock import MagicMock

from django.test import TestCase

from .. import context_processors


class CoreContextProcessorsTestCase(TestCase):
    def test_site_title(self):
        with self.settings(SITE_TITLE='Expected site title'):
            context = context_processors.site_title(MagicMock())
            self.assertEqual(context['title'], 'Expected site title')
