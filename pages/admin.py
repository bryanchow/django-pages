from django.contrib import admin
from .models import Page, Redirect


class PageAdmin(admin.ModelAdmin):

    list_display = (
        'url',
        'title',
        'visible',
        'modified',
    )
    search_fields = (
        'url',
        'title',
        'body',
    )
    readonly_fields = (
        'created',
        'modified',
    )
    fieldsets = (
        (None, {
            'fields': (
                'url',
                'title',
                'body',
                'section',
            ),
        }),
        ('Search engine optimization', {
            'fields': (
                'page_title',
                'meta_description',
                'meta_keywords',
                'sitemap_changefreq',
                'sitemap_priority',
            ),
            'classes': (
                'collapse',
            ),
        }),
        ('More properties', {
            'fields': (
                'template_name',
                'visible',
                'created',
                'modified',
            ),
            'classes': (
                'collapse',
            ),
        }),
    )

admin.site.register(Page, PageAdmin)


class RedirectAdmin(admin.ModelAdmin):

    list_display = (
        'old_url',
        'new_url',
        'modified',
    )
    search_fields = (
        'old_url',
        'new_url',
    )
    fieldset = (
        (None, {
            'fields': (
                'old_url',
                'new_url',
            ),
        }),
        ('More properties', {
            'fields': (
                'created',
                'modified',
            ),
            'classes': (
                'collapse',
            ),
        }),
    )

admin.site.register(Redirect, RedirectAdmin)
