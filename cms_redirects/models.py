"""Models for cms redirects."""
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField


RESPONSE_CODES = (
    ('301', '301'),
    ('302', '302')
)


DEFAULT_REDIRECT_RESPONSE_CODE = getattr(
    settings, 'DEFAULT_REDIRECT_RESPONSE_CODE', '301')


class CMSRedirect(models.Model):
    """Model for information about a redirect"""
    page = PageField(
        verbose_name=_("page"),
        blank=True,
        null=True,
        help_text=_("A link to a page has priority over a text link.")
    )
    site = models.ForeignKey(Site)
    old_path = models.CharField(
        verbose_name=_('redirect from'),
        max_length=200,
        db_index=True,
        help_text=_("This should be an absolute path, excluding the"
                    " domain name. Example: '/events/search/'.")
    )
    new_path = models.CharField(
        verbose_name=_('redirect to'),
        max_length=200,
        blank=True,
        help_text=_("This can be either an absolute path (as above) or a"
                    " full URL starting with 'http://'.")
    )
    response_code = models.CharField(
        verbose_name=_('response code'),
        max_length=3,
        choices=RESPONSE_CODES,
        default=DEFAULT_REDIRECT_RESPONSE_CODE,
        help_text=_("This is the http response code returned if a destination"
                    " is specified. If no destination is specified"
                    " the response code will be 410.")
    )
    
    def page_site(self):
        """If this redirects to a page, return the name of the site."""
        if self.page:
            return u'%s' % self.page.site
        return u''
    page_site.short_description = "Page Site"
    
    def actual_response_code(self):
        """Returns the response code. Returns 410 if no redirect is defined."""
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
        """Unicode representation of this redirect."""
        return "%s ---> %s" % (self.old_path, self.new_path)
