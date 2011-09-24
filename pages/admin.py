from django.contrib import admin
from .models import Page, Redirect


class PageAdmin(admin.ModelAdmin):

    list_display = ('url', 'title', 'site', 'visible', 'modified')
    list_filter = ('site',)
    search_fields = ['url', 'title', 'body']
    fieldsets = (
        (None, {'fields': ('url', 'title', 'body', 'body_markup', 'site')}),
        ('Search engine optimization', {'fields': ('page_title', 'meta_description', 'meta_keywords', 'sitemap_changefreq', 'sitemap_priority'), 'classes': ('collapse',)}),
        ('More properties', {'fields': ('template_name', 'visible', 'notes', 'created', 'modified'), 'classes': ('collapse',)}),
    )

admin.site.register(Page, PageAdmin)


class RedirectAdmin(admin.ModelAdmin):

    list_display = ('old_url', 'new_url', 'site', 'modified')
    list_filter = ('site',)
    search_fields = ['old_url', 'new_url']
    fieldset = (
        (None, {'fields': ('old_url', 'new_url', 'site')}),
        ('More properties', {'fields': ('notes', 'created', 'modified'), 'classes': ('collapse',)}),
    )


admin.site.register(Redirect, RedirectAdmin)
