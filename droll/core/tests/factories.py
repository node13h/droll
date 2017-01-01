import factory

from ..models import Link
from droll.access.tests.factories import UserFactory


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    title = factory.Sequence(lambda n: 'Link nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)
    url = 'http://www.google.com/'
