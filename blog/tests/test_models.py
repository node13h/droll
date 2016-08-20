from unittest.mock import MagicMock
from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from .factories import PostFactory
from ..models import Post
from access.tests.factories import UserFactory


class PostTestCase(TestCase):
    def test_model(self):
        post = PostFactory()

        self.assertTrue(post.pk)

    def test_str(self):
        post = PostFactory.build()
        post.slug = 'test-post'

        self.assertEqual(str(post), 'test-post')

    def test_slug_derived_from_title_on_save(self):
        post = PostFactory()
        post.title = 'This is a test post'
        post.save()
        self.assertEqual(post.slug, 'this-is-a-test-post')

    def test_queryset_relevant(self):
        user1 = UserFactory()
        user2 = UserFactory()

        post1 = PostFactory(user=user1, public=True)
        post2 = PostFactory(user=user1, public=False)
        post3 = PostFactory(user=user2, public=True)
        post4 = PostFactory(user=user2, public=False)

        relevant = Post.objects.all().relevant(user1)

        self.assertIn(post1, relevant)
        self.assertIn(post2, relevant)
        self.assertIn(post3, relevant)
        self.assertNotIn(post4, relevant)

    def test_queryset_relevant_unauthenticated_public_only(self):
        user1 = MagicMock()
        user1.is_authenticated.return_value = False
        user2 = UserFactory()

        post1 = PostFactory(user=user2, public=True)
        post2 = PostFactory(user=user2, public=False)

        relevant = Post.objects.all().relevant(user1)

        self.assertIn(post1, relevant)
        self.assertNotIn(post2, relevant)

    def test_manager_roll_non_public_own_only(self):
        user1 = UserFactory()
        user2 = UserFactory()

        post1 = PostFactory(user=user1, public=True)
        post2 = PostFactory(user=user1, public=False)
        post3 = PostFactory(user=user2, public=True)
        post4 = PostFactory(user=user2, public=False)

        roll = Post.objects.roll(user1)

        self.assertIn(post1, roll)
        self.assertIn(post2, roll)
        self.assertIn(post3, roll)
        self.assertNotIn(post4, roll)

    def test_manager_roll_unauthenticated_public_only(self):
        user1 = MagicMock()
        user1.is_authenticated.return_value = False
        user2 = UserFactory()

        post1 = PostFactory(user=user2, public=True)
        post2 = PostFactory(user=user2, public=False)

        roll = Post.objects.roll(user1)

        self.assertIn(post1, roll)
        self.assertNotIn(post2, roll)

    def test_manager_roll_default_order_newest_to_oldest(self):
        user = UserFactory()

        post1 = PostFactory(user=user, timestamp=datetime(1980, 5, 3, tzinfo=utc))
        post2 = PostFactory(user=user, timestamp=datetime(1980, 5, 2, tzinfo=utc))
        post3 = PostFactory(user=user, timestamp=datetime(1980, 5, 6, tzinfo=utc))

        roll_list = list(Post.objects.roll(user))

        self.assertEqual(roll_list, [post3, post1, post2])

    def test_manager_roll_limit(self):
        user = UserFactory()

        post1 = PostFactory(user=user, timestamp=datetime(1980, 5, 3, tzinfo=utc))
        post2 = PostFactory(user=user, timestamp=datetime(1980, 5, 2, tzinfo=utc))

        roll = Post.objects.roll(user, limit=1)

        self.assertIn(post1, roll)
        self.assertNotIn(post2, roll)

    def test_manager_roll_start(self):
        user = UserFactory()

        post1 = PostFactory(user=user, timestamp=datetime(1980, 5, 3, tzinfo=utc))
        post2 = PostFactory(user=user, timestamp=datetime(1980, 5, 2, tzinfo=utc))

        roll = Post.objects.roll(user, start=datetime(1980, 5, 3, tzinfo=utc))

        self.assertIn(post1, roll)
        self.assertNotIn(post2, roll)
