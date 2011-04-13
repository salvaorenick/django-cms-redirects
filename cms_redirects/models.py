from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField

from cms.models import Page

RESPONSE_CODES = (
    ('301', '301'),
    ('302', '302'),
)

class CMSRedirect(models.Model):
    page = PageField(verbose_name=_("page"), blank=True, null=True, help_text=_("A link to a page has priority over a text link."))
    site = models.ForeignKey(Site)
    old_path = models.CharField(_('redirect from'), max_length=200, db_index=True,
        help_text=_("This should be an absolute path, excluding the domain name. Example: '/events/search/'."))
    new_path = models.CharField(_('redirect to'), max_length=200, blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL starting with 'http://'."))
    response_code = models.CharField(_('response code'), max_length=3, choices=RESPONSE_CODES, default=RESPONSE_CODES[0][0],
        help_text=_("This is the http response code returned if a destination is specified. If no destination is specified the response code will be 410."))
    
    def page_site(self):
        if self.page:
            return u'%s' % self.page.site
        return u''
    page_site.short_description = "Page Site"
    
    def actual_response_code(self):
        if self.page or self.new_path:
            return self.response_code
        return u'410'
    actual_response_code.short_description = "Response Code"
    
    class Meta:
        verbose_name = _('CMS Redirect')
        verbose_name_plural = _('CMS Redirects')
        unique_together=(('site', 'old_path'),)
        ordering = ('old_path',)
    
    def __unicode__(self):
        return "%s ---> %s" % (self.old_path, self.new_path)
