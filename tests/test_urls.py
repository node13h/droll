from django.test import TestCase
from django.core.urlresolvers import reverse


class UrlsTestCase(TestCase):

    def test_reverse_landing(self):
        url = reverse('landing')
        self.assertEqual(url, '/')
