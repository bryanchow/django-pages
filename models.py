from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from factorlib import markup


DEFAULT_MARKUP = 'textile'

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

    url                = models.CharField('URL', max_length=128, help_text='Should have leading and trailing slashes. ')
    title              = models.CharField(max_length=128)
    body               = models.TextField(max_length=65536, null=True, blank=True)
    body_markup        = models.CharField(choices=markup.MARKUP_CHOICES, null=True, default=DEFAULT_MARKUP, max_length=8)
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

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Page, self).save(*args, **kwargs)

    def render_body(self):
        return markup.render(self.body, self.body_markup)


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

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Redirect, self).save(*args, **kwargs)


def redirect_if_slug_changed(sender, **kwargs):
    """
    Automatically create redirects when a saved object's slug has changed.
    Requires that the model being saved has fields called id and slug.
    """
    try:
        new = kwargs['instance']
        old = sender.objects.get(id=new.id)
        new.slug
    except:
        # Abort on any exception
        pass
    else:
        if new.slug != old.slug:
            # Prevent cyclical redirects
            Redirect.objects.filter(old_url=new.get_absolute_url()).delete()
            # Create or fetch redirect for old slug, and point to new slug
            redirect, created = Redirect.objects.get_or_create(old_url=old.get_absolute_url())
            redirect.new_url = new.get_absolute_url()
            redirect.notes = 'Created by redirect_if_slug_changed.'
            redirect.save()

models.signals.pre_save.connect(redirect_if_slug_changed)

