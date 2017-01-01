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
