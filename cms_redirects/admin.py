from django.contrib import admin
from cms_redirects.models import CMSRedirect

class CMSRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'page', 'page_site', 'site', 'actual_response_code',)
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path', 'page__title_set__title')
    radio_fields = {'site': admin.VERTICAL}
    fieldsets = [
        ('Source', {
            "fields": ('site','old_path',)
        }),
        ('Destination', {
            "fields": ('new_path','page', 'response_code',)
        }),
    ]

admin.site.register(CMSRedirect, CMSRedirectAdmin)
