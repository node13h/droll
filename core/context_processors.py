from django.conf import settings


def site_title(request):
    return {'title': settings.SITE_TITLE}
