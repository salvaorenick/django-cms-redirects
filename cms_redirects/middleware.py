from cms_redirects.models import CMSRedirect
from django import http
from django.conf import settings

class RedirectFallbackMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, http.Http404):
            path = request.get_full_path()
        try:
            r = CMSRedirect.objects.get(site__id__exact=settings.SITE_ID, old_path=path)
        except CMSRedirect.DoesNotExist:
            r = None
        if r is None and settings.APPEND_SLASH:
            # Try removing the trailing slash.
            try:
                r = CMSRedirect.objects.get(site__id__exact=settings.SITE_ID,
                    old_path=path[:path.rfind('/')]+path[path.rfind('/')+1:])
            except CMSRedirect.DoesNotExist:
                pass
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
        

