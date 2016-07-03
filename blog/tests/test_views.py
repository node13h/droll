from unittest.mock import MagicMock

from django.test import TestCase, RequestFactory

from .. import views


class RollViewTestCase(TestCase):
    def setUp(self):
        self.view = views.RollView.as_view()

    def test_unauthenticated_empty(self):
        request = RequestFactory().get('/')
        request.user = MagicMock()
        request.user.is_authenticated.return_value = False

        response = self.view(request)
        self.assertContains(response, '<html')
