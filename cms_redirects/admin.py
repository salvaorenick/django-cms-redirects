from django.contrib import admin
from cms_redirects.models import CMSRedirect

class CMSRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'page', 'page_site',)
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path', 'page')
    radio_fields = {'site': admin.VERTICAL}
    fieldsets = [
        ('Source', {
            "fields": ('site','old_path',)
        }),
        ('Destination', {
            "fields": ('new_path','page',)
        }),
    ]

admin.site.register(CMSRedirect, CMSRedirectAdmin)
