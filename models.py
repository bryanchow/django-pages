from datetime import datetime
from django.core import validators
from django.db import models
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


SITEMAP_CHANGEFREQ_CHOICES = [
    ('always', 'always'),
    ('hourly', 'hourly'),
    ('daily', 'daily'),
    ('weekly', 'weekly'),
    ('monthly', 'monthly'),
    ('yearly', 'yearly'),
    ('never', 'never'),
]


class Page(models.Model):

    url                = models.CharField('URL', max_length=128, validator_list=[validators.isAlphaNumericURL], help_text='Should have leading and trailing slashes. ')
    title              = models.CharField(max_length=128)
    body               = models.TextField(max_length=65536, null=True, blank=True)
    site               = models.ForeignKey(Site, default=1)

    page_title         = models.CharField(max_length=512, null=True, blank=True)
    meta_description   = models.CharField(max_length=512, null=True, blank=True)
    meta_keywords      = models.CharField(max_length=512, null=True, blank=True)
    sitemap_changefreq = models.CharField(null=True, blank=True, max_length=50, choices=SITEMAP_CHANGEFREQ_CHOICES)
    sitemap_priority   = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1, help_text='Enter a value from 0.0 to 1.0. ')

    template_name      = models.CharField(max_length=128, null=True, blank=True, help_text='If left blank, \'pages/default.html\' will be used. ')
    visible            = models.BooleanField(default=True)
    notes              = models.TextField(max_length=16384, null=True, blank=True, help_text='Private notes. ')
    created            = models.DateTimeField(default=datetime.now())
    modified           = models.DateTimeField(blank=True)

    objects            = models.Manager()
    on_site            = CurrentSiteManager('site')

    class Meta:
        unique_together = (('url', 'site'),)
        ordering = ['url',]

    def __repr__(self):
        return self.url

    def __str__(self):
        return str(self.url)

    def get_absolute_url(self):
        return self.url

    def save(self):
        self.modified = datetime.now()
        super(Page, self).save()


class PageAdmin(admin.ModelAdmin):
    
    list_display = ('url', 'title', 'site', 'visible', 'modified') 
    list_filter = ('site',)
    search_fields = ['url', 'title', 'body']
    fieldsets = (
        (None, {'fields': ('url', 'title', 'body', 'site')}),
        ('Search engine optimization', {'fields': ('page_title', 'meta_description', 'meta_keywords', 'sitemap_changefreq', 'sitemap_priority'), 'classes': ('collapse',)}),
        ('More properties', {'fields': ('template_name', 'visible', 'notes', 'created', 'modified'), 'classes': ('collapse',)}),
    )


class Redirect(models.Model):

    old_url            = models.CharField('Old URL', max_length=128, unique=True, help_text='Should have a leading slash. ')
    new_url            = models.CharField('New URL', max_length=128, help_text='Should have leading and trailing slashes. ')
    site               = models.ForeignKey(Site, default=1)

    notes              = models.TextField(max_length=16384, null=True, blank=True, help_text='Private notes. ')
    created            = models.DateTimeField(default=datetime.now())
    modified           = models.DateTimeField(blank=True)

    objects            = models.Manager()
    on_site            = CurrentSiteManager('site')

    class Meta:
        unique_together = (('old_url', 'site'),)
        ordering = ['old_url',]

    def __repr__(self):
        return self.old_url

    def __str__(self):
        return str(self.old_url)

    def get_absolute_url(self):
        return self.new_url

    def save(self):
        self.modified = datetime.now()
        super(Redirect, self).save()


class RedirectAdmin(admin.ModelAdmin):

    list_display = ('old_url', 'new_url', 'site', 'modified') 
    list_filter = ('site',)
    search_fields = ['old_url', 'new_url']
    fieldset = (
        (None, {'fields': ('old_url', 'new_url', 'site')}),
        ('More properties', {'fields': ('notes', 'created', 'modified'), 'classes': ('collapse',)}),
    )


admin.site.register(Page, PageAdmin)
admin.site.register(Redirect, RedirectAdmin)

