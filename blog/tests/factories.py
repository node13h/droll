import factory

from blog.models import Post, Link
from access.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'Post nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    title = factory.Sequence(lambda n: 'Link nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)
    url = 'http://www.google.com/'
