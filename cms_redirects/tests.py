from django.test import TestCase
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth.models import User
from django.test.utils import override_settings

from cms.api import create_page, publish_page
from cms_redirects.models import CMSRedirect


@override_settings(APPEND_SLASH=False)
class TestRedirects(TestCase):

    def setUp(self):

        self.site = Site.objects.get_current()

        self.page = create_page(title='Hello world!',
                                # TODO we're assuming here that at least one template exists
                                # in the settings file.
                                template=settings.CMS_TEMPLATES[0][0],
                                language='en'
                                )

        self.user = User.objects.create_user('test_user', 'test@example.com', 'test_user')
        self.user.is_superuser = True
        self.user.save()

        publish_page(self.page, self.user)

    def test_301_page_redirect(self):
        r_301_page = CMSRedirect(site=self.site,
                                 page=self.page,
                                 old_path='/301_page.php')
        r_301_page.save()

        r = self.client.get('/301_page.php')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r._headers['location'][1], 'http://testserver/')

    def test_302_page_redirect(self):
        r_302_page = CMSRedirect(site=self.site,
                                 page=self.page,
                                 old_path='/302_page.php',
                                 response_code='302')
        r_302_page.save()

        r = self.client.get('/302_page.php')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r._headers['location'][1], 'http://testserver/')

    def test_301_path_redirect(self):
        r_301_path = CMSRedirect(site=self.site,
                                 new_path='/',
                                 old_path='/301_path.php')
        r_301_path.save()

        r = self.client.get('/301_path.php')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r._headers['location'][1], 'http://testserver/')

    def test_302_path_redirect(self):
        r_302_path = CMSRedirect(site=self.site,
                                 new_path='/',
                                 old_path='/302_path.php',
                                 response_code='302')
        r_302_path.save()

        r = self.client.get('/302_path.php')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r._headers['location'][1], 'http://testserver/')

    def test_410_redirect(self):
        r_410 = CMSRedirect(site=self.site,
                            old_path='/410.php',
                            response_code='302')
        r_410.save()

        r = self.client.get('/410.php')
        self.assertEqual(r.status_code, 410)

    def test_redirect_can_ignore_query_string(self):
        """
        Set up a redirect as in the generic 301 page case, but then try to get this page with
        a query string appended.  Succeed nonetheless.
        """
        r_301_page = CMSRedirect(site=self.site,
                                 page=self.page,
                                 old_path='/301_page.php')
        r_301_page.save()

        r = self.client.get('/301_page.php?this=is&a=query&string')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r._headers['location'][1], 'http://testserver/')
