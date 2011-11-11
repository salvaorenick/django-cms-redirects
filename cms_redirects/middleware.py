from urlparse import urlparse
from cms_redirects.models import CMSRedirect
from django import http
from django.conf import settings

def get_redirect(old_path):
    try:
        r = CMSRedirect.objects.get(site__id__exact=settings.SITE_ID,
                                    old_path=old_path)
    except CMSRedirect.DoesNotExist:
        r = None
    return r

def remove_slash(path):
    return path[:path.rfind('/')]+path[path.rfind('/')+1:]

def remove_query(path):
    return path.split('?', 1)[0]

class RedirectFallbackMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, http.Http404):
            path = request.environ.get('PATH_INFO')
            r = get_redirect(path)

            # If we couldn't find the path, try removing the slash
            # and/or removing the query string.
            if r is None and settings.APPEND_SLASH:
                r = get_redirect(remove_slash(path))
            if r is None and path.count('?'):
                r = get_redirect(remove_query(path))
            if r is None and path.count('?') and settings.APPEND_SLASH:
                r = get_redirect(remove_slash(remove_query(path)))

            if r is not None:
                if r.page:
                    if r.response_code == '302':
                        return http.HttpResponseRedirect(r.page.get_absolute_url())
                    else:
                        return http.HttpResponsePermanentRedirect(r.page.get_absolute_url())
                if r.new_path == '':
                    return http.HttpResponseGone()
                if r.response_code == '302':
                    return http.HttpResponseRedirect(r.new_path)
                else:
                    return http.HttpResponsePermanentRedirect(r.new_path)
