from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Link(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(_('title'), max_length=30)
    url = models.CharField(_('URL'), max_length=2000)
