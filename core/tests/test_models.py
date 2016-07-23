from django.test import TestCase

from .factories import LinkFactory


class LinkTestCase(TestCase):
    def test_model(self):
        link = LinkFactory()

        self.assertTrue(link.pk)
