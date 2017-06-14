from django.db import models
from django.utils.safestring import mark_safe
from . import resources


class Page(models.Model):

    url = models.CharField(
        "URL",
        help_text = "Should have leading and trailing slashes.",
        max_length = 255,
    )
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=65536, blank=True)
    section = models.CharField(
        help_text = (
            "Enter a section name to highlight the corresponding nav element "
            "(optional)."
        ),
        max_length = 32,
        blank = True,
    )

    page_title = models.CharField(max_length=512, blank=True)
    meta_description = models.CharField(max_length=512, blank=True)
    meta_keywords = models.CharField(max_length=512, blank=True)
    sitemap_changefreq = models.IntegerField(
        null = True,
        choices = resources.SITEMAP_CHANGEFREQ_CHOICES,
        default = resources.DEFAULT_SITEMAP_CHANGEFREQ,
    )
    sitemap_priority = models.DecimalField(
        help_text = "Enter a value from 0.0 to 1.0.",
        blank = True,
        max_digits = 2,
        decimal_places = 1,
        default = 0,
    )

    template_name = models.CharField(
        help_text = (
            "If left blank, '%s' will be used." % resources.DEFAULT_TEMPLATE
        ),
        max_length = 128,
        blank = True,
    )
    visible = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('url',)

    def __unicode__(self):
        return unicode(self.url)

    def get_absolute_url(self):
        return self.url

    def render_body(self):
        return mark_safe(self.body)

    def render_sitemap_changefreq(self):
        return resources.SITEMAP_CHANGEFREQS[self.sitemap_changefreq]


class Redirect(models.Model):

    old_url = models.CharField(
        "Old URL",
        help_text = "Should have a leading slash.",
        max_length = 255,
    )
    new_url = models.CharField(
        "New URL",
        help_text = "Should have leading and trailing slashes.",
        max_length = 255,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('old_url',)

    def __unicode__(self):
        return unicode(self.old_url)

    def get_absolute_url(self):
        return self.old_url
