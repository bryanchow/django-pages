from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):

    def lastmod(self, obj):
        return obj.modified

    def changefreq(self, obj):
        return obj.render_sitemap_changefreq()

    def priority(self, obj):
        return obj.sitemap_priority

    def items(self):
        return Page.objects.filter(visible=True)
