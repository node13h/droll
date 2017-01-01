from django.conf import settings

from .models import Link


def site_title(request):
    return {'title': settings.SITE_TITLE}


def links(request):
    return {'links': Link.objects.all()}
