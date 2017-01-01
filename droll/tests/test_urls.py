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
from django.core.urlresolvers import reverse


class UrlsTestCase(TestCase):

    def test_reverse_landing(self):
        url = reverse('landing')
        self.assertEqual(url, '/')

    def test_reverse_blog_post_detail(self):
        url = reverse('blog:post_detail',
                      kwargs={'slug': 'test-post',
                              'year': '2016',
                              'month': '08',
                              'day': '01'})
        self.assertEqual(url, '/blog/2016-08-01-test-post/')
