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
