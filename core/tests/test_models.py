from django.test import TestCase

from .factories import LinkFactory


class LinkTestCase(TestCase):
    def test_model(self):
        link = LinkFactory()

        self.assertTrue(link.pk)

    def test_str(self):
        link = LinkFactory.build()
        link.title = 'Test Link'

        self.assertEqual(str(link), 'Test Link')
