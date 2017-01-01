from unittest.mock import MagicMock

from django.test import TestCase

from droll.access.tests.factories import UserFactory
from .factories import LinkFactory
from .. import context_processors


class CoreContextProcessorsTestCase(TestCase):
    def test_site_title(self):
        with self.settings(SITE_TITLE='Expected site title'):
            context = context_processors.site_title(MagicMock())
            self.assertEqual(context['title'], 'Expected site title')

    def test_links(self):
        user1 = UserFactory()
        user2 = UserFactory()

        link1 = LinkFactory(user=user1)
        link2 = LinkFactory(user=user1)
        link3 = LinkFactory(user=user2)

        request = MagicMock()
        request.user.is_authenticated.return_value = False

        links = context_processors.links(request)['links']

        self.assertIn(link1, links)
        self.assertIn(link2, links)
        self.assertIn(link3, links)
