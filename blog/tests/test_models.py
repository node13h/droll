from django.test import TestCase

from .factories import PostFactory


class PostTestCase(TestCase):
    def test_model(self):
        post = PostFactory()

        self.assertTrue(post.pk)
