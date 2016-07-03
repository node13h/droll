from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = models.SlugField(_('slug'), editable=False)
    public = models.BooleanField(_('public'), default=False, db_index=True)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, db_index=True)
    title = models.CharField(_('title'), max_length=140)
    body = models.TextField(_('body'))
