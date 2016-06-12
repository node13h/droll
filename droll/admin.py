from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf.urls import url
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from access.decorators import verified_otp_required
from access.models import User
from access.admin import UserAdmin
from access.views import otp_verify


class AdminSite(admin.AdminSite):
    """
    Custom admin site with two-factor auth support
    """

    @never_cache
    def otp_verify(self, request):
        """
        OTP verify view. Based on AdminSite.login view
        """

        context = dict(self.each_context(request),
                       title=_('Verify OTP'),
                       app_path=request.get_full_path())

        if (REDIRECT_FIELD_NAME not in request.GET and
                REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = request.get_full_path()

        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'login_url': reverse('admin:login'),
            'template_name': 'admin/otp.html',
        }

        return otp_verify(request, **defaults)

    def get_urls(self):
        urls = super().get_urls()
        urls.append(url(r'^otp/$', self.otp_verify, name='otp_verify'))

        return urls

    def admin_view(self, view, cacheable=False):
        """
        Pass wrapped views through an OTP verification check
        """

        verify_url = reverse_lazy('admin:otp_verify', current_app=self.name)

        # Original admin_view() already requires authentication for all views
        # except for login/logout views. As we are adding outer OTP
        # verification decorator we need to pass through unauthenticated
        # requests to the inner view for normal authentication to happen first,
        # hence the pass_unauthenticated=True
        return verified_otp_required(super().admin_view(view, cacheable),
                                     verify_url=verify_url,
                                     pass_unauthenticated=True)


site = AdminSite()

site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
