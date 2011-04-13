from django.contrib.redirects.models import Redirect
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField

from cms.models import Page

class CMSRedirect(Redirect):
    page = PageField(verbose_name=_("page"), blank=True, null=True, help_text=_("A link to a page has priority over a text link."))
    
