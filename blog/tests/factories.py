import factory

from blog.models import Post
from access.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'Post nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)
