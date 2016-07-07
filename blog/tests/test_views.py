from unittest.mock import MagicMock

from django.test import TestCase, RequestFactory

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
