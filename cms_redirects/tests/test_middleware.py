"""Tests for redirect middleware."""
from urlparse import urlparse

from cms_redirects.models import CMSRedirect
from cms.api import create_page
from django import http
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from cms_redirects import middleware


class RedirectMiddlewareTest(TestCase):
    """Tests for redirect middleware."""
    def setUp(self):
        """A few quick things used by a lot of tests."""
        self.factory = RequestFactory()
        self.middleware = middleware.RedirectMiddleware()

    @override_settings(APPEND_SLASH=False)
    def test_get_possible_paths_append_slash_off(self):
        """Should return just path with trailing slash."""
        result = self.middleware.get_possible_paths(
            urlparse('http://localhost/some/path/'))
        self.assertEqual(result, ['/some/path/'])

    @override_settings(APPEND_SLASH=True)
    def test_get_possible_paths_append_slash_on(self):
        """Should return paths with and without appended slashes."""
        result = self.middleware.get_possible_paths(
            urlparse('http://localhost/some/path/'))
        self.assertEqual(result, ['/some/path/', '/some/path'])

    @override_settings(APPEND_SLASH=True)
    def test_get_possible_paths_append_slash_on_path_end_is_not_slash(self):
        """Should return just path without appended slash."""
        path = urlparse('http://localhost/some/path')
        result = self.middleware.get_possible_paths(path)
        self.assertEqual(result, ['/some/path'])

    def test_get_query(self):
        """Should return the query string prepended by a ?."""
        path = urlparse('http://localhost/some/path/?a=b&c=dee')
        result = self.middleware.get_query(path)
        self.assertEqual(result, 'a=b&c=dee')

    def test_get_query_empty(self):
        """Should return an empty string."""
        result = self.middleware.get_query(
            urlparse('http://localhost/some/path/'))
        self.assertEqual(result, '')

    def test_get_cms_redirect(self):
        """Should return the correct CMSRedirect object."""
        cms_redirect = CMSRedirect.objects.create(
            site_id=1, old_path='/some/path/'
        )
        result = self.middleware.get_cms_redirect(['/some/path/'])
        self.assertEqual(result.pk, cms_redirect.pk)

    def test_get_cms_redirect_does_not_exist(self):
        """Should return None."""
        result = self.middleware.get_cms_redirect((['/cows/come/home/']))
        self.assertIsNone(result)

    def test_get_cms_redirect_response_class_301(self):
        """Should return the HttpResponsePermanentRedirect class."""
        cmsredirect = CMSRedirect(response_code='301')
        result = self.middleware.get_cms_redirect_response_class(cmsredirect)
        self.assertEqual(result, http.HttpResponsePermanentRedirect)

    def test_get_cms_redirect_response_class_302(self):
        """Should return the HttpResponseRedirect class."""
        cmsredirect = CMSRedirect(response_code='302')
        result = self.middleware.get_cms_redirect_response_class(cmsredirect)
        self.assertEqual(result, http.HttpResponseRedirect)

    def test_cms_redirect_no_page_no_new_path(self):
        """Should return the HttpResponseGone class."""
        cmsredirect = CMSRedirect()
        result = self.middleware.cms_redirect(cmsredirect, {})
        self.assertTrue(isinstance(result, http.HttpResponseGone))

    def test_cms_redirect_to_page_empty_query(self):
        """Should redirect to the correct page without any querystring."""
        page = create_page(
            title='A page somewhere',
            template='template_1.html',
            language='en',
            slug='a-page-somewhere'
        )
        cmsredirect = CMSRedirect.objects.create(
            page_id=page.pk,
            site_id=1,
            old_path='/page/elsewhere/',
        )
        result = self.middleware.cms_redirect(cmsredirect, '')
        self.assertEqual(
            result['Location'], '/en/a-page-somewhere/')

    def test_cms_redirect_to_page_with_query(self):
        """Should redirect to the correct page and keep querystring."""
        page = create_page(
            title='A page somewhere',
            template='template_1.html',
            language='en',
            slug='a-page-somewhere'
        )
        cmsredirect = CMSRedirect.objects.create(
            page=page,
            site_id=1,
            old_path='/page/elsewhere/',
        )
        result = self.middleware.cms_redirect(cmsredirect, 'a=b')
        self.assertEqual(
            result['Location'], '/en/a-page-somewhere/?a=b')

    def test_cms_redirect_to_new_path(self):
        """Should redirect to the correct path and keep querystring."""
        cmsredirect = CMSRedirect.objects.create(
            site_id=1,
            old_path='/page/elsewhere/',
            new_path='/something/new/'
        )
        result = self.middleware.cms_redirect(cmsredirect, 'a=b')
        self.assertEqual(
            result['Location'], '/something/new/?a=b')

    def test_process_exception_not_404(self):
        """Should return None if the exception is not a 404."""
        result = self.middleware.process_exception(
            self.factory.get('/'), ValueError)
        self.assertIsNone(result)

    def test_process_exception_cms_redirect_empty_query(self):
        """Should redirect to the correct path."""
        CMSRedirect.objects.create(
            site_id=1,
            old_path='/page/elsewhere/',
            new_path='/something/new/'
        )
        request = self.factory.get('/page/elsewhere/')
        result = self.middleware.process_exception(request, http.Http404())
        self.assertEqual(result['Location'], '/something/new/')

    def test_process_exception_cms_redirect_with_query(self):
        """Should redirect tot he correct path, preserving querystring."""
        CMSRedirect.objects.create(
            site_id=1,
            old_path='/page/elsewhere/',
            new_path='/something/new/'
        )
        request = self.factory.get('/page/elsewhere/?a=b')
        result = self.middleware.process_exception(request, http.Http404())
        self.assertEqual(result['Location'], '/something/new/?a=b')

    def test_source_and_destination_have_query_strings(self):
        """Parameters should be merged."""
        CMSRedirect.objects.create(
            site_id=1,
            old_path='/page/elsewhere/',
            new_path='/something/new/?cow=moo'
        )
        request = self.factory.get('/page/elsewhere/?a=b')
        result = self.middleware.process_exception(request, http.Http404())
        self.assertEqual(result['Location'], '/something/new/?cow=moo&a=b')

    def test_source_and_destination_have_common_query_string_params(self):
        """Query string can have multiples of the same parameter."""
        CMSRedirect.objects.create(
            site_id=1,
            old_path='/page/elsewhere/',
            new_path='/new/?cow=moo'
        )
        request = self.factory.get('/page/elsewhere/?cow=bark&a=b')
        result = self.middleware.process_exception(request, http.Http404())
        self.assertEqual(result['Location'], '/new/?cow=moo&cow=bark&a=b')
