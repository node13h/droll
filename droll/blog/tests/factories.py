import factory

from ..models import Post
from droll.access.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'Post nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)
