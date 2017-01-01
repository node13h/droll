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

from django.test import TestCase, RequestFactory
from django.http import Http404

from .. import views
from .factories import PostFactory


class RollViewTestCase(TestCase):
    def setUp(self):
        self.view = views.RollView.as_view()

    def test_unauthenticated_empty(self):
        request = RequestFactory().get('/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        response = self.view(request)
        self.assertContains(response, '<html')

    def test_template(self):
        request = RequestFactory().get('/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        PostFactory(body='POST-BODY-MARKER', public=True)

        response = self.view(request)
        self.assertContains(response, 'POST-BODY-MARKER')

    def test_public(self):
        request = RequestFactory().get('/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        PostFactory(body='POST1-BODY-MARKER', public=True)
        PostFactory(body='POST2-BODY-MARKER')

        response = self.view(request)

        posts = response.context_data['object_list']
        self.assertTrue(posts.filter(body='POST1-BODY-MARKER').exists())
        self.assertFalse(posts.filter(body='POST2-BODY-MARKER').exists())


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.view = views.PostDetailView.as_view()

    def test_unauthenticated_public(self):
        post = PostFactory(body='POST-BODY-MARKER', public=True)
        request = RequestFactory().get(post.get_absolute_url())
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        response = self.view(request, slug=post.slug)
        self.assertContains(response, 'POST-BODY-MARKER')
        self.assertEqual(response.context_data['object'], post)
        self.assertEqual(response.context_data['post'], post)

    def test_unauthenticated_private(self):
        post = PostFactory(body='POST-BODY-MARKER', public=False)
        request = RequestFactory().get(post.get_absolute_url())
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        with self.assertRaises(Http404):
            self.view(request, slug=post.slug)

    def test_unauthenticated_private_own(self):
        post = PostFactory(body='POST-BODY-MARKER', public=False)
        request = RequestFactory().get(post.get_absolute_url())
        request.user = post.user

        response = self.view(request, slug=post.slug)
        self.assertContains(response, 'POST-BODY-MARKER')
        self.assertEqual(response.context_data['object'], post)
        self.assertEqual(response.context_data['post'], post)
