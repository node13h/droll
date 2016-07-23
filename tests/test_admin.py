from unittest.mock import MagicMock, patch, ANY

from django.test import TestCase
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth import REDIRECT_FIELD_NAME

from droll import admin
import access.models
import blog.models
import core.models


class AdminModuleTestCase(TestCase):
    def test_site(self):
        self.assertIsInstance(admin.site, admin.AdminSite)

    def test_registered(self):
        self.assertIn(Group, admin.site._registry)
        self.assertIn(access.models.User, admin.site._registry)
        self.assertIn(blog.models.Post, admin.site._registry)
        self.assertIn(core.models.Link, admin.site._registry)


class AdminSiteTestCase(TestCase):
    @patch.object(admin, 'otp_verify')
    def test_otp_verify(self, m_otp_verify):
        # never_cache requires valid HttpResponse
        m_otp_verify.return_value = HttpResponse()
        request = MagicMock()
        request.GET = {}
        request.POST = {}

        admin_site = admin.AdminSite()

        admin_site.otp_verify(request)

        args, kwargs = m_otp_verify.call_args
        self.assertIn('site_title', kwargs['extra_context'])
        self.assertIn('site_header', kwargs['extra_context'])
        self.assertIn('site_url', kwargs['extra_context'])
        self.assertIn('has_permission', kwargs['extra_context'])
        self.assertIn('title', kwargs['extra_context'])
        self.assertIn('app_path', kwargs['extra_context'])
        self.assertIn(REDIRECT_FIELD_NAME, kwargs['extra_context'])
        self.assertIn('current_app', kwargs)
        self.assertEqual(kwargs['template_name'], 'admin/otp.html')

    @patch.object(admin, 'otp_verify')
    def test_otp_verify_redirect_field_in_get(self, m_otp_verify):
        # never_cache requires valid HttpResponse
        m_otp_verify.return_value = HttpResponse()
        request = MagicMock()
        request.GET = {REDIRECT_FIELD_NAME: '/'}
        request.POST = {}

        admin_site = admin.AdminSite()

        admin_site.otp_verify(request)

        args, kwargs = m_otp_verify.call_args
        self.assertNotIn(REDIRECT_FIELD_NAME, kwargs['extra_context'])

    @patch.object(admin, 'otp_verify')
    def test_otp_verify_redirect_field_in_post(self, m_otp_verify):
        # never_cache requires valid HttpResponse
        m_otp_verify.return_value = HttpResponse()
        request = MagicMock()
        request.GET = {}
        request.POST = {REDIRECT_FIELD_NAME: '/'}

        admin_site = admin.AdminSite()

        admin_site.otp_verify(request)

        args, kwargs = m_otp_verify.call_args
        self.assertNotIn(REDIRECT_FIELD_NAME, kwargs['extra_context'])

    @patch.object(admin, 'otp_verify')
    def test_otp_verify_never_cache(self, m_otp_verify):
        # never_cache requires valid HttpResponse
        m_otp_verify.return_value = HttpResponse()
        request = MagicMock()
        request.GET = {}
        request.POST = {}

        admin_site = admin.AdminSite()

        response = admin_site.otp_verify(request)

        self.assertIn('Cache-Control', response)

    def test_get_urls(self):
        admin_site = admin.AdminSite()
        self.assertIn(r'otp_verify', [p.name for p in admin_site.get_urls()])

    @patch.object(admin, 'verified_otp_required')
    def test_admin_view_is_decorated(self, m_verified_otp_required):
        admin_site = admin.AdminSite()

        admin_site.admin_view(None)
        m_verified_otp_required.assert_called_with(ANY, verify_url='/admin/otp/',
                                                   pass_unauthenticated=True)
