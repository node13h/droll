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


from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.core.urlresolvers import reverse


class PostQuerySet(models.QuerySet):
    def relevant(self, user):
        f = Q(public=True)

        if user.is_authenticated():
            f |= Q(user=user)

        return self.filter(f)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def roll(self, user, *, limit=None, start=None):
        """
        Return personalized blog roll

        :param User user: user to prepare personalized roll for
        :param int limit: maximum number of object to return
        :param datetime start: minimum timestamp to return

        :rtype: QuerySet
        :returns: filtered QuerySet
        """

        qs = self.get_queryset()

        if start is not None:
            qs = qs.filter(timestamp__gte=start)

        qs = qs.relevant(user).order_by('-timestamp')

        if limit is not None:
            qs = qs[:limit]

        return qs


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = models.SlugField(_('slug'), editable=False)
    public = models.BooleanField(_('public'), default=False, db_index=True)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, db_index=True)
    title = models.CharField(_('title'), max_length=140)
    body = models.TextField(_('body'))

    objects = PostManager()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       kwargs={'slug': self.slug,
                               'year': '{:04d}'.format(self.timestamp.year),
                               'month': '{:02d}'.format(self.timestamp.month),
                               'day': '{:02d}'.format(self.timestamp.day)})


@receiver(pre_save, sender=Post)
def update_slug(sender, instance, *args, **kwargs):
    # The following will update slug each time title changes..
    # TODO Implement Slug model to keep history of the slugs for
    # the Post model to avoiud broken links on title change.
    instance.slug = slugify(instance.title)
