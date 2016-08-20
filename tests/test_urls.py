from django.test import TestCase
from django.core.urlresolvers import reverse


class UrlsTestCase(TestCase):

    def test_reverse_landing(self):
        url = reverse('landing')
        self.assertEqual(url, '/')

    def test_reverse_blog_post_detail(self):
        url = reverse('blog:post_detail',
                      kwargs={'slug': 'test-post',
                              'year': '2016',
                              'month': '08',
                              'day': '01'})
        self.assertEqual(url, '/blog/2016-08-01-test-post/')
