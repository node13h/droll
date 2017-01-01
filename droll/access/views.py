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


from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.conf import settings
from django.template.response import TemplateResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login

from .forms import OtpForm
from . import otp


@sensitive_post_parameters()
@csrf_protect
@never_cache
def otp_verify(request, template_name='registration/otp.html',
               login_url=None,
               redirect_field_name=REDIRECT_FIELD_NAME,
               otp_form=OtpForm,
               current_app=None, extra_context=None):
    """
    Display OTP form and handle the verification action if user is
    authenticated. Redirect to the URL specified in
    redirect_field_name argument otherwise. Resembles
    login view from django.contrib.auth.views

    :param HttpRequest request: The request object
    :param str vtemplate_name: File to use as a template for the view
    :param str redirect_field_name: URL query argument containing URL
        to redirect to
    :param Form form: Form class to use in the view
    :param str current_app: Current app name
    :param dict extra_context: Extra context dict to pass to the template

    :returns: HttpResponse
    """

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    # Ensure the user-originating redirection url is safe.
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)

    if not request.user.is_authenticated():
        return redirect_to_login(redirect_to, login_url=resolved_login_url,
                                 redirect_field_name=redirect_field_name)

    if request.method == 'POST':
        form = otp_form(request, request.POST)

        if form.is_valid():
            otp.set_verified(request)
            return HttpResponseRedirect(redirect_to)
    else:
        form = otp_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
