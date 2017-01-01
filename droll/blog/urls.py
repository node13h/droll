from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})-(?P<slug>[\w-]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail')
    ]
