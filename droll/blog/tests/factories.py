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


import factory

from ..models import Post
from droll.access.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'Post nr. {}'.format(n))
    user = factory.SubFactory(UserFactory)
