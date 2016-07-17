from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings


class PostManager(models.Manager):
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

        f = Q(public=True)

        if user.is_authenticated():
            f |= Q(user=user)

        qs = qs.filter(f).order_by('-timestamp')

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
